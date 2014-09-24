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
    CommentIsFreeCartoonDataSource, MostViewedDataSource, MediaDataSource, MediaMonkeyDataSource, \
    MediaBriefingDataSource, BusinessDataSource, TravelDataSource, TechnologyDataSource, LifeAndStyleDataSource, \
    TravelMostViewedDataSource, TravelTopTenDataSource, TravelTipsDataSource, TravelVideoDataSource, \
    FashionEditorsPicksDataSource, FashionMostViewedDataSource, FashionAskHadleyDataSource, \
    FashionSaliHughesDataSource, FashionBlogDataSource, FashionNetworkDataSource, \
    FashionNewsDataSource, FashionStylewatchDataSource, FashionGalleryDataSource, FashionVideoDataSource, \
    FilmEditorsPicksDataSource, FilmMostViewedDataSource, FilmInterviewsDataSource, \
    FilmBlogsDataSource, FilmOfTheWeekDataSource, FilmQuizDataSource, FilmShowDataSource, \
    USMoneyDataSource, TechnologyMostViewedDataSource, TechnologyBlogDataSource, \
    TechnologyGamesDataSource, TechnologyPodcastDataSource, TechnologyVideoDataSource, \
    MusicMostViewedDataSource, MusicNewsDataSource, MusicWatchListenDataSource, ContentDataSource, \
    MusicBlogDataSource, MusicEditorsPicksDataSource, CommentIsFreeDataSource, ItemDataSource, \
    MostCommentedDataSource, MostSharedDataSource, MostSharedCountInterpolator, ScienceDataSource, EnvironmentDataSource, VideoDataSource, AusVideoDataSource, \
    MultiContentDataSource, CommentCountInterpolator, AusSportDataSource, AusTopStoriesDataSource, FilmTodayLatestDataSource,  ItemPlusBlogDataSource, fetch_all, build_unique_trailblocks, \
    IndiaDataSource

import data_sources.au as au

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
ophan_base_url = 'http://***REMOVED***'
discussion_base_url = 'http://discussion.guardianapis.com/discussion-api'

client = ApiClient(base_url, api_key, edition="uk")
clientUS = ApiClient(base_url, api_key, edition='us')
clientAUS = ApiClient(base_url, api_key, edition='au')



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

# Super dirty
# import now after the common functionality of this module is defined
# The result of script execution flow

import email_definitions.culture as culture_emails

class AustralianPolitics(EmailTemplate):
    recognized_versions = ['v1']

    ad_tag = 'email-australian-politics'
    ad_config = {}

    data_sources = {
        'v1': {
            'politics_latest': au.AustralianPoliticsDataSource(client),
            'politics_comment': au.AusCommentIsFreeDataSource(clientAUS),
            'politics_video': au.AustralianPoliticsVideoDataSource(client)
        }
    }

    priority_list = {
        'v1': [('politics_comment', 1), ('politics_video', 1), ('politics_latest', 4)]
    }

    template_names = {'v1': 'australian-politics'}


