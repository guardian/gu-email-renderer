#! /usr/bin/python

from urllib2 import urlparse
import unittest2
import urllib


from data_source import \
    CultureDataSource, SportDataSource, MostViewedDataSource, \
    PicOfDayDataSource, TopStoriesDataSource, SearchDataSource, \
    MediaDataSource, MediaCommentDataSource, MediaMonkeyDataSource, \
    ItemDataSource, EyeWitnessDataSource, MusicBlogDataSource, MusicNewsDataSource, MusicWatchListenDataSource, \
    MusicVideoDataSource, MusicAudioDataSource, MusicEditorsPicksDataSource, MusicMostViewedDataSource, \
    BusinessDataSource, LifeAndStyleDataSource, TravelDataSource, TechnologyDataSource, \
    DataSourceException, ContentDataSource, fetch_all
from guardianapi.apiClient import ApiClient
from datetime import datetime
from test_fetchers import ApiStubFetcher

API_KEY = '***REMOVED***'
Fields = 'trailText,headline,liveBloggingNow,standfirst,commentable,thumbnail,byline'
DEBUG = False




class UrlCapturingFetcher():
    def get(self, url):
        self.actual_url = url
        return (None, '{"response": {"results": [], "editorsPicks": [], "mostViewed": []}}')


fetcher = UrlCapturingFetcher()
url_capturing_client = ApiClient('http://content.guardianapis.com/', API_KEY, fetcher)

