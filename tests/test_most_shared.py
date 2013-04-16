import unittest2
from ophan_calls import MostSharedFetcher
from data_source import MostSharedDataSource, MostSharedCountInterpolator

OphanResponse = """
    [{"url":"http://www.guardian.co.uk/commentisfree/2013/apr/14/thatcher-ding-dong-bbc-charlie-brooker","count":49723},
    {"url":"http://www.guardian.co.uk/music/2013/apr/14/justin-bieber-anne-frank-belieber","count":27556}]
"""
comment_count_list = [("http://www.guardian.co.uk/commentisfree/2013/apr/14/thatcher-ding-dong-bbc-charlie-brooker", 49723), ("http://www.guardian.co.uk/music/2013/apr/14/justin-bieber-anne-frank-belieber", 27556)]
api_data = ["mr", "big", "cheese"]

class IdRememberingMultiContentDataSourceStub:
    def __init__(self, client):
        self.fields = []
        self.content_ids = None
        self.fetch_all_was_called = False

    def fetch_data(self):
        self.fetch_all_was_called = True;
        return api_data


class StubClient:
    base_url = 'base'
    actual_url = None

    def do_get(self, url):
        self.actual_url = url
        return ('headers', OphanResponse)


class StubMostSharedFetcher:
    def __init__(self):
        self.actual_page_size = None
        self.most_shared_urls_with_counts = comment_count_list
    def fetch_most_shared(self, page_size, age=86400):
        self.actual_page_size = page_size
        self.age = age
        return self.most_shared_urls_with_counts


class SharedCountInterpolator:
    def interpolate(self, comment_count_list, content_list):
        self.content_list = content_list
        self.comment_count_list = comment_count_list
        return 'Interpolated content'




class TestMostShared(unittest2.TestCase):
    def test_most_shared_fetcher_should_return_list_of_paths_and_share_counts(self):
        stub_client = StubClient()
        fetcher = MostSharedFetcher(stub_client)
        actual_data = fetcher.fetch_most_shared(n_items=34, age=12000)

        expected_data = [('/commentisfree/2013/apr/14/thatcher-ding-dong-bbc-charlie-brooker', 49723),
                         ('/music/2013/apr/14/justin-bieber-anne-frank-belieber', 27556)]
        self.assertEquals(expected_data, actual_data)

    def test_should_build_correct_url_for_ophan_call(self):
        stub_client = StubClient()
        fetcher = MostSharedFetcher(stub_client)
        fetcher.fetch_most_shared(n_items=34, age=12000)
        self.assertEquals(stub_client.actual_url, 'base//api/mostreferred?count=34&age=12000')

    def test_should_fetch_specified_number_of_items(self):
        multi_content_data_source = IdRememberingMultiContentDataSourceStub('client')
        most_shared_fetcher = StubMostSharedFetcher()
        shared_count_interpolator = SharedCountInterpolator()

        data_source = MostSharedDataSource(n_items=23,
            multi_content_data_source=multi_content_data_source,
            most_shared_fetcher=most_shared_fetcher,
            shared_count_interpolator=shared_count_interpolator
        )
        data_source.fetch_data()
        self.assertEquals(most_shared_fetcher.actual_page_size,23)

    def test_should_fetch_each_piece_of_content_from_api(self):
        multi_content_data_source = IdRememberingMultiContentDataSourceStub('client')
        most_shared_fetcher = StubMostSharedFetcher()
        shared_count_interpolator = SharedCountInterpolator()

        data_source = MostSharedDataSource(n_items=23,
            multi_content_data_source=multi_content_data_source,
            most_shared_fetcher=most_shared_fetcher,
            shared_count_interpolator=shared_count_interpolator
        )
        data_source.fetch_data()
        self.assertTrue(multi_content_data_source.fetch_all_was_called)

    def test_should_return_interpolated_content(self):
        multi_content_data_source = IdRememberingMultiContentDataSourceStub('client')
        most_shared_fetcher = StubMostSharedFetcher()
        shared_count_interpolator = SharedCountInterpolator()

        data_source = MostSharedDataSource(n_items=23,
            multi_content_data_source=multi_content_data_source,
            most_shared_fetcher=most_shared_fetcher,
            shared_count_interpolator=shared_count_interpolator
        )
        data = data_source.fetch_data()
        self.assertEquals(list('Interpolated content'), data)

    def test_should_should_set_a_list_of_paths_on_multi_content_data_source(self):
        multi_content_data_source = IdRememberingMultiContentDataSourceStub('client')
        most_shared_fetcher = StubMostSharedFetcher()
        shared_count_interpolator = SharedCountInterpolator()

        data_source = MostSharedDataSource(n_items=23,
            multi_content_data_source=multi_content_data_source,
            most_shared_fetcher=most_shared_fetcher,
            shared_count_interpolator=shared_count_interpolator
        )
        expected_content_ids = ["/commentisfree/2013/apr/14/thatcher-ding-dong-bbc-charlie-brooker", "/music/2013/apr/14/justin-bieber-anne-frank-belieber"]
        data_source.fetch_data()
        self.assertListEqual(expected_content_ids,multi_content_data_source.content_ids)

    def test_should_call_interpolator_with_shared_counts_and_content_list(self):
        multi_content_data_source = IdRememberingMultiContentDataSourceStub('client')
        most_shared_fetcher = StubMostSharedFetcher()
        shared_count_interpolator = SharedCountInterpolator()

        data_source = MostSharedDataSource(n_items=23,
            multi_content_data_source=multi_content_data_source,
            most_shared_fetcher=most_shared_fetcher,
            shared_count_interpolator=shared_count_interpolator
        )
        data_source.fetch_data()
        self.assertEquals(api_data, shared_count_interpolator.content_list)
        self.assertEquals(comment_count_list, shared_count_interpolator.comment_count_list)



