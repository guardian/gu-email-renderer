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
    DataSourceException, fetch_all
from guardianapi.client import Client
from datetime import datetime
from test_fetchers import ApiStubFetcher

API_KEY = '***REMOVED***'
Fields = 'trailText,headline,liveBloggingNow,standfirst,commentable,thumbnail,byline'
DEBUG = False




class UrlCapturingFetcher():
    def get(self, url):
        self.actual_url = url
        return (None, '{"response": {"results": [], "editorsPicks": [], "mostViewed": []}}')


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

        fetcher = UrlCapturingFetcher()
        client = Client('http://content.guardianapis.com/', API_KEY, fetcher)
        data_source.fetch_data(client)

        if DEBUG:
            print 'Testing url for %s' % data_source.__class__
            print 'Expected path: %s' % expected_path
            print 'Expected args: %s' % expected_args
            print 'Actual url: %s' % fetcher.actual_url

        quoted_params = self.quote_params(expected_args)
        self.assert_expected_url_equals(fetcher.actual_url, expected_path, quoted_params)


    def test_should_call_api_with_correct_url_for_culture_section(self):
        self.check_data_source_url(CultureDataSource(), '/culture',
                                   show_editors_picks='true',
                                   show_fields=Fields,
                                   page_size='10')


    def test_should_call_api_with_correct_url_for_media_section(self):
        self.check_data_source_url(MediaDataSource(), '/media',
                                   show_editors_picks='true',
                                   show_fields=Fields,
                                   page_size='10')


    def test_should_call_api_with_correct_url_for_media_monkey(self):
        self.check_data_source_url(MediaMonkeyDataSource(), '/media/mediamonkeyblog',
                                   show_fields=Fields + ',body',
                                   page_size='10')


    def test_should_call_api_with_correct_url_for_media_comment(self):
        self.check_data_source_url(MediaCommentDataSource(), '/media',
                                   show_fields=Fields,
                                   tag='tone/comment',
                                   page_size='10')


    def test_should_call_api_with_correct_url_for_sport_section(self):
        self.check_data_source_url(SportDataSource(), '/sport',
                                   show_editors_picks='true',
                                   show_fields=Fields,
                                   page_size='10')


    def test_should_call_api_with_correct_url_for_most_viewed(self):
        self.check_data_source_url(MostViewedDataSource(), '/search',
                                   page_size='10',
                                   show_fields=Fields,
                                   show_media='picture',
                                   show_most_viewed='true')


    def test_should_call_api_with_correct_url_for_pic_of_the_day(self):
        self.check_data_source_url(PicOfDayDataSource(), '/search',
                                   show_fields=Fields,
                                   page_size='1',
                                   show_media='picture',
                                   tag='artanddesign/series/picture-of-the-day,type/picture')


    def test_should_call_api_with_correct_url_for_eye_witness(self):
        self.check_data_source_url(EyeWitnessDataSource(), '/search',
                                   show_fields=Fields,
                                   page_size='1',
                                   show_media='picture',
                                   tag='world/series/eyewitness,type/picture')


    def test_should_call_api_with_correct_url_for_music_blog(self):
        self.check_data_source_url(MusicBlogDataSource(), '/music/musicblog',
                                   show_fields=Fields,
                                   page_size='10')


    def test_should_call_api_with_correct_url_for_music_watch_and_listen(self):
        self.check_data_source_url(MusicWatchListenDataSource(), '/music',
                                   show_fields=Fields,
                                   tag='type/video|type/audio',
                                   page_size='10')


    def test_should_call_api_with_correct_url_for_business(self):
        self.check_data_source_url(BusinessDataSource(), '/business',
                                   show_fields=Fields,
                                   show_editors_picks='true',
                                   page_size='10')


    def test_should_call_api_with_correct_url_for_life_and_style(self):
        self.check_data_source_url(LifeAndStyleDataSource(), '/lifeandstyle',
                                   show_fields=Fields,
                                   show_editors_picks='true',
                                   page_size='10')


    def test_should_call_api_with_correct_url_for_life_and_travel(self):
        self.check_data_source_url(TravelDataSource(), '/travel',
                                   show_fields=Fields,
                                   show_editors_picks='true',
                                   page_size='10')


    def test_should_call_api_with_correct_url_for_life_and_technology(self):
        self.check_data_source_url(TechnologyDataSource(), '/technology',
                                   show_fields=Fields,
                                   show_editors_picks='true',
                                   page_size='10')


    def test_should_call_api_with_correct_url_for_music_most_viewed(self):
        self.check_data_source_url(MusicMostViewedDataSource(), '/music',
                                   show_most_viewed='true',
                                   show_fields=Fields,
                                   page_size='10')


    def test_should_call_api_with_correct_url_for_music_video(self):
        self.check_data_source_url(MusicVideoDataSource(), '/music',
                                   show_fields=Fields,
                                   page_size='10',
                                   tag='type/video')


    def test_should_call_api_with_correct_url_for_music_editors_picks(self):
        self.check_data_source_url(MusicEditorsPicksDataSource(), '/music',
                                   show_editors_picks='true',
                                   show_fields=Fields,
                                   page_size='10',
                                   tag='-tone/news')


    def test_should_call_api_with_correct_url_for_music_audio(self):
        self.check_data_source_url(MusicAudioDataSource(), '/music',
                                   show_fields=Fields,
                                   page_size='10',
                                   tag='type/audio')


    def test_should_call_api_with_correct_url_for_music_news(self):
        self.check_data_source_url(MusicNewsDataSource(), '/music',
                                   show_fields=Fields,
                                   page_size='10',
                                   tag='tone/news')


    def test_should_call_api_with_correct_url_for_top_stories(self):
        self.check_data_source_url(TopStoriesDataSource(), '/',
                                   show_fields=Fields,
                                   page_size='10',
                                   show_editors_picks='true')


    def test_a_search_data_source_should_know_how_to_process_response(self):
        fetcher = ApiStubFetcher()
        client = Client('http://somewhere.com/', API_KEY, fetcher)
        data_source = SearchDataSource()
        data = data_source.fetch_data(client)

        assert len(data) == 2
        result = data[1]
        assert result.has_key('id')
        assert result.has_key('apiUrl')
        assert result.has_key('webPublicationDate')
        assert result.has_key('sectionName')
        assert result.has_key('webTitle')
        assert result.has_key('fields')
        assert result.has_key('sectionName')


    def test_if_most_viewed_are_included_these_alone_should_be_returned(self):
        class TestMostViwedDataSource(ItemDataSource):
            def __init__(self):
                ItemDataSource.__init__(self, show_most_viewed=True)

        fetcher = ApiStubFetcher()
        client = Client('http://somewhere.com/', API_KEY, fetcher)
        data_source = TestMostViwedDataSource()
        data = data_source.fetch_data(client)
        self.assertEquals(len(data), 2)
        filtered_data = set([result['id'] for result in data])
        self.assertEquals(filtered_data, set(["uk/2012/dec/18/antarctic-territory-queen-cabinet",
                                              "world/2012/dec/17/white-house-obama-gun-control-newtown"]))


    def test_it_is_an_error_to_ask_for_both_editors_picks_and_most_viewed(self):
        class FaultyClass(ItemDataSource):
            def __init__(self):
                ItemDataSource.__init__(self, show_editors_picks=True, show_most_viewed=True)
        try:
            badSource = FaultyClass()
        except DataSourceException:
            pass
        else:
            self.fail('Turning on both editors_picks and most_viewed should throw an Exception')


    def test_an_editors_picks_data_source_should_know_how_to_process_response(self):
        class TestEditorsPicksDataSource(ItemDataSource):
            def __init__(self):
                ItemDataSource.__init__(self, show_editors_picks=True)

        fetcher = ApiStubFetcher()
        client = Client('http://somewhere.com/', API_KEY, fetcher)
        data_source = TestEditorsPicksDataSource()
        data = data_source.fetch_data(client)
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
        client = Client('http://somewhere.com/', API_KEY, fetcher)
        data_source = SportDataSource()
        data = data_source.fetch_data(client)
        assert len(data) == 1


    def test_fetch_all_should_retrieve_data_for_each_data_source_and_return_a_map_indexed_as_input_map(self):
        class StubDataSource1:
            def fetch_data(self, client):
                return 'stub data 1'

        class StubDataSource2:
            def fetch_data(self, client):
                return 'stub data 2'


        data_source_map = {'cheese': StubDataSource1(), 'pickle': StubDataSource2()}
        retrieved_data = fetch_all(None, data_source_map)

        assert len(retrieved_data.keys()) == 2
        assert retrieved_data['cheese'] == 'stub data 1'
        assert retrieved_data['pickle'] == 'stub data 2'


    # def _check_data_source_url(data_source, expected_path, **expected_args):
    #     print 'Testing url for %s' % data_source.__class__
    #     expected_args['api-key'] = API_KEY
    #     expected_args['format'] = 'json'

    #     if not expected_args.has_key('tag'):
    #         expected_args['tag'] = '-news/series/picture-desk-live'
    #     else:
    #         expected_args['tag'] += ',-news/series/picture-desk-live'

    #     fetcher = UrlCheckingFetcher(expected_path, **expected_args)
    #     client = Client('http://content.guardianapis.com/', API_KEY, fetcher)
    #     data_source.fetch_data(client)