class TestDataSources(unittest2.TestCase):

    def quote_params(self, query_params):
        quoted_params = {}
        for key in query_params.keys():
            new_key = key.replace('_', '-')
            new_value = urllib.quote_plus(query_params[key])
            quoted_params[new_key] = new_value
        return quoted_params


    def compare_tags(self, expected_tags, actual_tags):
        actual_tag_set = set(actual_tags.split('%2C'))
        expected_tag_set = set(expected_tags.split('%2C'))
        self.assertEquals(expected_tag_set,  actual_tag_set)


    def assert_expected_url_equals(self, actual_url, expected_path, expected_args):
        (scheme, netloc, path, params, query, fragment) = urlparse.urlparse(actual_url)
        actual_args = dict([arg.split('=') for arg in query.split('&')])

        self.assertEquals(set(actual_args.keys()), set(expected_args.keys()))

        for key in actual_args:
            if key == 'tag':
                self.compare_tags(expected_args['tag'], actual_args['tag'])
            else:
                self.assertEquals(actual_args[key], expected_args[key])

        self.assertEquals(path, expected_path)


    def check_data_source_url(self, data_source, expected_path, **expected_args):
        expected_args['api-key'] = API_KEY
        expected_args['format'] = 'json'

        if not expected_args.has_key('tag'):
            expected_args['tag'] = '-news/series/picture-desk-live'
        else:
            expected_args['tag'] += ',-news/series/picture-desk-live'

        data_source.fetch_data()

        if DEBUG:
            print 'Testing url for %s' % data_source.__class__
            print 'Expected path: %s' % expected_path
            print 'Expected args: %s' % expected_args
            print 'Actual url: %s' % fetcher.actual_url

        quoted_params = self.quote_params(expected_args)
        self.assert_expected_url_equals(fetcher.actual_url, expected_path, quoted_params)


    def test_should_call_api_with_correct_url_for_culture_section(self):
        self.check_data_source_url(CultureDataSource(url_capturing_client), '/culture',
                                   show_editors_picks='true',
                                   show_fields=Fields,
                                   page_size='10')


    def test_should_call_api_with_correct_url_for_media_section(self):
        self.check_data_source_url(MediaDataSource(url_capturing_client), '/media',
                                   show_editors_picks='true',
                                   show_fields=Fields,
                                   page_size='10')


    def test_should_call_api_with_correct_url_for_media_monkey(self):
        self.check_data_source_url(MediaMonkeyDataSource(url_capturing_client), '/media/mediamonkeyblog',
                                   show_fields=Fields + ',body',
                                   page_size='10')


    def test_should_call_api_with_correct_url_for_media_comment(self):
        self.check_data_source_url(MediaCommentDataSource(url_capturing_client), '/media',
                                   show_fields=Fields,
                                   tag='tone/comment',
                                   page_size='10')


    def test_should_call_api_with_correct_url_for_sport_section(self):
        self.check_data_source_url(SportDataSource(url_capturing_client), '/sport',
                                   show_editors_picks='true',
                                   show_fields=Fields,
                                   page_size='10')


    def test_should_call_api_with_correct_url_for_most_viewed(self):
        self.check_data_source_url(MostViewedDataSource(url_capturing_client), '/search',
                                   page_size='10',
                                   show_fields=Fields,
                                   show_media='picture',
                                   show_most_viewed='true')

    def test_content_data_source_should_call_api_with_correct_url(self):
        self.check_data_source_url(ContentDataSource(url_capturing_client, 'content_id'), '/content_id', show_fields='trailText,headline,liveBloggingNow,standfirst,commentable,thumbnail,byline')


    def test_should_call_api_with_correct_url_for_pic_of_the_day(self):
        self.check_data_source_url(PicOfDayDataSource(url_capturing_client), '/search',
                                   show_fields=Fields,
                                   page_size='1',
                                   show_media='picture',
                                   tag='artanddesign/series/picture-of-the-day,type/picture')


    def test_should_call_api_with_correct_url_for_eye_witness(self):
        self.check_data_source_url(EyeWitnessDataSource(url_capturing_client), '/search',
                                   show_fields=Fields,
                                   page_size='1',
                                   show_media='picture',
                                   tag='world/series/eyewitness,type/picture')


    def test_should_call_api_with_correct_url_for_music_blog(self):
        self.check_data_source_url(MusicBlogDataSource(url_capturing_client), '/music/musicblog',
                                   show_fields=Fields,
                                   page_size='10')


    def test_should_call_api_with_correct_url_for_music_watch_and_listen(self):
        self.check_data_source_url(MusicWatchListenDataSource(url_capturing_client), '/music',
                                   show_fields=Fields,
                                   tag='type/video|type/audio',
                                   page_size='10')


    def test_should_call_api_with_correct_url_for_business(self):
        self.check_data_source_url(BusinessDataSource(url_capturing_client), '/business',
                                   show_fields=Fields,
                                   show_editors_picks='true',
                                   page_size='10')


    def test_should_call_api_with_correct_url_for_life_and_style(self):
        self.check_data_source_url(LifeAndStyleDataSource(url_capturing_client), '/lifeandstyle',
                                   show_fields=Fields,
                                   show_editors_picks='true',
                                   page_size='10')


    def test_should_call_api_with_correct_url_for_life_and_travel(self):
        self.check_data_source_url(TravelDataSource(url_capturing_client), '/travel',
                                   show_fields=Fields,
                                   show_editors_picks='true',
                                   page_size='10')


    def test_should_call_api_with_correct_url_for_life_and_technology(self):
        self.check_data_source_url(TechnologyDataSource(url_capturing_client), '/technology',
                                   show_fields=Fields,
                                   show_editors_picks='true',
                                   page_size='10')


    def test_should_call_api_with_correct_url_for_music_most_viewed(self):
        self.check_data_source_url(MusicMostViewedDataSource(url_capturing_client), '/music',
                                   show_most_viewed='true',
                                   show_fields=Fields,
                                   page_size='10')


    def test_should_call_api_with_correct_url_for_music_video(self):
        self.check_data_source_url(MusicVideoDataSource(url_capturing_client), '/music',
                                   show_fields=Fields,
                                   page_size='10',
                                   tag='type/video')


    def test_should_call_api_with_correct_url_for_music_editors_picks(self):
        self.check_data_source_url(MusicEditorsPicksDataSource(url_capturing_client), '/music',
                                   show_editors_picks='true',
                                   show_fields=Fields,
                                   page_size='10',
                                   tag='-tone/news')


    def test_should_call_api_with_correct_url_for_music_audio(self):
        self.check_data_source_url(MusicAudioDataSource(url_capturing_client), '/music',
                                   show_fields=Fields,
                                   page_size='10',
                                   tag='type/audio')


    def test_should_call_api_with_correct_url_for_music_news(self):
        self.check_data_source_url(MusicNewsDataSource(url_capturing_client), '/music',
                                   show_fields=Fields,
                                   page_size='10',
                                   tag='tone/news')


    def test_should_call_api_with_correct_url_for_top_stories(self):
        self.check_data_source_url(TopStoriesDataSource(url_capturing_client), '/',
                                   show_fields=Fields,
                                   page_size='10',
                                   show_editors_picks='true')


    def test_a_search_data_source_should_know_how_to_process_response(self):
        fetcher = ApiStubFetcher()
        client = ApiClient('http://somewhere.com/', API_KEY, fetcher)
        data_source = SearchDataSource(client)
        data = data_source.fetch_data()

        assert len(data) == 2
        result = data[1]
        assert result.has_key('id')
        assert result.has_key('apiUrl')
        assert result.has_key('webPublicationDate')
        assert result.has_key('sectionName')
        assert result.has_key('webTitle')
        assert result.has_key('fields')
        assert result.has_key('sectionName')

    def test_a_content_datasource_should_know_how_to_process_response(self):
        # import pdb; pdb.set_trace()
        fetcher = ApiStubFetcher()
        client = ApiClient('http://somewhere.com/', API_KEY, fetcher)
        data_source = ContentDataSource(client, 'i/am/a/short/url')
        data = data_source.fetch_data()

        assert len(data) == 1
        result = data[0]
        assert result['id'] == 'content_1'
        assert result['sectionName'] == 'cif name'
        assert result['sectionId'] == 'cif'
        assert result['webTitle'] == 'Toynbee speaks'
        assert result['fields']['trailText'] == 'Stuff happened'
        assert result['fields']['headline'] == 'More stuff happened'
        assert result['fields']['thumbnail'] == "thumb piano"
        assert result['fields']['standfirst'] == "Stand by your man"
        assert result['fields']['byline'] == "Keith"
        assert result['fields']['liveBloggingNow'] == "false"


    #        assert result.has_key('apiUrl')
