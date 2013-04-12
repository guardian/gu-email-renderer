import unittest2
from data_source import MostCommentedDataSource


most_commented_short_urls_with_counts = [('cheese', 23), ('egg', 19), ('mouse', 9)]
most_commented_content = ["my", "uncle", "norbert"]


class IdRememberingMultiContentDataSourceStub:
    def __init__(self, client):
        self.content_ids = None
        self.fetch_all_was_called = False

    def fetch_data(self):
        self.fetch_all_was_called = True
        return self.expected_content


class StubDiscussionFetcher:
    def __init__(self):
        self.actual_page_size = None
        self.most_commented_short_urls_with_counts = None

    def fetch_most_commented(self, page_size):
        self.actual_page_size = page_size
        return self.most_commented_short_urls_with_counts


# Where does MostCommentedDataSource get his two clients from?
    # Assume that the Fetcher and the DS already have them

# TODO: test that we ask for n_items

class TestMostCommented(unittest2.TestCase):

    def test_data_source_should_retrieve_most_commented_pieces_of_content(self):
        multi_content_data_source = IdRememberingMultiContentDataSourceStub('client')

        discussion_fetcher = StubDiscussionFetcher()
        discussion_fetcher.most_commented_short_urls_with_counts = most_commented_short_urls_with_counts

        data_source = MostCommentedDataSource(n_items=23,
                                              multi_content_data_source=multi_content_data_source,
                                              discussion_fetcher=discussion_fetcher)
        data_source.fetch_data()
        self.assertEquals(set(multi_content_data_source.content_ids), set(['cheese', 'egg', 'mouse']))

    def test_data_source_should_fetch_each_piece_of_content_from_api(self):
        multi_content_data_source_stub = IdRememberingMultiContentDataSourceStub('client')

        discussion_fetcher = StubDiscussionFetcher()
        discussion_fetcher.most_commented_short_urls_with_counts = most_commented_short_urls_with_counts
        data_source = MostCommentedDataSource(n_items=12, multi_content_data_source=multi_content_data_source_stub,
            discussion_fetcher=discussion_fetcher)
        data_source.fetch_data()
        self.assertTrue(multi_content_data_source_stub.fetch_all_was_called)

    def test_data_source_should_interpolate_most_commented_content_with_comment_counts




