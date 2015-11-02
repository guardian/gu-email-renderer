import logging
import httplib
import urllib2

from google.appengine.api import memcache

import defaults

def best_fetcher():
    return Fetcher()

def read_url(url, retries=1, timeout=5):
    try:
        return urllib2.urlopen(url, timeout=timeout)
    except urllib2.URLError as e:
        if hasattr(e, 'reason'):
            logging.error('Could not reach server while accessing %s. Reason: %s' % (url, e.reason))
        elif hasattr(e, 'code'):
            logging.error('Server could not fulfill request at %s. Error: %s' % (url, e.code))
        return None
    except httplib.HTTPException as he:
        logging.warning("HTTP Exception thrown, retries {0} remaining".format(retries))
        if retries:
            return read_url(url, retries=retries-1)
        raise he

class Fetcher(object):
    def get(self, url):
        api_response = memcache.get(url)

        if api_response:
            return api_response

        u = read_url(url)

        if not u:
            return None, None

        headers = u.headers.dict
        api_response = (headers, u.read())

        response_length = sum([len(api_response[i]) for i in range(2)])

        if response_length < defaults.MAX_MEMCACHE_LENGTH:
            memcache.set(url, api_response, time=defaults.CACHE_TIME)

        return api_response



