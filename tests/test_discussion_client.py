import unittest2
from discussionapi.discussion_client import DiscussionFetcher

class MockClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.actual_url = None

    def do_get(self, url):
        self.actual_url = url


class TestDiscussionClient(unittest2.TestCase):
    def test_the_fetcher_should_pass_the_right_url_to_the_client(self):
        base_url = 'http://discussion.com/api'
        client = MockClient(base_url)
        fetcher = DiscussionFetcher(client)
        fetcher.fetch_most_commented(123)

        expected_url = 'http://discussion.com/api/popular?pageSize=123'
        self.assertEquals(expected_url, client.actual_url)
