import jinja2
import os
import webapp2
import datetime
import math
import logging


from google.appengine.api import memcache
from guardianapi.client import Client
from data_source import \
    CultureDataSource, TopStoriesDataSource, SportDataSource, EyeWitnessDataSource, \
    MostViewedDataSource, MediaDataSource, MediaMonkeyDataSource, MediaCommentDataSource, \
    BusinessDataSource, TravelDataSource, TechnologyDataSource, LifeAndStyleDataSource, \
    MusicMostViewedDataSource, MusicNewsDataSource, MusicWatchListenDataSource, ContentDataSource, \
    MusicBlogDataSource, MusicEditorsPicksDataSource, CommentIsFreeDataSource, fetch_all, build_unique_trailblocks
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

api_key = '***REMOVED***'
base_url = 'http://content.guardianapis.com/'

client = Client(base_url, api_key)


class EmailTemplate(webapp2.RequestHandler):
    cache = memcache
    ad_fetcher = AdFetcher()

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
            retrieved_data = fetch_all(client, self.data_sources[version_id])
            trail_blocks = build_unique_trailblocks(retrieved_data, self.priority_list[version_id])
            today = datetime.datetime.now()
            date = today.strftime('%A %d %b %Y')

            template_name = self.template_names[version_id] + '.html'
            template = self.resolve_template(template_name)

            page = template.render(ad_html=self.ad_fetcher.leaderboard(), date=date, **trail_blocks)
            self.cache.add(cache_key, page, 300)
        else:
            logging.debug('Cache hit with key: %s' % cache_key)

        self.response.out.write(page)


class MediaBriefing(EmailTemplate):
    recognized_versions = ['v1']

    data_sources = {}
    data_sources['v1'] = {
        'media_stories': MediaDataSource(),
        'media_comment': MediaCommentDataSource(),
        'media_monkey': MediaMonkeyDataSource()
        }

    priority_list = {}
    priority_list['v1'] = [('media_stories', 8), ('media_comment', 1), ('media_monkey', 1)]

    template_names = {'v1': 'media-briefing'}


class DailyEmail(EmailTemplate):
    recognized_versions = ['v1', 'v2']

    data_sources = {}
    data_sources['v1'] = {
        'business': BusinessDataSource(),
        'technology': TechnologyDataSource(),
        'travel': TravelDataSource(),
        'lifeandstyle': LifeAndStyleDataSource(),
        'sport': SportDataSource(),
        'comment': CommentIsFreeDataSource(),
        'culture': CultureDataSource(),
        'top_stories': TopStoriesDataSource(),
        'eye_witness': EyeWitnessDataSource(),
        'most_viewed': MostViewedDataSource(),
        }
    data_sources['v2'] = data_sources['v1']


    priority_list = {}
    priority_list['v1'] = [('top_stories', 6), ('most_viewed', 6), ('sport', 3), ('comment', 3),
                           ('culture', 3), ('business', 2), ('technology', 2), ('travel', 2), ('lifeandstyle', 2),
                           ('eye_witness', 1)]

    priority_list['v2'] = [('top_stories', 6), ('most_viewed', 6), ('eye_witness', 1), ('sport', 3), ('culture', 3),
                               ('business', 2), ('technology', 2), ('travel', 2), ('lifeandstyle', 2)]

    template_names = {'v1': 'daily-email-v1', 'v2': 'daily-email-v2'}


class ShortUrl(webapp2.RequestHandler):
    def get(self, short_url):
        data_sources = {'short_url': ContentDataSource(content_id=short_url)}
        retrieved_data = fetch_all(client, data_sources)
        self.response.out.write(retrieved_data)


class SleeveNotes(EmailTemplate):
    recognized_versions = ['v1']

    data_sources = {}
    data_sources['v1'] = {
        'music_most_viewed': MusicMostViewedDataSource(),

        'music_news': MusicNewsDataSource(),
        'music_blog': MusicBlogDataSource(),
        'music_watch_listen': MusicWatchListenDataSource(),
        'music_editors_picks': MusicEditorsPicksDataSource(),
        }

    priority_list = {}
    priority_list['v1'] = [('music_most_viewed', 3), ('music_news', 5), ('music_blog', 5),
                           ('music_watch_listen', 5), ('music_editors_picks', 3)]
    template_names = {'v1': 'sleeve-notes'}

app = webapp2.WSGIApplication([('/daily-email/(.+)', DailyEmail),
                               ('/media-briefing/(.+)', MediaBriefing),
                               ('/sleeve-notes/(.+)', SleeveNotes),
                                ('/short-url/(.+)', ShortUrl)],
                              debug=True)
