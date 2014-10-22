import unittest
from discussionapi.discussion_client import DiscussionFetcher




class MockClient(object):
    def __init__(self, base_url):
        self.base_url = base_url
        self.actual_url = None

    def do_get(self, url):
        self.actual_url = url
        return ('header', TestResponse)


class TestDiscussionClient(unittest.TestCase):
    def test_the_fetcher_should_pass_the_right_url_to_the_client(self):
        base_url = 'http://discussion.com/api'
        client = MockClient(base_url)
        fetcher = DiscussionFetcher(client)
        fetcher.fetch_most_commented(123)

        expected_url = 'http://discussion.com/api/popular?pageSize=123'
        self.assertEquals(expected_url, client.actual_url)

    def test_the_fetcher_should_be_cool_about_trailing_slashes_on_the_base_url(self):
        base_url = 'http://discussion.com/api/' # Different from the last test, yeah?
        client = MockClient(base_url)
        fetcher = DiscussionFetcher(client)
        fetcher.fetch_most_commented(123)

        expected_url = 'http://discussion.com/api/popular?pageSize=123'
        self.assertEquals(expected_url, client.actual_url)

    def test_fetcher_should_parse_response_from_client_into_a_list(self):
        client = MockClient('cheese')
        fetcher = DiscussionFetcher(client)
        most_commented = fetcher.fetch_most_commented('cheese')
        expected_most_commented = [("/p/3f262", 1312), ("/p/3f244", 973), ("/p/3f26a", 469), ("/p/3fxam", 422), ("/p/3f24d", 304)]
        self.assertEquals(expected_most_commented, most_commented)


TestResponse = """

      { "discussions" : [ { "key" : "/p/3f262",
            "numberOfComments" : 1312,
            "url" : "http://www.theguardian.com/politics/blog/2013/apr/09/margaret-thatcher-death-reaction-funeral-live"
          },
          { "key" : "/p/3f244",
            "numberOfComments" : 973,
            "url" : "http://www.theguardian.com/commentisfree/2013/apr/09/thatcher-acolytes-cameron-dont-know-when-to-stop"
          },
          { "key" : "/p/3f26a",
            "numberOfComments" : 469,
            "url" : "http://www.theguardian.com/commentisfree/2013/apr/09/margaret-thatcher-miners-society"
          },
          { "key" : "/p/3fxam",
            "numberOfComments" : 422,
            "url" : "http://www.theguardian.com/technology/gamesblog/2013/apr/09/chatterbox-tuesday"
          },
          { "key" : "/p/3f24d",
            "numberOfComments" : 304,
            "url" : "http://www.theguardian.com/politics/2013/apr/09/chris-grayling-criminals-legal-costs"
      } ] }
"""
