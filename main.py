import jinja2
import json
import logging
import os
import urllib2
import urllib
import webapp2

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader( os.path.dirname( __file__ ) ) )


class MainPage( webapp2.RequestHandler ):
    def get( self ):

        template = jinja_environment.get_template( 'index.html' )
        template_values = {}
        DataSource('').fetch_data()
        self.response.out.write( template.render( template_values ) )


app = webapp2.WSGIApplication( [ ( '/', MainPage ) ], debug=True )


class PageRenderer:

    def __init__(self, data_source_map, template_name):
        self.data_source_map = data_source_map
        self.template_name = template_name

    def render (self):
        # iterate through map. call fetch on each data_source.
        # turn json into map
        # put string and map onto view
        pass


class DataSource:

    base_url = 'http://content.guardianapis.com/'
    api_key = '***REMOVED***'

    #fields = ['trailText', 'headline', 'liveBloggingNow', 'standfirst', 'commentable']


    def __init__(self, end_point, params):
        params['api-key'] = api_key
        self.api_url = base_url + endpoint + urllib.urlencode(params)

    def fetch_data(self):
        try:
            response = urllib2.urlopen(api_url)
            response_body = response.read()
            json_response = json.loads(response_body)

            response_object = json_response['response']
            status = response_object['status']
            results = response_object['results']

            logging.info(fields)
            return results

        except urllib2.URLError, e:
            pass
