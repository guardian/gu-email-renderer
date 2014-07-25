import logging
import urllib2
import json

from urlparse import urljoin
from django.utils import simplejson as json
from urlparse import urlparse
from urllib import urlencode

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
    def __init__(self, client, section=''):
        self.client = client
        self.section = section

    def fetch_most_shared(self, age=86400):
        url = self._build_url(age)
        (headers, response_string) = self.client.do_get(url)
        url_list = self._parse_response(response_string)
        return url_list

    def _build_url(self, age):
        url = self.client.base_url
        if url[-1] == '/':
            url = url[:-1]

        return '{base_url}/api/viral?mins={mins:d}&referrer=social+media&api-key={api_key}&section={section}'.format(
            base_url=url,
            mins=age/60,
            api_key=self.client.api_key,
            section=self.section
            )

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