class CloseUp(EmailTemplate):
    recognized_versions = ['v1', 'v2', 'v3']

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
        'film_quiz': FilmQuizDataSource(client)
        }
    data_sources['v2'] = data_sources['v1']
    data_sources['v3'] = data_sources['v1']

    priority_list = {}
    priority_list['v1'] = [('film_week', 1), ('film_show', 1), ('film_interviews', 3),
                           ('film_blogs', 5), ('film_quiz', 1), ('film_picks', 2), ('film_most_viewed', 3)]

    priority_list['v2'] = priority_list['v1']
    priority_list['v3'] = priority_list['v1']

    template_names = {'v1': 'close-up-v1',
                      'v2': 'close-up-v2',
                      'v3': 'close-up-v3'}


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
    recognized_versions = ['v1', 'v2', 'v3', 'v4', 'v5', 'india', 'MPU_v1a', 'MPU_v1b', 'MPU_v2']

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
        }
    data_sources['v2'] = data_sources['v1']
    data_sources['v4'] = data_sources['v1']
    data_sources['v5'] = data_sources['v1']
    data_sources['MPU_v1a'] = data_sources['v1']
    data_sources['MPU_v1b'] = data_sources['v1']
    data_sources['MPU_v2'] = data_sources['v1']
    data_sources['v3'] = {
        'top_stories': TopStoriesDataSource(client),
        'most_viewed': MostViewedDataSource(client)
    }

    data_sources['india'] = data_sources['v1']
    data_sources['india']['india_recent'] = IndiaDataSource(client)


    priority_list = {}
    priority_list['v1'] = [('top_stories', 6), ('most_viewed', 6),
                           ('sport', 3), ('comment', 3), ('culture', 3),
                           ('business', 2), ('technology', 2), ('travel', 2),
                           ('lifeandstyle', 2), ('eye_witness', 1)]

    priority_list['v2'] = [('top_stories', 6), ('most_viewed', 6), ('eye_witness', 1),
                           ('sport', 3), ('culture', 3), ('business', 2),
                           ('technology', 2), ('travel', 2), ('lifeandstyle', 2)]

    priority_list['v3'] = [('top_stories', 16), ('most_viewed', 16)]

    priority_list['v4'] = priority_list['v1']
    priority_list['v5'] = priority_list['v1']
    priority_list['india'] = [('top_stories', 6), ('india_recent', 5), ('most_viewed', 6),
                           ('sport', 3), ('comment', 3), ('culture', 3),
                           ('business', 2), ('technology', 2), ('travel', 2),
                           ('lifeandstyle', 2), ('eye_witness', 1)]
    priority_list['MPU_v1a'] = priority_list['v1']
    priority_list['MPU_v1b'] = priority_list['v1']
    priority_list['MPU_v2'] = priority_list['v1']

    template_names = {'v1': 'daily-email-v1',
                      'v2': 'daily-email-v2',
                      'v3': 'daily-email-v3',
                      'v4': 'daily-email-v4',
                      'v5': 'daily-email-v5',
                      'india': 'daily-email-india',
                      'MPU_v1a': 'daily-email-v6',
                      'MPU_v1b': 'daily-email-v7',
                      'MPU_v2': 'daily-email-v8',}

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
    recognized_versions = ['v1', 'v2', 'v3', 'MPU_v1a', 'MPU_v1b']

    ad_tag = 'email-guardian-today-us'
    ad_config = {
        'leaderboard_v1': 'Top',
        'leaderboard_v2': 'Bottom'
    }

    data_sources = {}
    data_sources['v1'] = {
        'business': BusinessDataSource(clientUS),
        'money': USMoneyDataSource(clientUS),
        'technology': TechnologyDataSource(clientUS),
        'sport': SportUSDataSource(clientUS),
        'comment': CommentIsFreeDataSource(clientUS),
        'culture': CultureDataSource(clientUS),
        'top_stories': TopStoriesDataSource(clientUS),
        'video': VideoDataSource(clientUS),
        }
    data_sources['v2'] = {
        'business': BusinessDataSource(clientUS),
        'money': USMoneyDataSource(clientUS),
        'technology': TechnologyDataSource(clientUS),
        'sport': SportUSDataSource(clientUS),
        'comment': CommentIsFreeDataSource(clientUS),
        'culture': CultureDataSource(clientUS),
        'top_stories': TopStoriesDataSource(clientUS),
        'video': VideoDataSource(clientUS),
        }
    data_sources['v3'] = {
        'business': BusinessDataSource(clientUS),
        'money': USMoneyDataSource(clientUS),
        'technology': TechnologyDataSource(clientUS),
        'sport': SportUSDataSource(clientUS),
        'comment': CommentIsFreeDataSource(clientUS),
        'culture': CultureDataSource(clientUS),
        'top_stories': TopStoriesDataSource(clientUS),
        'video': VideoDataSource(clientUS),
        }
    data_sources['MPU_v1a'] = {
        'business': BusinessDataSource(clientUS),
        'money': USMoneyDataSource(clientUS),
        'technology': TechnologyDataSource(clientUS),
        'sport': SportUSDataSource(clientUS),
        'comment': CommentIsFreeDataSource(clientUS),
        'culture': CultureDataSource(clientUS),
        'top_stories': TopStoriesDataSource(clientUS),
        'video': VideoDataSource(clientUS),
        }
    data_sources['MPU_v1b'] = {
        'business': BusinessDataSource(clientUS),
        'money': USMoneyDataSource(clientUS),
        'technology': TechnologyDataSource(clientUS),
        'sport': SportUSDataSource(clientUS),
        'comment': CommentIsFreeDataSource(clientUS),
        'culture': CultureDataSource(clientUS),
        'top_stories': TopStoriesDataSource(clientUS),
        'video': VideoDataSource(clientUS),
        }


    priority_list = {}
    priority_list['v1'] = [('top_stories', 6), ('video', 3), ('sport', 3), ('comment', 3),
                           ('culture', 3), ('business', 2), ('money', 2), ('technology', 2)]
    priority_list['v2'] = [('top_stories', 6), ('video', 3), ('sport', 3), ('comment', 3),
                           ('culture', 3), ('business', 2), ('money', 2), ('technology', 2)]
    priority_list['v3'] = [('top_stories', 6), ('video', 3), ('sport', 3), ('comment', 3),
                           ('culture', 3), ('business', 2), ('money', 2), ('technology', 2)]
    priority_list['MPU_v1a'] = [('top_stories', 6), ('video', 3), ('sport', 3), ('comment', 3),
                           ('culture', 3), ('business', 2), ('money', 2), ('technology', 2)]
    priority_list['MPU_v1b'] = [('top_stories', 6), ('video', 3), ('sport', 3), ('comment', 3),
                           ('culture', 3), ('business', 2), ('money', 2), ('technology', 2)]

    template_names = {'v1': 'daily-email-us', 'v2': 'daily-email-us-v2', 'v3': 'daily-email-us-v3', 'MPU_v1a': 'daily-email-us-v4', 'MPU_v1b': 'daily-email-us-v5'}

