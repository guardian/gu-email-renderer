from google.appengine.api import memcache
import jinja2
import json
import logging
import os
import urllib
import urllib2
import webapp2


jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader( os.path.dirname( __file__ ) + '/template' ) )


class MainPage( webapp2.RequestHandler ):
    def get( self ):
        story_count = 3
        template = jinja_environment.get_template( 'master.html' )
        top_stories = DataSource('search', {
            'tag': 'type/article',
            'show-fields': 'all',
            'lead-content': 'culture/culture',
            'page-size': story_count,
        })

        page = memcache.get('gu-daily-email')

        if not page:
            logging.info('Cache miss')
            page_renderer = PageRenderer({
                'top_stories': top_stories
            }, 'master.html')
            page = page_renderer.render()
            memcache.add('gu-daily-email', page)

        self.response.out.write(page)


app = webapp2.WSGIApplication( [ ( '/', MainPage ) ], debug=True )


class PageRenderer:

    def __init__(self, data_source_map, template_name):
        """
        template_name is the name of a jinja_template.

        data_source_map is a map whose values are objects which know how
        to fetch json data from the api, and return that data as a
        python map; the keys specify interpolation points in the
        template.
        """
        self.data_source_map = data_source_map
        self.template = jinja_environment.get_template(template_name)

        self.template_name = template_name

    def render(self):
        """
        Fetch the json data over the wire and interpolate it into the
        template specified by *template_name*
        """
        data = self._fetch_data()
        #print("Here is the data: " + data['culture'])

        return self.template.render(**data)

    def _fetch_data(self):
        """
        Turn my data_source_map into a data map by calling fetch on each
        value. The keys of the resulting map correspond exactly to those
        of data_source_map.
        """
        fetched_data = {}

        for data_source_name in self.data_source_map:
            data_source = self.data_source_map[data_source_name]
            data = data_source.fetch()
            fetched_data[data_source_name] = data

        return fetched_data

class DataSource:

    base_url = 'http://content.guardianapis.com/%s?%s'
    api_key = '***REMOVED***'
    fields = ['trailText', 'headline', 'liveBloggingNow', 'standfirst', 'commentable', 'thumbnail']

    def __init__(self, endpoint, params):
        params['api-key'] = self.api_key
        params['format'] = 'json'
        params['show-fields'] = ','.join(self.fields)
        self.api_url = self.base_url  % (endpoint, urllib.urlencode(params))

    def fetch(self):
        try:
            logging.info("Here is the api url: " + self.api_url)
            response = urllib2.urlopen(self.api_url)
            response_body = response.read()
            json_response = json.loads(response_body)

            response_object = json_response['response']
            status = response_object['status']
            results = response_object['results']

            return results

        except urllib2.URLError, e:
            pass
