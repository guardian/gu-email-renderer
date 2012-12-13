import jinja2
import json
import logging
import os
import urllib2
import webapp2

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader( os.path.dirname( __file__ ) ) )


class MainPage( webapp2.RequestHandler ):
    def get( self ):

        template = jinja_environment.get_template( 'index.html' )
        template_values = {}
        DataSource('cock').fetch_data()
        self.response.out.write( template.render( template_values ) )


app = webapp2.WSGIApplication( [ ( '/', MainPage ) ], debug=True )


class PageRenderer:

    def __init__(self, data_source_map, template_name):
        self.data_source_map = data_source_map
        self.template_name = template_name

    def render (self):
        # iterate through map. call fetch on each data_source.
        # turn json into map
        # string and map onto view
        pass


class DataSource:

    def __init__(self, api_url):
        self.api_url = api_url

    def fetch_data(self):
        url = 'http://content.guardianapis.com/search?tag=type%2Farticle&section=culture&format=json&show-fields=all&lead-content=culture%2Fculture&api-key=***REMOVED***'
        try:
            response = urllib2.urlopen(url)
            response_body = response.read()
            json_response = json.loads(response_body)

            response_object = json_response['response']
            status = response_object['status']
            results = response_object['results']

            fields = results[0]['fields'].keys()

            logging.info(fields)


        except urllib2.URLError, e:
            pass
