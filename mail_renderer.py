import jinja2
import logging
import os
import webapp2
from datetime import datetime
from guardianapi.client import Client
from data_source import CultureDataSource, TopStoriesDataSource

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

api_key = '***REMOVED***'
client = Client(api_key)


# http://content.guardianapis.com/search?tag=type/picture,artanddesign/series/picture-of-the-day&page-size=1&format=json&show-media=all&api-key=***REMOVED***

class DailyEmail( webapp2.RequestHandler):
    template = jinja_environment.get_template('index.html')

    def get(self):
        #fields = ','.join(['trailText', 'headline', 'liveBloggingNow', 'standfirst', 'commentable', 'thumbnail', 'byline'])
        #data = client.search(**{'tag': 'type/article', 'section': 'culture', 'show-fields': fields, 'lead-content': 'culture/culture', 'show-editors-picks': True})
        # data = PicOfDayDataSource().fetch_data()
        data = CultureDataSource().fetch_data()
        for result in data:
            logging.info(result)
        page = self.template.render()
        self.response.out.write(page)


app = webapp2.WSGIApplication([('/daily-email', DailyEmail)], debug=True)