class DailyEmailAUS(EmailTemplate):
    recognized_versions = ['v1', 'v2']

    ad_tag = 'email-guardian-today-aus'
    ad_config = {
        'leaderboard_v1': 'Top',
        'leaderboard_v2': 'Bottom'
    }

    data_sources = {}

    cultureDataSource = ItemPlusBlogDataSource(CultureDataSource(clientAUS), au.AusCultureBlogDataSource(clientAUS))
    
    data_sources['v1'] = {
        'top_stories_code': TopStoriesDataSource(clientAUS),
        'top_stories': TopStoriesDataSource(clientAUS),
        'most_viewed': MostViewedDataSource(clientAUS),
        'sport': SportDataSource(clientAUS),
        'aus_sport': AusSportDataSource(client),
        'culture': cultureDataSource,
        'comment': au.AusCommentIsFreeDataSource(clientAUS),
        'lifeandstyle': LifeAndStyleDataSource(clientAUS),
        'technology': TechnologyDataSource(clientAUS),
        'environment': EnvironmentDataSource(clientAUS),
        'science' : ScienceDataSource(clientAUS),
        'video' :  AusVideoDataSource(clientAUS),
        }

    data_sources['v2'] = dict(data_sources['v1'])
    data_sources['v2'].update({
        'eye_witness' : EyeWitnessDataSource(clientAUS)
    })

    priority_list = {}
    priority_list['v1'] = [('top_stories', 6), ('most_viewed', 6), ('sport', 3),
                           ('aus_sport', 3), ('culture',3), ('comment', 3), ('lifeandstyle', 3),
                           ('technology', 2), ('environment', 2), ('science', 2), ('video', 3)]

    priority_list['v2'] = list(priority_list['v1'])
    priority_list['v2'].append(('eye_witness', 1))

    template_names = {
        'v1': 'daily-email-aus',
        'v2': 'daily-email-aus-v2'
    }

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

    ophan_client = OphanClient(ophan_base_url, ophan_key)
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


