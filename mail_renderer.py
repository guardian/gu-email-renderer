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
    MostViewedDataSource, MediaDataSource, MediaMonkeyDataSource, \
    MediaBriefingDataSource, BusinessDataSource, TravelDataSource, TechnologyDataSource, LifeAndStyleDataSource, \
    AustralianPoliticsDataSource, AustralianPoliticsCommentDataSource, AustralianPoliticsVideoDataSource, \
    FashionEditorsPicksDataSource, FashionMostViewedDataSource, FashionAskHadleyDataSource, \
    FashionSaliHughesDataSource, FashionBlogDataSource, FashionNetworkDataSource, \
    FashionNewsDataSource, FashionStylewatchDataSource, FashionGalleryDataSource, FashionVideoDataSource, \
    FilmEditorsPicksDataSource, FilmMostViewedDataSource, FilmInterviewsDataSource, \
    FilmBlogsDataSource, FilmOfTheWeekDataSource, MusicQuizDataSource, FilmShowDataSource, \
    TechnologyMostViewedDataSource, TechnologyBlogDataSource, \
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
discussion_base_url = 'http://discussion.guardianapis.com/discussion-api'

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
        'v1': [('politics_comment', 1), ('politics_video', 1), ('politics_latest', 4)]
    }

    template_names = {'v1': 'australian-politics'}


class CloseUp(EmailTemplate):
    recognized_versions = ['v1']

    ad_tag = 'email-close-up'
    ad_config = {
        'leaderboard_v1': 'Top',
        'leaderboard_v2': 'Bottom'
    }

    data_sources = {}
    data_sources['v1'] = {
        'film_week': FilmOfTheWeekDataSource(client),
        'film_picks': FilmEditorsPicksDataSource(client),
        'film_show': FilmShowDataSource(client),
        'film_most_viewed': FilmMostViewedDataSource(client),
        'film_interviews': FilmInterviewsDataSource(client),
        'film_blogs': FilmBlogsDataSource(client),
        'film_quiz': MusicQuizDataSource(client)
        }

    priority_list = {}
    priority_list['v1'] = [('film_week', 1), ('film_show', 1), ('film_interviews', 3), ('film_blogs', 5), ('film_quiz', 1), ('film_picks', 2), ('film_most_viewed', 3)]

    template_names = {'v1': 'close-up'}


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
        'media_monkey': MediaMonkeyDataSource(client),
        'media_briefing': MediaBriefingDataSource(client)
        }

    priority_list = {}
    priority_list['v1'] = [('media_stories', 10), ('media_monkey', 1), ('media_briefing', 1)]

    template_names = {'v1': 'media-briefing'}


class DailyEmail(EmailTemplate):
    recognized_versions = ['v1', 'v2', 'v3', 'v4', 'v5', 'v6']

    ad_tag = 'email-guardian-today'
    ad_config = {
        'leaderboard_v1': 'Top',
        'leaderboard_v2': 'Bottom'
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
        'video': VideoDataSource(client),
        }
    data_sources['v2'] = data_sources['v1']
    data_sources['v4'] = data_sources['v1']
    data_sources['v5'] = data_sources['v1']
    data_sources['v6'] = data_sources['v1']

    data_sources['v3'] = {
        'top_stories': TopStoriesDataSource(client),
        'most_viewed': MostViewedDataSource(client)
    }


    priority_list = {}
    priority_list['v1'] = [('top_stories', 6), ('most_viewed', 6), ('video', 3),
                           ('sport', 3), ('comment', 3), ('culture', 3),
                           ('business', 2), ('technology', 2), ('travel', 2),
                           ('lifeandstyle', 2), ('eye_witness', 1)]

    priority_list['v2'] = [('top_stories', 6), ('most_viewed', 6), ('eye_witness', 1),
                           ('sport', 3), ('culture', 3), ('business', 2),
                           ('technology', 2), ('travel', 2), ('lifeandstyle', 2)]

    priority_list['v3'] = [('top_stories', 16), ('most_viewed', 16)]

    priority_list['v4'] = priority_list['v1']
    priority_list['v5'] = priority_list['v1']
    priority_list['v6'] = priority_list['v3']


    template_names = {'v1': 'daily-email-v1',
                      'v2': 'daily-email-v2',
                      'v3': 'daily-email-v3',
                      'v4': 'daily-email-v4',
                      'v5': 'daily-email-v5',
                      'v6': 'daily-email-v6'}

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
        'leaderboard_v1': 'Top',
        'leaderboard_v2': 'Bottom'
    }

    data_sources = {}
    data_sources['v1'] = {
        'business': BusinessDataSource(clientUS),
        'technology': TechnologyDataSource(clientUS),
        'sport': SportUSDataSource(clientUS),
        'comment': CommentIsFreeDataSource(clientUS),
        'culture': CultureDataSource(clientUS),
        'top_stories': TopStoriesDataSource(clientUS),
        'video': VideoDataSource(clientUS),
        }


    priority_list = {}
    priority_list['v1'] = [('top_stories', 6), ('video', 3), ('sport', 3), ('comment', 3),
                           ('culture', 3), ('business', 2), ('technology', 2)]

    template_names = {'v1': 'daily-email-us'}