class TestMostSharedInterpolator(unittest2.TestCase):
    def test_should_interpolate_share_counts_into_content(self):

        content_list = [
            {
                "id": "id_1",
                "sectionId": "cif",
                "sectionName": "cif name",
                "webPublicationDate": "2013-04-12T14:15:00Z",
                "webTitle": "Why I wish Huma Abedin had left Anthony Weiner in the dust | Jill Filipovic",
                "webUrl": "http://www.guardian.co.uk/commentisfree/2013/apr/12/anthony-weiner-wife-huma-abedin",
                "apiUrl": "http://content.guardianapis.com/commentisfree/2013/apr/12/anthony-weiner-wife-huma-abedin",
                "fields": {
                    "trailText": "happy trails",
                    "standfirst": "Stand pipe",
                    "shortUrl": "http://gu.com/p/3f1xj",
                    "thumbnail": "well thumbed",
                    "byline": "Branch line",
                    }},
            {
                "id": "id_2",
                "sectionId": "cif",
                "sectionName": "cif name",
                "webPublicationDate": "2013-04-12T14:15:00Z",
                "webTitle": "Why I wish Huma Abedin had left Anthony Weiner in the dust | Jill Filipovic",
                "webUrl": "http://www.guardian.co.uk/commentisfree/2013/apr/12/boston-bomb",
                "apiUrl": "http://content.guardianapis.com/commentisfree/2013/apr/12/boston-bomb",
                "fields": {
                    "trailText": "happy trails",
                    "standfirst": "Stand pipe",
                    "shortUrl": "http://gu.com/p/3f2xj",
                    "thumbnail": "well thumbed 2",
                    "byline": "Branch line 2",
                    }},
            {
                "id": "id_3",
                "sectionId": "cif 3",
                "sectionName": "cif name 3",
                "webPublicationDate": "2013-04-12T14:15:00Z",
                "webTitle": "Why I wish Huma Abedin had left Anthony Weiner in the dust | Jill Filipovic",
                "webUrl": "http://www.guardian.co.uk//commentisfree/2013/apr/12/iain-duncan-smith-exposed-as-popper-sniffer",
                "apiUrl": "http://content.guardianapis.com/commentisfree/2013/apr/12/iain-duncan-smith-exposed-as-popper-sniffer",
                "fields": {
                    "trailText": "happy trails 3",
                    "standfirst": "Stand pipe",
                    "shortUrl": "http://gu.com/p/3f3xj",
                    "thumbnail": "well thumbed",
                    "byline": "Branch line",
                    }},
            {
                "id": "id_4",
                "sectionId": "cif 4",
                "sectionName": "cif name",
                "webPublicationDate": "2013-04-12T14:15:00Z",
                "webTitle": "Why I wish Huma Abedin had left Anthony Weiner in the dust | Jill Filipovic",
                "webUrl": "http://www.guardian.co.uk/commentisfree/2013/apr/12/monbiot-declarers-he-is-god",
                "apiUrl": "http://content.guardianapis.com/commentisfree/2013/apr/12/monbiot-declarers-he-is-god",
                "fields": {
                    "trailText": "happy trails 4",
                    "standfirst": "Stand pipe 4",
                    "shortUrl": "http://gu.com/p/3f4xj",
                    "thumbnail": "well thumbed",
                    "byline": "Branch line",
                    }}]

        shared_count_list = [('http://www.guardian.co.uk/commentisfree/2013/apr/12/anthony-weiner-wife-huma-abedin', 99), ('http://www.guardian.co.uk/commentisfree/2013/apr/12/boston-bomb', 3), ('http://www.guardian.co.uk//commentisfree/2013/apr/12/iain-duncan-smith-exposed-as-popper-sniffer', 28), ('http://www.guardian.co.uk/commentisfree/2013/apr/12/monbiot-declarers-he-is-god', 102)]

        expected_interpolated_content = [
            {
                "share_count": 99,
                "id": "id_1",
                "sectionId": "cif",
                "sectionName": "cif name",
                "webPublicationDate": "2013-04-12T14:15:00Z",
                "webTitle": "Why I wish Huma Abedin had left Anthony Weiner in the dust | Jill Filipovic",
                "webUrl": "http://www.guardian.co.uk/commentisfree/2013/apr/12/anthony-weiner-wife-huma-abedin",
                "apiUrl": "http://content.guardianapis.com/commentisfree/2013/apr/12/anthony-weiner-wife-huma-abedin",
                "fields": {
                    "trailText": "happy trails",
                    "standfirst": "Stand pipe",
                    "shortUrl": "http://gu.com/p/3f1xj",
                    "thumbnail": "well thumbed",
                    "byline": "Branch line",
                    }},
            {
                "share_count": 3,
                "id": "id_2",
                "sectionId": "cif",
                "sectionName": "cif name",
                "webPublicationDate": "2013-04-12T14:15:00Z",
                "webTitle": "Why I wish Huma Abedin had left Anthony Weiner in the dust | Jill Filipovic",
                "webUrl": "http://www.guardian.co.uk/commentisfree/2013/apr/12/boston-bomb",
                "apiUrl": "http://content.guardianapis.com/commentisfree/2013/apr/12/boston-bomb",
                "fields": {
                    "trailText": "happy trails",
                    "standfirst": "Stand pipe",
                    "shortUrl": "http://gu.com/p/3f2xj",
                    "thumbnail": "well thumbed 2",
                    "byline": "Branch line 2",
                    }},
            {
                "share_count": 28,
                "id": "id_3",
                "sectionId": "cif 3",
                "sectionName": "cif name 3",
                "webPublicationDate": "2013-04-12T14:15:00Z",
                "webTitle": "Why I wish Huma Abedin had left Anthony Weiner in the dust | Jill Filipovic",
                "webUrl": "http://www.guardian.co.uk//commentisfree/2013/apr/12/iain-duncan-smith-exposed-as-popper-sniffer",
                "apiUrl": "http://content.guardianapis.com/commentisfree/2013/apr/12/iain-duncan-smith-exposed-as-popper-sniffer",
                "fields": {
                    "trailText": "happy trails 3",
                    "standfirst": "Stand pipe",
                    "shortUrl": "http://gu.com/p/3f3xj",
                    "thumbnail": "well thumbed",
                    "byline": "Branch line",
                    }},
            {
                "share_count": 102,
                "id": "id_4",
                "sectionId": "cif 4",
                "sectionName": "cif name",
                "webPublicationDate": "2013-04-12T14:15:00Z",
                "webTitle": "Why I wish Huma Abedin had left Anthony Weiner in the dust | Jill Filipovic",
                "webUrl": "http://www.guardian.co.uk/commentisfree/2013/apr/12/monbiot-declarers-he-is-god",
                "apiUrl": "http://content.guardianapis.com/commentisfree/2013/apr/12/monbiot-declarers-he-is-god",
                "fields": {
                    "trailText": "happy trails 4",
                    "standfirst": "Stand pipe 4",
                    "shortUrl": "http://gu.com/p/3f4xj",
                    "thumbnail": "well thumbed",
                    "byline": "Branch line",
                    }}]

        interpolator = MostSharedCountInterpolator()
        interpolated_data = interpolator.interpolate(content_list=content_list, shared_count_list=shared_count_list)
        self.maxDiff = None
        self.assertListEqual(expected_interpolated_content, interpolated_data)







