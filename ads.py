import logging, re

from google.appengine.api import urlfetch



class AdFetcher(object):
    """
    Class to fetch advert html from OAS.
    """
    def __init__(self, tag):
        self.root_url = "http://oas.guardian.co.uk/RealMedia/ads/adstream_sx.ads/" + tag + "/1234567890"

    def fetch_html(self, ad_type):
        """
        Fetches the raw ad html from OAS
        """
        ad_url = self.root_url + "@" + ad_type
        response = urlfetch.fetch(ad_url)
        if response.status_code == 200:
            content = re.sub(r'width="\d{1,}" height="\d{1,}"', 'width="100%"', response.content)
            return content
        else:
            logging.error("Failed to fetch ad: status code %s, content '%s'" % (response.status_code, response.content))
            return ''

    def fetch_type(self, type):
        """
        Returns an advert by type, use a string e.g. as follows:
         - 'Top' (leaderboard)
         - 'Bottom' (leaderboard)
         - 'x01' (square)
         - 'Right1' (skyscraper)
        """
        return self.fetch_html(type)
