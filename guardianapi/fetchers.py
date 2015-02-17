import logging
import urllib2

from google.appengine.api import memcache

def best_fetcher():
    return Fetcher()

class Fetcher(object):
    def get(self, url):
        api_response = memcache.get(url)

        if api_response:
            return api_response

        try:
            u = urllib2.urlopen(url, timeout=12)
        except urllib2.URLError as e:
            if hasattr(e, 'reason'):
                logging.error('Could not reach server while accessing %s. Reason: %s' % (url, e.reason))
            elif hasattr(e, 'code'):
                logging.error('Server could not fulfill request at %s. Error: %s' % (url, e.code))
            raise e

        headers = u.headers.dict
        api_response = (headers, u.read())

        memcache.set(url, api_response, time=2*60)

        return api_response



