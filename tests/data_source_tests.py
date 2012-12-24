#! /usr/bin/python

from data_source import \
    CultureDataSource, SportDataSource, MostViewedDataSource, \
    PicOfDayDataSource, TopStoriesDataSource, SearchDataSource, EditorsPicksDataSource, EyeWitnessDataSource, fetch_all
from guardianapi.client import Client
from datetime import datetime
from test_fetchers import ApiStubFetcher, UrlCheckingFetcher

API_KEY = '***REMOVED***'
Fields = 'trailText,headline,liveBloggingNow,standfirst,commentable,thumbnail,byline'


def test_should_call_api_with_correct_url_for_culture_section():
    _check_data_source_url(CultureDataSource(), '/search',
                           section='culture',
                           show_fields=Fields,
                           page_size='10',
                           tag='type/article')


def test_should_call_api_with_correct_url_for_sport_section():
    _check_data_source_url(SportDataSource(), '/search',
                           section='sport',
                           show_fields=Fields,
                           page_size='10',
                           tag='type/article')


def test_should_call_api_with_correct_url_for_most_viewed():
    now = datetime.now()
    from_date = '%4d-%2d-%2d' % (now.year, now.month, now.day)

    _check_data_source_url(MostViewedDataSource(), '/search',
                           page_size='10',
                           tag='type/article',
                           show_fields=Fields,
                           #from_date=from_date,
                           show_most_viewed='true')


def test_should_call_api_with_correct_url_for_pic_of_the_day():
    _check_data_source_url(PicOfDayDataSource(), '/search',
        show_fields=Fields,
        page_size='1',
        show_media='picture',
        tag='artanddesign/series/picture-of-the-day,type/picture')


def test_should_call_api_with_correct_url_for_eye_witness():
    _check_data_source_url(EyeWitnessDataSource(), '/search',
        show_fields=Fields,
        page_size='1',
        show_media='picture',
        tag='world/series/eyewitness,type/picture')


def test_should_call_api_with_correct_url_for_top_stories():
    _check_data_source_url(TopStoriesDataSource(), '/',
                           show_fields=Fields,
                           page_size='10',
                           show_editors_picks='true',
                           tag='type/article')


def test_a_search_data_source_should_know_how_to_process_response():
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


def test_an_editors_picks_data_source_should_know_how_to_process_response():
    fetcher = ApiStubFetcher()
    client = Client('http://somewhere.com/', API_KEY, fetcher)
    data_source = EditorsPicksDataSource()
    data = data_source.fetch_data(client)
    assert len(data) == 3
    result = data[2]
    assert result.has_key('id')
    assert result.has_key('apiUrl')
    assert result.has_key('webPublicationDate')
    assert result.has_key('sectionName')
    assert result.has_key('webTitle')
    assert result.has_key('fields')
    assert result.has_key('sectionName')


def test_fetch_all_should_retrieve_data_for_each_data_source_and_return_a_map_indexed_as_input_map():
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


def _check_data_source_url(data_source, expected_path, **expected_args):
    print 'Testing url for %s' % data_source.__class__
    expected_args['api-key'] = API_KEY
    expected_args['format'] = 'json'
    fetcher = UrlCheckingFetcher(expected_path, **expected_args)
    client = Client('http://somewhere.com/', API_KEY, fetcher)
    data_source.fetch_data(client)


if __name__ == '__main__':
    test_should_call_api_with_correct_url_for_sport_section()
    test_should_call_api_with_correct_url_for_culture_section()
    test_should_call_api_with_correct_url_for_most_viewed()
    test_should_call_api_with_correct_url_for_pic_of_the_day()
    test_should_call_api_with_correct_url_for_top_stories()
    test_should_call_api_with_correct_url_for_eye_witness()
    test_a_search_data_source_should_know_how_to_process_response()
    test_an_editors_picks_data_source_should_know_how_to_process_response()
    test_fetch_all_should_retrieve_data_for_each_data_source_and_return_a_map_indexed_as_input_map()


