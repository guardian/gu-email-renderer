import logging
import httplib
import urllib2

from google.appengine.api import memcache

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
        raise e
    except httplib.HTTPException:
        logging.warning("HTTP Exception thrown, retries {0} remaining".format(retries))
        return read_url(url, retries=retries-1)

class Fetcher(object):
    def get(self, url):
        api_response = memcache.get(url)

        if api_response:
            return api_response

        u = read_url(url)

        headers = u.headers.dict
        api_response = (headers, u.read())

        memcache.set(url, api_response, time=2*60)

        return api_response



