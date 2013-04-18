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
    CultureDataSource, TopStoriesDataSource, SportDataSource, EyeWitnessDataSource, \
    MostViewedDataSource, MediaDataSource, MediaBlogDataSource, MediaMonkeyDataSource, MediaCommentDataSource, \
    MediaBriefingDataSource, BusinessDataSource, TravelDataSource, TechnologyDataSource, LifeAndStyleDataSource, \
    MusicMostViewedDataSource, MusicNewsDataSource, MusicWatchListenDataSource, ContentDataSource, \
    MusicBlogDataSource, MusicEditorsPicksDataSource, CommentIsFreeDataSource, MostCommentedDataSource, MostSharedDataSource, MostSharedCountInterpolator, \
    MultiContentDataSource, CommentCountInterpolator, fetch_all, build_unique_trailblocks
from discussionapi.discussion_client import DiscussionFetcher, DiscussionClient
from template_filters import first_paragraph
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
jinja_environment.cache = None

# TODO: Hide me away somewhere warm and secret.
api_key = '***REMOVED***'
base_url = 'http://content.guardianapis.com/'

client = ApiClient(base_url, api_key)


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

            ad_fetcher = getattr(self, 'ad_fetcher', AdFetcher(self.default_ad_tag))

            page = template.render(ad_html=ad_fetcher.leaderboard(), date=date, **trail_blocks)
            self.cache.add(cache_key, page, 300)
        else:
            logging.debug('Cache hit with key: %s' % cache_key)

        self.response.out.write(page)


class MediaBriefing(EmailTemplate):
    recognized_versions = ['v1']

    ad_fetcher = AdFetcher('email-media-briefing')

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


class MostCommented(EmailTemplate):
    recognized_versions = ['v1']
    n_items=6
    discussion_base_url = 'http://discussion.guardianapis.com/discussion-api'


    discussion_client = DiscussionClient(discussion_base_url)
    discussion_fetcher = DiscussionFetcher(discussion_client)
    multi_content_data_source = MultiContentDataSource(client)
    comment_count_interpolator = CommentCountInterpolator()

    most_commented_data_source = MostCommentedDataSource(
        discussion_fetcher=discussion_fetcher,
        multi_content_data_source=multi_content_data_source,
        comment_count_interpolator=comment_count_interpolator,
        n_items=n_items
        )

    data_sources = {}
    data_sources['v1'] = {
        'most_commented': most_commented_data_source
        }

    priority_list = {'v1': [('most_commented', n_items)]}
    template_names = {'v1': 'most-commented'}

class MostShared(EmailTemplate):
    recognized_versions = ['v1']
    n_items=6
    base_url = 'http://***REMOVED***'


    ophan_client = OphanClient(base_url)
    most_shared_fetcher = MostSharedFetcher(ophan_client)
    multi_content_data_source = MultiContentDataSource(client)
    shared_count_interpolator = MostSharedCountInterpolator()

    most_shared_data_source = MostSharedDataSource(
        most_shared_fetcher=most_shared_fetcher,
        multi_content_data_source=multi_content_data_source,
        shared_count_interpolator=shared_count_interpolator,
        n_items=6
    )

    data_sources = {}
    data_sources['v1'] = {
        'most_shared': most_shared_data_source
        }

    priority_list = {'v1': [('most_shared', n_items)]}
    template_names = {'v1': 'most-shared'}


class SleeveNotes(EmailTemplate):
    recognized_versions = ['v1']

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

app = webapp2.WSGIApplication([('/daily-email/(.+)', DailyEmail),
                               ('/media-briefing/(.+)', MediaBriefing),
                               ('/sleeve-notes/(.+)', SleeveNotes),
                                ('/most-commented/(.+)', MostCommented),
                                ('/most-shared/(.+)', MostShared)],


                              debug=True)
