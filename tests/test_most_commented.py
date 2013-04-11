import unittest2
from data_source import MostCommentedDataSource


most_commented_short_urls_with_counts = [('cheese', 23), ('egg', 19), ('mouse', 9)]


class StubDiscussionFetcher:
    def __init__(self):
        self.actual_page_size = None
        self.most_commented_short_urls_with_counts = None

    def fetch_most_commented(self, page_size):
        self.actual_page_size = page_size
        return self.most_commented_short_urls_with_counts


class StubContentDataSource:
    # def __init__(self, **kwargs):
    #     pass
    pass


class TestMostCommented(unittest2.TestCase):

    def test_data_source_should_retrieve_most_commented_content(self):
        client = None
        content_data_source = StubContentDataSource()

        discussion_fetcher = StubDiscussionFetcher()
        discussion_fetcher.most_commented_short_urls_with_counts = most_commented_short_urls_with_counts

        data_source = MostCommentedDataSource(client=client,
                                              page_size=23,
                                              content_data_source=content_data_source,
                                              discussion_fetcher=discussion_fetcher)
        data_source.fetch_data()