class DailyEmailAUS(EmailTemplate):
    recognized_versions = ['v1']

    ad_tag = 'email-guardian-today-aus'
    ad_config = {
        'leaderboard_v1': 'Top',
        'leaderboard_v2': 'Bottom'
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
        'music_picks': MusicEditorsPicksDataSource(client),
        'music_blog': MusicBlogDataSource(client),
        'music_watch_listen': MusicWatchListenDataSource(client),
        'music_further': MusicEditorsPicksDataSource(client),
        }

    priority_list = {}
    priority_list['v1'] = [('music_most_viewed', 3), ('music_picks', 5), ('music_blog', 5),
                           ('music_watch_listen', 5), ('music_further', 3)]
    template_names = {'v1': 'sleeve-notes'}


class ZipFile(EmailTemplate):
    recognized_versions = ['v1']

    ad_tag = 'email-technology-roundup'
    ad_config = {
        'leaderboard_v1': 'Top',
        'leaderboard_v2': 'Bottom'
    }

    discussion_client = DiscussionClient(discussion_base_url)
    tech_most_commented = MostCommentedDataSource (
        discussion_fetcher = DiscussionFetcher(discussion_client, 'technology'),
        multi_content_data_source = MultiContentDataSource(client=client, name='most_commented'),
        comment_count_interpolator = CommentCountInterpolator()
    )

    data_sources = {
        'v1': {
            'tech_news': TechnologyDataSource(client),
            'tech_most_commented': tech_most_commented,
            'tech_games': TechnologyGamesDataSource(client),
            'tech_blog': TechnologyBlogDataSource(client),
            'tech_podcast': TechnologyPodcastDataSource(client),
            'tech_video': TechnologyVideoDataSource(client)
        }
    }

    priority_list = {
        'v1': [('tech_video', 1), ('tech_news', 5), ('tech_most_commented', 3), ('tech_games', 3), ('tech_blog', 5), ('tech_podcast', 1)]
    }

    template_names = {'v1': 'zip-file'}


app = webapp2.WSGIApplication([('/daily-email/(.+)', DailyEmail),
                               ('/daily-email-us/(.+)', DailyEmailUS),
                               ('/daily-email-aus/(.+)', DailyEmailAUS),
                               ('/australian-politics/(.+)', AustralianPolitics),
                               ('/close-up/(.+)', CloseUp),
                               ('/fashion-statement/(.+)', FashionStatement),
                               ('/media-briefing/(.+)', MediaBriefing),
                               ('/sleeve-notes/(.+)', SleeveNotes),
                               ('/zip-file/(.+)', ZipFile),
                               ('/most-commented/(.+)', MostCommented),
                               ('/most-shared/(.+)', MostShared),
                               ('/most-viewed/(.+)', MostViewed),
                               ('/editors-picks/(.+)', EditorsPicks),
                               ('/', Index)],
                              debug=True)

