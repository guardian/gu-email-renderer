import jinja2
import logging
import os
import webapp2
from guardianapi.client import Client
from data_source import \
    CultureDataSource, TopStoriesDataSource, SportDataSource, EyeWitnessDataSource, \
    MostViewedDataSource, EditorsPicksDataSource, \
    fetch_all, take_unique_subsets


jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

api_key = '***REMOVED***'
client = Client(api_key)


class DailyEmail( webapp2.RequestHandler):
    template = jinja_environment.get_template('index.html')

    data_sources = {
        'sport': SportDataSource(),
        'culture': CultureDataSource(),
        'top_stories': TopStoriesDataSource(),
        'eye_witness': EyeWitnessDataSource(),
        'most_viewed': MostViewedDataSource(),
    }

    priority_list = ['top_stories', 'most_viewed', 'eye_witness', 'sport', 'culture']

    def get(self):

        retrieved_data = fetch_all(client, self.data_sources)
        deduped_data = take_unique_subsets(3, retrieved_data, self.priority_list)

        page = self.template.render(deduped_data)
        self.response.out.write(page)


app = webapp2.WSGIApplication([('/daily-email', DailyEmail)], debug=True)