class CommentIsFree(EmailTemplate):
    recognized_versions = ['v1', 'v2']

    ad_tag = 'email-speakers-corner'
    ad_config = {
        'leaderboard': 'Top'
    }

    ophan_client = OphanClient(ophan_base_url, ophan_key)
    most_shared_data_source = MostSharedDataSource(
        most_shared_fetcher=MostSharedFetcher(ophan_client, section='commentisfree'),
        multi_content_data_source=MultiContentDataSource(client=client, name='most_shared'),
        shared_count_interpolator=MostSharedCountInterpolator()
    )

    discussion_client = DiscussionClient(discussion_base_url)
    most_commented_data_source = MostCommentedDataSource (
        discussion_fetcher = DiscussionFetcher(discussion_client, 'commentisfree'),
        multi_content_data_source = MultiContentDataSource(client=client, name='most_commented'),
        comment_count_interpolator = CommentCountInterpolator()
    )

    data_sources = {
        'v1': {
            'cif_most_shared': most_shared_data_source,
            'cif_cartoon': CommentIsFreeCartoonDataSource(client),
        },
        'v2': {
            'cif_most_commented': most_commented_data_source,
            'cif_cartoon': CommentIsFreeCartoonDataSource(client),
        }
    }

    priority_list = {
        'v1': [('cif_cartoon', 1), ('cif_most_shared', 5)],
        'v2': [('cif_cartoon', 1), ('cif_most_commented', 5)]
    }

    template_names = {'v1': 'comment-is-free-v1', 'v2': 'comment-is-free-v2'}

class SleeveNotes(EmailTemplate):
    recognized_versions = ['v1', 'v2', 'v3']

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
    data_sources['v2'] = data_sources['v1']
    data_sources['v3'] = data_sources['v1']

    priority_list = {}
    priority_list['v1'] = [('music_most_viewed', 3), ('music_picks', 5), ('music_blog', 5),
                           ('music_watch_listen', 5), ('music_further', 3)]

    priority_list['v2'] = priority_list['v1']
    priority_list['v3'] = priority_list['v1']

    template_names = {'v1': 'sleeve-notes-v1',
                      'v2': 'sleeve-notes-v2',
                      'v3': 'sleeve-notes-v3'}


class TheFlyer(EmailTemplate):
    recognized_versions = ['v1']

    ad_tag = 'email-the-flyer'
    ad_config = {
        'leaderboard': 'Top'
    }

    data_sources = {
        'v1': {
            'travel_picks': TravelDataSource(client),
            'travel_most_viewed': TravelMostViewedDataSource(client),
            'travel_top_ten': TravelTopTenDataSource(client),
            'travel_video': TravelVideoDataSource(client),
            'travel_tips': TravelTipsDataSource(client),
        }
    }

    priority_list = {
        'v1': [('travel_video', 1), ('travel_picks', 5), ('travel_most_viewed', 3),
               ('travel_top_ten', 5), ('travel_tips', 1)]
    }

    template_names = {'v1': 'the-flyer'}


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

class Headline(webapp2.RequestHandler):

    def get(self, edition="uk"):
        def determine_client(edition):
          clients = {'us' : clientUS, 'au' : clientAUS}
          return clients.get(edition, client)

        data_sources = {'top_stories': TopStoriesDataSource(determine_client(edition))}
        priority_list = [('top_stories', 1)]
        template_data = {}
        retrieved_data = fetch_all(data_sources)
        trail_block = build_unique_trailblocks(retrieved_data,priority_list)
        stories = trail_block.get('top_stories')
        headlines = [s.get('webTitle') for s in stories]
        if headlines:
            headline = headlines[0]
            template_data['headline'] = headline
        template = jinja_environment.get_template('headline.html')
        self.response.out.write(template.render(template_data))


app = webapp2.WSGIApplication([('/daily-email/(.+)', DailyEmail),
                               ('/daily-email-us/(.+)', DailyEmailUS),
                               ('/daily-email-aus/(.+)', DailyEmailAUS),
                               ('/australian-politics/(.+)', AustralianPolitics),
                               ('/close-up/(.+)', CloseUp),
                               ('/fashion-statement/(.+)', FashionStatement),
                               ('/media-briefing/(.+)', MediaBriefing),
                               ('/sleeve-notes/(.+)', SleeveNotes),
                               ('/comment-is-free/(.+)', CommentIsFree),
                               ('/film-today/(.+)', culture_emails.FilmToday),
                               ('/the-flyer/(.+)', TheFlyer),
                               ('/zip-file/(.+)', ZipFile),
                               ('/most-commented/(.+)', MostCommented),
                               ('/most-shared/(.+)', MostShared),
                               ('/most-viewed/(.+)', MostViewed),
                               ('/editors-picks/(.+)', EditorsPicks),
                               webapp2.Route(r'/headline', handler=Headline),
                               webapp2.Route(r'/headline/<edition>', handler=Headline),
                               ('/', Index)],
                              debug=True)
