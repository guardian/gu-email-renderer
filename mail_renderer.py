import jinja2
import os
import webapp2
import datetime

from google.appengine.api import memcache

from guardianapi.client import Client
from data_source import \
    CultureDataSource, TopStoriesDataSource, SportDataSource, EyeWitnessDataSource, \
    MostViewedDataSource, \
    fetch_all, build_unique_trailblocks
from ads import AdFetcher


URL_ROOT = '' if os.environ['SERVER_SOFTWARE'].startswith('Development') else "http://***REMOVED***.appspot.com"

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), "template"))
)
jinja_environment.globals['URL_ROOT'] = URL_ROOT

api_key = '***REMOVED***'
base_url = 'http://content.guardianapis.com/'

client = Client(base_url, api_key)
adFetcher = AdFetcher()

class MediaBriefing(webapp2.RequestHandler):
    template = jinja_environment.get_template('daily-email.html')

    data_sources = {
        'top_stories': TopStoriesDataSource(),
        'sport': SportDataSource(),
        'culture': CultureDataSource(),
        'most_viewed': MostViewedDataSource(),
        'eye_witness': EyeWitnessDataSource(),
        }

    priority_list = [('most_viewed', 2), ('eye_witness', 1), ('culture', 3), ('top_stories', 5)]

    def get(self):
        page = memcache.get('media-briefing')

        if not page:
            retrieved_data = fetch_all(client, self.data_sources)
            trail_blocks = build_unique_trailblocks(3, retrieved_data, self.priority_list)
            today = datetime.datetime.now()
            date = today.strftime('%A %d %b %Y')

            page = self.template.render(ad_html=adFetcher.leaderboard(), date=date, **trail_blocks)
            memcache.add('media-briefing', page, 300)

        self.response.out.write(page)


class DailyEmail(webapp2.RequestHandler):
    template = jinja_environment.get_template('daily-email.html')

    data_sources = {
        'sport': SportDataSource(),
        'culture': CultureDataSource(),
        'top_stories': TopStoriesDataSource(),
        'eye_witness': EyeWitnessDataSource(),
        'most_viewed': MostViewedDataSource(),
    }

    priority_list = [('top_stories', 3), ('most_viewed', 3), ('eye_witness', 1), ('sport', 3), ('culture', 3)]

    def get(self):
        page = memcache.get('daily-email')

        if not page:
            retrieved_data = fetch_all(client, self.data_sources)
            trail_blocks = build_unique_trailblocks(3, retrieved_data, self.priority_list)
            today = datetime.datetime.now()
            date = today.strftime('%A %d %b %Y')

            page = self.template.render(ad_html=adFetcher.leaderboard(), date=date, **trail_blocks)
            memcache.add('daily-email', page, 300)

        self.response.out.write(page)

app = webapp2.WSGIApplication([('/daily-email', DailyEmail), ('/media-briefing', MediaBriefing)], debug=True)
