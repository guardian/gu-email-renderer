import jinja2
import os
import webapp2
import datetime
import math
import logging

import pysistence as immutable

from guardianapi.apiClient import ApiClient

import template_filters

import data_source as ds

from handlers import EmailTemplate

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
