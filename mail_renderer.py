import jinja2
import os
import webapp2
import datetime
import math
import logging

from google.appengine.api import memcache

import pysistence as immutable

from guardianapi.apiClient import ApiClient
from ophan_calls import OphanClient, MostSharedFetcher
from data_source import \
    CultureDataSource, TopStoriesDataSource, SportDataSource, EyeWitnessDataSource, \
    CommentIsFreeCartoonDataSource, MostViewedDataSource, MediaDataSource, MediaMonkeyDataSource, \
    MediaBriefingDataSource, BusinessDataSource, TravelDataSource, LifeAndStyleDataSource, \
    TravelMostViewedDataSource, TravelTopTenDataSource, TravelTipsDataSource, TravelVideoDataSource, \
    FilmEditorsPicksDataSource, FilmMostViewedDataSource, FilmInterviewsDataSource, \
    FilmBlogsDataSource, FilmOfTheWeekDataSource, FilmQuizDataSource, FilmShowDataSource, \
    MusicMostViewedDataSource, MusicNewsDataSource, MusicWatchListenDataSource, ContentDataSource, \
    MusicBlogDataSource, MusicEditorsPicksDataSource, CommentIsFreeDataSource, ItemDataSource, \
    MostCommentedDataSource, MostSharedDataSource, MostSharedCountInterpolator, ScienceDataSource, EnvironmentDataSource, VideoDataSource, \
    MultiContentDataSource, CommentCountInterpolator, AusTopStoriesDataSource, FilmTodayLatestDataSource,  ItemPlusBlogDataSource, fetch_all, build_unique_trailblocks, \
    IndiaDataSource

import data_sources.au as au
import data_sources.technology as tech_data

from discussionapi.discussion_client import DiscussionFetcher, DiscussionClient
from template_filters import first_paragraph, urlencode
import template_filters
from ads import AdFetcher

if os.environ.has_key('SERVER_SOFTWARE') and os.environ['SERVER_SOFTWARE'].startswith('Development'):
    URL_ROOT = ''
else:
    URL_ROOT = 'http://***REMOVED***.appspot.com'

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), "template")),
)

jinja_environment.globals.update({
        'URL_ROOT': URL_ROOT,
    })

jinja_environment.filters.update({
        'first_paragraph': template_filters.first_paragraph,
        'urlencode': template_filters.urlencode,
        'largest_image': template_filters.largest_image,
        'image_of_width': template_filters.image_of_width,
        'asset_url': template_filters.asset_url,
    })

jinja_environment.cache=None


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
    cache_bust = False
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

        if self.cache_bust or not page:
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

import email_definitions as emails

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

    template_names = immutable.make_dict({
        'v1': 'comment-is-free/v1',
        'v2': 'comment-is-free/v2',
    })

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

    template_names = {'v1': 'travel/the-flyer'}


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


app = webapp2.WSGIApplication([('/daily-email/(.+)', emails.uk.DailyEmail),
                               ('/daily-email-us/(.+)', emails.us.DailyEmailUS),
                               ('/daily-email-aus/(.+)', emails.au.DailyEmailAUS),
                               ('/australian-politics/(.+)', emails.au.Politics),
                               ('/australian-cif/(.+)', emails.au.CommentIsFree),
                               ('/australia-morning/(.+)', emails.au.Morning),
                               ('/us-opinion/(.+)', emails.us.Opinion),
                               ('/close-up/(.+)', emails.culture.CloseUp),
                               ('/fashion-statement/(.+)', emails.fashion.FashionStatement),
                               ('/media-briefing/(.+)', emails.media.MediaBriefing),
                               ('/sleeve-notes/(.+)', emails.culture.SleeveNotes),
                               ('/bookmarks/(.+)', emails.culture.Bookmarks),
                               ('/comment-is-free/(.+)', CommentIsFree),
                               ('/film-today/(.+)', emails.culture.FilmToday),
                               ('/the-flyer/(.+)', TheFlyer),
                               ('/zip-file/(.+)', emails.technology.ZipFile),
                               ('/most-commented/(.+)', MostCommented),
                               ('/most-shared/uk/(.+)', emails.most_shared.MostSharedUK),
                               ('/most-shared/us/(.+)', emails.most_shared.MostSharedUS),
                               ('/most-shared/au/(.+)', emails.most_shared.MostSharedAU),
                               ('/most-shared/(.+)', emails.most_shared.MostShared),
                               ('/most-viewed/(.+)', MostViewed),
                               ('/editors-picks/(.+)', EditorsPicks),
                               webapp2.Route(r'/headline', handler=Headline),
                               webapp2.Route(r'/headline/<edition>', handler=Headline),
                               ('/', Index)],
                              debug=True)