if __name__ == '__main__':
    unittest2.main()
    # test_should_call_api_with_correct_url_for_sport_section()
    # test_should_call_api_with_correct_url_for_culture_section()
    # test_should_call_api_with_correct_url_for_most_viewed()
    # test_should_call_api_with_correct_url_for_pic_of_the_day()
    # test_should_call_api_with_correct_url_for_top_stories()
    # test_should_call_api_with_correct_url_for_eye_witness()
    # test_should_call_api_with_correct_url_for_media_section()
    # test_should_call_api_with_correct_url_for_media_comment()
    # test_should_call_api_with_correct_url_for_media_monkey()
    # test_should_call_api_with_correct_url_for_music_blog()
    # test_should_call_api_with_correct_url_for_music_news()
    # test_should_call_api_with_correct_url_for_music_video()
    # test_should_call_api_with_correct_url_for_music_audio()
    # test_should_call_api_with_correct_url_for_music_editors_picks()

    # test_if_most_viewed_are_included_these_alone_should_be_returned()
    # test_it_is_an_error_to_ask_for_both_editors_picks_and_most_viewed()
    # test_a_search_data_source_should_know_how_to_process_response()
    # test_an_editors_picks_data_source_should_know_how_to_process_response()
    # test_an_editors_picks_data_source_should_should_not_barf_if_there_are_no_normal_results_in_the_response()
    # test_fetch_all_should_retrieve_data_for_each_data_source_and_return_a_map_indexed_as_input_map()