#        assert result.has_key('webPublicationDate')
#        assert result.has_key('sectionName')
#        assert result.has_key('webTitle')
#        assert result.has_key('fields')
#        assert result.has_key('sectionName')

        #self.fail("I don't work")


    def test_if_most_viewed_are_included_these_alone_should_be_returned(self):
        class TestMostViwedDataSource(ItemDataSource):
            def __init__(self, client):
                ItemDataSource.__init__(self, client, show_most_viewed=True)

        fetcher = ApiStubFetcher()
        client = ApiClient('http://somewhere.com/', API_KEY, fetcher)
        data_source = TestMostViwedDataSource(client)
        data = data_source.fetch_data()
        self.assertEquals(len(data), 2)
        filtered_data = set([result['id'] for result in data])
        self.assertEquals(filtered_data, set(["uk/2012/dec/18/antarctic-territory-queen-cabinet",
                                              "world/2012/dec/17/white-house-obama-gun-control-newtown"]))


    def test_it_is_an_error_to_ask_for_both_editors_picks_and_most_viewed(self):
        class FaultyClass(ItemDataSource):
            def __init__(self, client):
                ItemDataSource.__init__(self, client, show_editors_picks=True, show_most_viewed=True)
        try:
            badSource = FaultyClass(None)
        except DataSourceException:
            pass
        else:
            self.fail('Turning on both editors_picks and most_viewed should throw an Exception')


    def test_an_editors_picks_data_source_should_know_how_to_process_response(self):
        class TestEditorsPicksDataSource(ItemDataSource):
            def __init__(self, client):
                ItemDataSource.__init__(self, client, show_editors_picks=True)

        fetcher = ApiStubFetcher()
        client = ApiClient('http://somewhere.com/', API_KEY, fetcher)
        data_source = TestEditorsPicksDataSource(client)
        data = data_source.fetch_data()
        assert len(data) == 4
        result = data[2]
        assert result.has_key('id')
        assert result.has_key('apiUrl')
        assert result.has_key('webPublicationDate')
        assert result.has_key('sectionName')
        assert result.has_key('webTitle')
        assert result.has_key('fields')
        assert result.has_key('sectionName')

        result = data[3]
        assert result['id'] == 'sport/video/2013/jan/09/relay-runners-start-brawl-video'


    def test_an_editors_picks_data_source_should_should_not_barf_if_there_are_no_normal_results_in_the_response(self):
        fetcher = ApiStubFetcher()
        client = ApiClient('http://somewhere.com/', API_KEY, fetcher)
        data_source = SportDataSource(client)
        data = data_source.fetch_data()
        assert len(data) == 1


    def test_fetch_all_should_retrieve_data_for_each_data_source_and_return_a_map_indexed_as_input_map(self):
        class StubDataSource1:
            def fetch_data(self):
                return 'stub data 1'

        class StubDataSource2:
            def fetch_data(self):
                return 'stub data 2'


        data_source_map = {'cheese': StubDataSource1(), 'pickle': StubDataSource2()}
        retrieved_data = fetch_all(data_source_map)

        assert len(retrieved_data.keys()) == 2
        assert retrieved_data['cheese'] == 'stub data 1'
        assert retrieved_data['pickle'] == 'stub data 2'


if __name__ == '__main__':
    unittest2.main()
