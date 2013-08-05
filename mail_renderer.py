import jinja2
import os
import webapp2
import datetime
import math
import logging



from google.appengine.api import memcache
from guardianapi.apiClient import ApiClient
from ophan_calls import OphanClient, MostSharedFetcher
from data_source import \
    CultureDataSource, TopStoriesDataSource, SportDataSource, SportUSDataSource, EyeWitnessDataSource, \
    MostViewedDataSource, MediaDataSource, MediaBlogDataSource, MediaMonkeyDataSource, MediaCommentDataSource, \
    MediaBriefingDataSource, BusinessDataSource, TravelDataSource, TechnologyDataSource, LifeAndStyleDataSource, \
    AustralianPoliticsDataSource, AustralianPoliticsCommentDataSource, AustralianPoliticsVideoDataSource, \
    FashionEditorsPicksDataSource, FashionMostViewedDataSource, FashionAskHadleyDataSource, \
    FashionSaliHughesDataSource, FashionBlogDataSource, FashionNetworkDataSource, \
    FashionNewsDataSource, FashionStylewatchDataSource, FashionGalleryDataSource, FashionVideoDataSource, \
    TechnologyMostViewedDataSource, TechnologyBootupDataSource, \
    TechnologyGamesDataSource, TechnologyPodcastDataSource, TechnologyVideoDataSource, \
    MusicMostViewedDataSource, MusicNewsDataSource, MusicWatchListenDataSource, ContentDataSource, \
    MusicBlogDataSource, MusicEditorsPicksDataSource, CommentIsFreeDataSource, ItemDataSource, \
    MostCommentedDataSource, MostSharedDataSource, MostSharedCountInterpolator, ScienceDataSource, EnvironmentDataSource, AusCommentIsFreeDataSource, VideoDataSource, AusVideoDataSource, \
    MultiContentDataSource, CommentCountInterpolator, AusSportDataSource, AusTopStoriesDataSource, ItemPlusBlogDataSource, fetch_all, build_unique_trailblocks

from aus_data_sources import AusCultureBlogDataSource, AusFoodBlogDataSource
from discussionapi.discussion_client import DiscussionFetcher, DiscussionClient
from template_filters import first_paragraph, urlencode
from ads import AdFetcher

if os.environ.has_key('SERVER_SOFTWARE') and os.environ['SERVER_SOFTWARE'].startswith('Development'):
    URL_ROOT = ''
else:
    URL_ROOT = 'http://***REMOVED***.appspot.com'




jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), "template"))
)

jinja_environment.globals['URL_ROOT'] = URL_ROOT
jinja_environment.filters['first_paragraph'] = first_paragraph
jinja_environment.filters['urlencode'] = urlencode
jinja_environment.cache = None

# TODO: Hide me away somewhere warm and secret.
api_key = '***REMOVED***'
ophan_key = '***REMOVED***'
base_url='http://***REMOVED***'

client = ApiClient(base_url, api_key, url_suffix='/api/', edition="uk")
clientUS = ApiClient(base_url, api_key, url_suffix='/api/', edition='us')
clientAUS = ApiClient(base_url, api_key, url_suffix='/api/', edition='au')



