import unittest2
from ophan_calls import MostSharedFetcher


OphanResponse = """
    [{"url":"http://www.guardian.co.uk/commentisfree/2013/apr/14/thatcher-ding-dong-bbc-charlie-brooker","count":49723},
    {"url":"http://www.guardian.co.uk/music/2013/apr/14/justin-bieber-anne-frank-belieber","count":27556}]
"""


class StubClient:
    base_url = 'base'
    actual_url = None
    def do_get(self, url):
        self.actual_url = url
        return ('headers', OphanResponse)


class TestMostShared(unittest2.TestCase):
    def test_most_shared_fetcher_should_return_list_of_paths_and_share_counts(self):
        stub_client = StubClient()
        fetcher = MostSharedFetcher(stub_client)
        actual_data = fetcher.fetch_most_shared(n_items=34, age=12000)

        expected_data = [('/commentisfree/2013/apr/14/thatcher-ding-dong-bbc-charlie-brooker', 49723),
                         ('/music/2013/apr/14/justin-bieber-anne-frank-belieber', 27556)]
        self.assertEquals(expected_data, actual_data)
