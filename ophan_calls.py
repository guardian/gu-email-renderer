import logging
import urllib
import urllib2
import json
from urlparse import urlparse, urljoin

# TODO: pull this up into a generic http client

class OphanClient(object):
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key

    def do_get(self, url):
        try:
            u = urllib2.urlopen(url)
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

        if self.section:
            params["section"] = self.section

        if self.country:
            params['country'] = self.country

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