class Index(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('index.html')
        self.response.out.write(template.render())


class EmailTemplate(webapp2.RequestHandler):
    cache = memcache
    default_ad_tag = 'email-guardian-today'

    def check_version_id(self, version_id):
        if not version_id in self.recognized_versions:
            logging.exception('Unrecognized version: %s' % version_id)
            self.abort(404)

    def resolve_template(self, template_name):
        return jinja_environment.get_template(template_name)

    def get(self, version_id):
        self.check_version_id(version_id)

        cache_key = version_id + str(self.__class__)
        page = self.cache.get(cache_key)

        if not page:
            logging.debug('Cache miss with key: %s' % cache_key)
            retrieved_data = fetch_all(self.data_sources[version_id])
            trail_blocks = build_unique_trailblocks(retrieved_data, self.priority_list[version_id])
            today = datetime.datetime.now()
            date = today.strftime('%A %d %b %Y')

            template_name = self.template_names[version_id] + '.html'
            template = self.resolve_template(template_name)

            ads = {}
            ad_fetcher = AdFetcher(self.ad_tag)
            for name, type in self.ad_config.iteritems():
                ads[name] = ad_fetcher.fetch_type(type)

            page = template.render(ads=ads, date=date, **trail_blocks)
            self.cache.add(cache_key, page, 300)
        else:
            logging.debug('Cache hit with key: %s' % cache_key)

        self.response.out.write(page)


class AustralianPolitics(EmailTemplate):
    recognized_versions = ['v1']

    ad_tag = 'email-australian-politics'
    ad_config = {}

    data_sources = {
        'v1': {
            'politics_latest': AustralianPoliticsDataSource(client),
            'politics_comment': AustralianPoliticsCommentDataSource(client),
            'politics_video': AustralianPoliticsVideoDataSource(client)
        }
    }

    priority_list = {
        'v1': [('politics_comment', 2), ('politics_video', 2), ('politics_latest', 4)]
    }

    template_names = {'v1': 'australian-politics'}


class FashionStatement(EmailTemplate):
    recognized_versions = ['v1', 'v2', 'v3']

    ad_tag = 'email-fashion-statement'
    ad_config = {
        'leaderboard_v1': 'Top',
        'leaderboard_v2': 'Bottom'
    }

    data_sources = {
        'v1': {
            'fashion_news': FashionNewsDataSource(client),
            'fashion_most_viewed': FashionMostViewedDataSource(client),
            'fashion_hadley': FashionAskHadleyDataSource(client),
            'fashion_blog': FashionBlogDataSource(client),
            'fashion_network': FashionNetworkDataSource(client),
            'fashion_gallery': FashionGalleryDataSource(client),
            'fashion_video': FashionVideoDataSource(client)
        },
        'v3': {
            'fashion_picks': FashionEditorsPicksDataSource(client),
            'fashion_video': FashionVideoDataSource(client),
            'fashion_hadley': FashionAskHadleyDataSource(client),
            'fashion_sali': FashionSaliHughesDataSource(client),
            'fashion_stylewatch': FashionStylewatchDataSource(client),
            'fashion_most_viewed': FashionMostViewedDataSource(client),
            'fashion_gallery': FashionGalleryDataSource(client)
        }
    }
    data_sources['v2'] = data_sources['v1']

    priority_list = {
        'v1': [('fashion_hadley', 1), ('fashion_video', 1), ('fashion_most_viewed', 6), ('fashion_news', 3), ('fashion_blog', 6), ('fashion_network', 6), ('fashion_gallery', 1)],
        'v3': [('fashion_video', 1), ('fashion_hadley', 1), ('fashion_sali', 1), ('fashion_stylewatch', 1), ('fashion_picks', 5), ('fashion_most_viewed', 6), ('fashion_gallery', 1)]
    }
    priority_list['v2'] = priority_list['v1']

    template_names = {'v1': 'fashion-statement-v1', 'v2': 'fashion-statement-v2', 'v3': 'fashion-statement-v3'}


class MediaBriefing(EmailTemplate):
    recognized_versions = ['v1']

    ad_tag = 'email-media-briefing'
    ad_config = {
        'leaderboard_v1': 'Top',
        'leaderboard_v2': 'Bottom'
    }

    data_sources = {}
    data_sources['v1'] = {
        'media_stories': MediaDataSource(client),
        'media_blog': MediaBlogDataSource(client),
        'media_comment': MediaCommentDataSource(client),
        'media_monkey': MediaMonkeyDataSource(client),
        'media_briefing': MediaBriefingDataSource(client)
        }

    priority_list = {}
    priority_list['v1'] = [('media_stories', 8), ('media_blog', 3), ('media_comment', 1), ('media_monkey', 1), ('media_briefing', 1)]

    template_names = {'v1': 'media-briefing'}


class DailyEmail(EmailTemplate):
    recognized_versions = ['v1', 'v2']

    ad_tag = 'email-guardian-today'
    ad_config = {
        'leaderboard': 'Top'
    }

    data_sources = {}
    data_sources['v1'] = {
        'business': BusinessDataSource(client),
        'technology': TechnologyDataSource(client),
        'travel': TravelDataSource(client),
        'lifeandstyle': LifeAndStyleDataSource(client),
        'sport': SportDataSource(client),
        'comment': CommentIsFreeDataSource(client),
        'culture': CultureDataSource(client),
        'top_stories': TopStoriesDataSource(client),
        'eye_witness': EyeWitnessDataSource(client),
        'most_viewed': MostViewedDataSource(client),
        }
    data_sources['v2'] = data_sources['v1']


    priority_list = {}
    priority_list['v1'] = [('top_stories', 6), ('most_viewed', 6), ('sport', 3), ('comment', 3),
                           ('culture', 3), ('business', 2), ('technology', 2), ('travel', 2), ('lifeandstyle', 2),
                           ('eye_witness', 1)]

    priority_list['v2'] = [('top_stories', 6), ('most_viewed', 6), ('eye_witness', 1), ('sport', 3), ('culture', 3),
                               ('business', 2), ('technology', 2), ('travel', 2), ('lifeandstyle', 2)]

    template_names = {'v1': 'daily-email-v1', 'v2': 'daily-email-v2'}

class MostViewed(EmailTemplate):
    recognized_versions = ['v1']

    ad_tag = ''
    ad_config = {}

    data_sources = {}
    data_sources['v1'] = { 'most_viewed' : MostViewedDataSource(client) }
    priority_list = {'v1': [('most_viewed', 3)]}
    template_names = {'v1': 'most-viewed'}

class EditorsPicks(EmailTemplate):
    recognized_versions = ['v1']

    ad_tag = ''
    ad_config = {}

    data_sources = {}
    data_sources['v1'] = { 'editors_picks' : TopStoriesDataSource(client) }
    priority_list = {'v1': [('editors_picks', 3)]}
    template_names = {'v1': 'editors-picks'}


class DailyEmailUS(EmailTemplate):
    recognized_versions = ['v1']

    ad_tag = 'email-guardian-today-us'
    ad_config = {
        'leaderboard': 'Top'
    }

    data_sources = {}
    data_sources['v1'] = {
        'business': BusinessDataSource(clientUS),
        'technology': TechnologyDataSource(clientUS),
        'sport': SportUSDataSource(clientUS),
        'comment': CommentIsFreeDataSource(clientUS),
        'culture': CultureDataSource(clientUS),
        'top_stories': TopStoriesDataSource(clientUS),
        }


    priority_list = {}
    priority_list['v1'] = [('top_stories', 6), ('sport', 3), ('comment', 3),
                           ('culture', 3), ('business', 2), ('technology', 2)]

    template_names = {'v1': 'daily-email-us'}

class DailyEmailAUS(EmailTemplate):
    recognized_versions = ['v1']

    ad_tag = 'email-guardian-today'
    ad_config = {
        'leaderboard': 'Top'
    }

    data_sources = {}

    cultureDataSource = ItemPlusBlogDataSource(CultureDataSource(clientAUS), AusCultureBlogDataSource(clientAUS))
    lifeAndStyle = ItemPlusBlogDataSource(LifeAndStyleDataSource(clientAUS), AusFoodBlogDataSource(clientAUS))

    data_sources['v1'] = {
        'top_stories_code': TopStoriesDataSource(clientAUS),
        'top_stories': TopStoriesDataSource(clientAUS),
        'most_viewed': MostViewedDataSource(clientAUS),
        'sport': SportDataSource(clientAUS),
        'aus_sport': AusSportDataSource(client),
        'culture': cultureDataSource,
        'comment': AusCommentIsFreeDataSource(clientAUS),
        'lifeandstyle': lifeAndStyle,
        'technology': TechnologyDataSource(clientAUS),
        'environment': EnvironmentDataSource(clientAUS),
        'science' : ScienceDataSource(clientAUS),
        'video' :  AusVideoDataSource(clientAUS),
        }

    priority_list = {}
    priority_list['v1'] = [('top_stories', 6), ('most_viewed', 6), ('sport', 3),
                           ('aus_sport', 3), ('culture',3), ('comment', 3), ('lifeandstyle', 3),
                           ('technology', 2), ('environment', 2), ('science', 2), ('video', 3)]

    template_names = {'v1': 'daily-email-aus'}


class MostCommented(EmailTemplate):
    recognized_versions = ['v1']
    n_items=6
    discussion_base_url = 'http://discussion.guardianapis.com/discussion-api'


    discussion_client = DiscussionClient(discussion_base_url)
    discussion_fetcher = DiscussionFetcher(discussion_client)
    multi_content_data_source = MultiContentDataSource(client=client, name='most_commented')
    comment_count_interpolator = CommentCountInterpolator()

    most_commented_data_source = MostCommentedDataSource(
        discussion_fetcher=discussion_fetcher,
        multi_content_data_source=multi_content_data_source,
        comment_count_interpolator=comment_count_interpolator
        )

    ad_tag = ''
    ad_config = {}

    data_sources = {}
    data_sources['v1'] = {
        'most_commented': most_commented_data_source
        }

    priority_list = {'v1': [('most_commented', n_items)]}
    template_names = {'v1': 'most-commented'}

class MostShared(EmailTemplate):
    recognized_versions = ['v1']
    n_items = 6
    base_url = 'http://***REMOVED***'


    ophan_client = OphanClient(base_url, ophan_key)
    most_shared_fetcher = MostSharedFetcher(ophan_client)
    multi_content_data_source = MultiContentDataSource(client=client, name='most_shared')
    shared_count_interpolator = MostSharedCountInterpolator()

    most_shared_data_source = MostSharedDataSource(
        most_shared_fetcher=most_shared_fetcher,
        multi_content_data_source=multi_content_data_source,
        shared_count_interpolator=shared_count_interpolator
    )

    data_sources = {}
    data_sources['v1'] = {
        'most_shared': most_shared_data_source
        }

    ad_tag = ''
    ad_config = {}

    priority_list = {'v1': [('most_shared', n_items)]}
    template_names = {'v1': 'most-shared'}


class SleeveNotes(EmailTemplate):
    recognized_versions = ['v1']

    ad_tag = 'email-sleeve-notes'
    ad_config = {
        'leaderboard': 'Top',
        'leaderboard2': 'Bottom',
    }

    data_sources = {}
    data_sources['v1'] = {
        'music_most_viewed': MusicMostViewedDataSource(client),

        'music_news': MusicNewsDataSource(client),
        'music_blog': MusicBlogDataSource(client),
        'music_watch_listen': MusicWatchListenDataSource(client),
        'music_editors_picks': MusicEditorsPicksDataSource(client),
        }

    priority_list = {}
    priority_list['v1'] = [('music_most_viewed', 3), ('music_news', 5), ('music_blog', 5),
                           ('music_watch_listen', 5), ('music_editors_picks', 3)]
    template_names = {'v1': 'sleeve-notes'}


class TheZipFile(EmailTemplate):
    recognized_versions = ['v1']

    ad_tag = ''
    ad_config = {
        'leaderboard_v1': 'Top',
        'leaderboard_v2': 'Bottom'
    }

    data_sources = {
        'v1': {
            'tech_news': TechnologyDataSource(client),
            'tech_most_viewed': TechnologyMostViewedDataSource(client),
            'tech_games': TechnologyGamesDataSource(client),
            'tech_bootup': TechnologyBootupDataSource(client),
            'tech_podcast': TechnologyPodcastDataSource(client),
            'tech_video': TechnologyVideoDataSource(client)
        }
    }

    priority_list = {
        'v1': [('tech_news', 5), ('tech_most_viewed', 3), ('tech_games', 3), ('tech_bootup', 5), ('tech_podcast', 1), ('tech_video', 1)]
    }

    template_names = {'v1': 'the-zip-file'}


app = webapp2.WSGIApplication([('/daily-email/(.+)', DailyEmail),
                               ('/daily-email-us/(.+)', DailyEmailUS),
                               ('/daily-email-aus/(.+)', DailyEmailAUS),
                               ('/australian-politics/(.+)', AustralianPolitics),
                               ('/fashion-statement/(.+)', FashionStatement),
                               ('/media-briefing/(.+)', MediaBriefing),
                               ('/sleeve-notes/(.+)', SleeveNotes),
                               ('/the-zip-file/(.+)', TheZipFile),
                               ('/most-commented/(.+)', MostCommented),
                               ('/most-shared/(.+)', MostShared),
                               ('/most-viewed/(.+)', MostViewed),
                               ('/editors-picks/(.+)', EditorsPicks),
                               ('/', Index)],
                              debug=True)

