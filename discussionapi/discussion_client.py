from urlparse import urljoin
from django.utils import simplejson as json
import urllib2


class DiscussionClient(object):
    def __init__(self, base_url):
        self.base_url = base_url

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


class DiscussionFetcher(object):
    def __init__(self, client):
        self.client = client

    def fetch_most_commented(self, page_size):
        url = self._build_url(page_size)
        (headers, response_string) = self.client.do_get(url)
        short_url_list = self._parse_response(response_string)
        return short_url_list

    def _build_url(self, page_size):
        url = self.client.base_url
        if url[-1] == '/':
            url = url[:-1]
        return '%s/popular?pageSize=%s' % (url, page_size)

    def _parse_response(self, response):
        discussions = json.loads(response)['discussions']
        return [(discussion['key'], discussion['numberOfComments']) for discussion in discussions]
