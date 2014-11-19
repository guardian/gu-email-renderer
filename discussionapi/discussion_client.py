from urlparse import urljoin, urlparse
import json
import urllib
import urllib2
import logging

import pysistence as immutable
from google.appengine.api import urlfetch

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
    def __init__(self, client, tagPath=None):
        self.client = client
        self.tagPath = tagPath

    def fetch_most_commented(self, page_size):
        url = self._build_url(page_size)
        (headers, response_string) = self.client.do_get(url)
        short_url_list = self._parse_response(response_string)
        return short_url_list

    def _build_url(self, page_size):
        url = self.client.base_url
        if url[-1] == '/':
            url = url[:-1]
        if self.tagPath:
            return '%s/popular?pageSize=%s&tagPath=%s' % (url, page_size, self.tagPath)
        else:
            return '%s/popular?pageSize=%s' % (url, page_size)

    def _parse_response(self, response):
        discussions = json.loads(response)['discussions']
        return [(discussion['key'], discussion['numberOfComments']) for discussion in discussions]

def comment_counts(client, urls):
    paths = [urlparse(url).path for url in urls]

    counts_url = "{base_url}/getCommentCounts?short-urls={params}".format(
        base_url=client.base_url,
        params=','.join(paths))

    result = urlfetch.fetch(counts_url)

    if not result.status_code == 200:
        logging.warning("Comment Count fetch failed: " + result.status_code)
        return None

    count_data = json.loads(result.content)

    return dict([('http://gu.com' + key, value) for key, value in count_data.items()])
