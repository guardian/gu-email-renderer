from urlparse import urljoin


class DiscussionClient:
    def do_get(self, base_url):
        """Return the response body as a string"""
        self.base_url = base_url

class DiscussionFetcher:
    def __init__(self, client):
        self.client = client

    def fetch_most_commented(self, page_size):
        """ I return a list of short url strings"""
        # make the right url and do a get on the client

        url = self._build_url(page_size)
        response_string = self.client.do_get(url)
        short_url_list = self._parse_response(response_string)
        return short_url_list

    def _build_url(self, page_size):
        return '%s/popular?pageSize=%s' % (self.client.base_url, page_size)

    def _parse_response(self, response):
        pass
