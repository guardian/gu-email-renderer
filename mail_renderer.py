import jinja2
import os
import webapp2
import datetime
import math
import logging

from google.appengine.api import memcache

import pysistence as immutable

from guardianapi.apiClient import ApiClient

from template_filters import first_paragraph, urlencode
import template_filters

import data_source as ds

from ads import AdFetcher

import deduplication
import configuration

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
api_key = configuration.read('CAPI_KEY')
ophan_key = '***REMOVED***'
base_url=configuration.read('CAPI_BASE_URL')
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
            logging.info('Valid versions {0}'.format(", ".join(self.recognized_versions)))
            self.abort(404)

    def resolve_template(self, template_name):
        return jinja_environment.get_template(template_name)

    def additional_template_data(self):
        return immutable.make_dict({})

    def exclude_from_deduplication(self):
        return immutable.make_list()

    @staticmethod
    def fetch_all(data_sources):
        """
        data is a map of type string->data_source.
        return a map with same keys as data, and retrieved data as values
        """

        #import pdb;pdb.set_trace()
        retrieved_data_map = {}

        for key, datasource in data_sources.items():
            retrieved_data_map[key] = datasource.fetch_data()

        return retrieved_data_map

    def get(self, version_id):
        self.check_version_id(version_id)

        cache_key = version_id + str(self.__class__)
        page = self.cache.get(cache_key)

        if self.cache_bust or not page:
            logging.debug('Cache miss with key: %s' % cache_key)
            retrieved_data = EmailTemplate.fetch_all(self.data_sources[version_id])
            trail_blocks = deduplication.build_unique_trailblocks(retrieved_data,
                self.priority_list[version_id],
                excluded=self.exclude_from_deduplication())
            today = datetime.datetime.now()
            date = today.strftime('%A %d %b %Y')

            template_name = self.template_names[version_id] + '.html'
            template = self.resolve_template(template_name)

            ads = {}

            if hasattr(self, 'ad_tag') and self.ad_tag:
                ad_fetcher = AdFetcher(self.ad_tag)
                for name, type in self.ad_config.iteritems():
                    ads[name] = ad_fetcher.fetch_type(type)

            page = template.render(ads=ads, date=date, data=self.additional_template_data(), **trail_blocks)
            self.cache.add(cache_key, page, 300)
        else:
            logging.debug('Cache hit with key: %s' % cache_key)

        self.response.out.write(page)

# Super dirty
# import now after the common functionality of this module is defined
# The result of script execution flow

import email_definitions as emails

class Headline(webapp2.RequestHandler):

    def get(self, edition="uk"):
        def determine_client(edition):
          clients = {'us' : clientUS, 'au' : clientAUS}
          return clients.get(edition, client)

        data_sources = {'top_stories': ds.TopStoriesDataSource(determine_client(edition))}
        priority_list = [('top_stories', 1)]
        template_data = {}
        retrieved_data = EmailTemplate.fetch_all(data_sources)
        trail_block = deduplication.build_unique_trailblocks(retrieved_data,priority_list)
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
                               ('/australia-sport/(.+)', emails.au.Sport),
                               ('/us-opinion/(.+)', emails.us.Opinion),
                               ('/close-up/(.+)', emails.culture.CloseUp),
                               ('/fashion-statement/(.+)', emails.fashion.FashionStatement),
                               ('/media-briefing/(.+)', emails.media.MediaBriefing),
                               ('/sleeve-notes/(.+)', emails.culture.SleeveNotes),
                               ('/bookmarks/(.+)', emails.culture.Bookmarks),
                               ('/comment-is-free/(.+)', emails.cif.CommentIsFree),
                               ('/film-today/(.+)', emails.culture.FilmToday),
                               ('/the-flyer/(.+)', emails.travel.TheFlyer),
                               ('/zip-file/(.+)', emails.technology.ZipFile),
                               ('/most-commented/(.+)', emails.developer.MostCommented),
                               ('/most-shared/uk/(.+)', emails.most_shared.MostSharedUK),
                               ('/most-shared/us/(.+)', emails.most_shared.MostSharedUS),
                               ('/most-shared/au/(.+)', emails.most_shared.MostSharedAU),
                               ('/most-shared/(.+)', emails.most_shared.MostShared),
                               ('/most-viewed/(.+)', emails.developer.MostViewed),
                               ('/editors-picks/(.+)', emails.developer.EditorsPicks),
                               ('/longreads/(.+)', emails.long_reads.LongReads),
                               webapp2.Route(r'/headline', handler=Headline),
                               webapp2.Route(r'/headline/<edition>', handler=Headline),
                               ('/', Index)],
                              debug=True)
