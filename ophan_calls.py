import logging
import urllib
import urllib2
from django.utils import simplejson as json
from urllib import urlencode
from urlparse import urlparse

# TODO: pull this up into a generic http client

class OphanClient(object):
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key

    def do_get(self, url, params=None, add_base=False):
        try:
            final_url = url
            if add_base:
                final_url = self.base_url + url

            if params:
                final_url = final_url + "?" + urlencode(params)

            #logging.info("Ophan url: {url}".format(url=final_url))

            u = urllib2.urlopen(final_url)
        except urllib2.URLError as e:
            if hasattr(e, 'reason'):
                logging.error('Could not reach server while accessing %s. Reason: %s' % (url, e.reason))
            elif hasattr(e, 'code'):
                logging.error('Server could not fulfill request at %s. Error: %s' % (url, e.code))
            raise e

        headers = u.headers.dict
        return headers, u.read()


class MostSharedFetcher(object):
    def __init__(self, client, section=None, country=None):
        self.client = client
        self.section = section
        self.country = country

    def fetch_most_shared(self, age=86400):
        url = self._build_url(age)
        (headers, response_string) = self.client.do_get(url)
        url_list = self._parse_response(response_string)
        return url_list

    def build_params(self, age):
        params = {
            "mins" : str(age/60),
            "referrer" : "social media",
            "api-key" : self.client.api_key
        }

        for name in ['section', 'country']:
            if hasattr(self, name) and getattr(self, name):
                params[name] = getattr(self, name)

        return params

    def _build_url(self, age):
        url = self.client.base_url
        if url[-1] == '/':
            url = url[:-1]

        url =  url + "/api/viral?" + urllib.urlencode(self.build_params(age))
        logging.debug(url)
        return url


    def _extract_path(self, url):
        return urlparse(url).path


    def _parse_response(self, response):
        shared_items = json.loads(response)
        return [(self._extract_path(item['path']), item['hits']) for item in shared_items]


class MostPopularFetcher(object):
    def __init__(self, ophan_client, edition=None):
        self.ophan_client = ophan_client
        self.edition = edition

    def fetch(self):
        params = None
        if self.edition:
            params = {'country' : self.edition}

        headers, most_viewed_result = self.ophan_client.do_get('/api/mostread', params=params, add_base=True)
        if not most_viewed_result:
            return []

        return [(entry['url'], entry['count']) for entry in json.loads(most_viewed_result)]


class MostPopularByTagFetcher(object):
    def __init__(self, ophan_client, keywordTag=None):
        self.ophan_client = ophan_client
        self.keywordTag = keywordTag
        self.age = 86400 #seconds in a day

    def fetch(self):
        params = {
            "age" : str(self.age),
            "api-key" : self.ophan_client.api_key
        }

        path = '/api/mostread/keywordtag/'+ urllib.quote(self.keywordTag, safe='')

        headers, most_viewed_result = self.ophan_client.do_get(path, params=params, add_base=True)

        if most_viewed_result:
            return [(entry['url'], entry['count']) for entry in json.loads(most_viewed_result)]