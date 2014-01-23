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


class OphanFetcher(object):
    def __init__(self, client, section='', country=''):
        self.client = client
        self.section = section
        self.country = country

    def fetch(self, age=86400):
        url = self._build_url(age)
        (headers, response_string) = self.client.do_get(url)
        url_list = self._parse_response(response_string)
        return url_list

    def _extract_path(self, url):
        return urlparse(url).path


class MostSharedFetcher(OphanFetcher):
    def __init__(self, client, section='', country=''):
        OphanFetcher.__init__(self, client, section, country)

    def _build_url(self, age):
        url = self.client.base_url
        if url[-1] == '/':
            url = url[:-1]

        return '{base_url}/api/viral?mins={mins:d}&referrer=social+media&api-key={api_key}&section={section}&country={country}'.format(
            base_url=url,
            mins=age/60,
            api_key=self.client.api_key,
            section=self.section,
            country=self.country
            )

    def _parse_response(self, response):
        shared_items = json.loads(response)
        return [(self._extract_path(item['path']), item['hits']) for item in shared_items]

    def __repr__(self):
        return os.environ['CURRENT_VERSION_ID'] + "MostSharedFetcher"


class Top20Fetcher(OphanFetcher):
    def __init__(self, client, section='', country=''):
        OphanFetcher.__init__(self, client, section, country)

    def _build_url(self, age):
        url = self.client.base_url
        if url[-1] == '/':
            url = url[:-1]

        return '{base_url}/api/mostread?mins={mins:d}&api-key={api_key}&section={section}&country={country}'.format(
            base_url=url,
            mins=age/60,
            api_key=self.client.api_key,
            section=self.section,
            country=self.country
            )

    def _parse_response(self, response):
        read_items = json.loads(response)
        return [(self._extract_path(item['url']), item['count']) for item in read_items]

    def __repr__(self):
        return os.environ['CURRENT_VERSION_ID'] + "Top20Fetcher"
