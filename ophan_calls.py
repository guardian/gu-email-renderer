import logging
import urllib2
from urlparse import urljoin
from django.utils import simplejson as json
from urlparse import urlparse

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
    def __init__(self, client):
        self.client = client

    def fetch_most_shared(self, n_items, age=86400):
        url = self._build_url(n_items, age)
        (headers, response_string) = self.client.do_get(url)
        url_list = self._parse_response(response_string)
        return url_list

    def _build_url(self, n_items, age):
        url = self.client.base_url
        if url[-1] == '/':
            url = url[:-1]

        return '%s/api/mostreferred?count=%s&age=%s&api-key=%s' % (url, n_items, age, self.client.api_key)

    def _extract_path(self, url):
        return urlparse(url).path


    def _parse_response(self, response):
        shared_items = json.loads(response)
        return [(self._extract_path(item['url']), item['count']) for item in shared_items]
