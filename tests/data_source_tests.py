#! /usr/bin/python

from data_source import \
    CultureDataSource, SportDataSource, MostViewedDataSource, \
    PicOfDayDataSource, TopStoriesDataSource, SearchDataSource, \
    MediaDataSource, MediaCommentDataSource, MediaMonkeyDataSource, \
    ItemDataSource, EyeWitnessDataSource, MusicBlogDataSource, MusicNewsDataSource, \
    MusicVideoDataSource, MusicAudioDataSource, MusicEditorsPicksDataSource, MusicMostViewedDataSource, \
    fetch_all
from guardianapi.client import Client
from datetime import datetime
from test_fetchers import ApiStubFetcher, UrlCheckingFetcher

API_KEY = '***REMOVED***'
Fields = 'trailText,headline,liveBloggingNow,standfirst,commentable,thumbnail,byline'


def test_should_call_api_with_correct_url_for_culture_section():
    _check_data_source_url(CultureDataSource(), '/culture',
                           show_editors_picks='true',
                           show_fields=Fields,
                           page_size='10')


def test_should_call_api_with_correct_url_for_media_section():
    _check_data_source_url(MediaDataSource(), '/media',
                           show_editors_picks='true',
                           show_fields=Fields,
                           page_size='10')

def test_should_call_api_with_correct_url_for_media_monkey():
    _check_data_source_url(MediaMonkeyDataSource(), '/media/mediamonkeyblog',
                           show_fields=Fields + ',body',
                           page_size='10')


def test_should_call_api_with_correct_url_for_media_comment():
    _check_data_source_url(MediaCommentDataSource(), '/media',
                           show_fields=Fields,
                           tag='tone/comment',
                           page_size='10')


def test_should_call_api_with_correct_url_for_sport_section():
    _check_data_source_url(SportDataSource(), '/sport',
                           show_editors_picks='true',
                           show_fields=Fields,
                           page_size='10')


def test_should_call_api_with_correct_url_for_most_viewed():
    now = datetime.now()
    from_date = '%4d-%2d-%2d' % (now.year, now.month, now.day)

    _check_data_source_url(MostViewedDataSource(), '/search',
                           page_size='10',
                           show_fields=Fields,
                           show_media='picture',
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


def test_should_call_api_with_correct_url_for_music_blog():
    _check_data_source_url(MusicBlogDataSource(), '/music/musicblog',
                           show_fields=Fields,
                           page_size='10')


def test_should_call_api_with_correct_url_for_music_most_viewed():
    _check_data_source_url(MusicBlogDataSource(), '/music',
                           show_fields=Fields,
                           show_most_viewed='true',
                           page_size='10')


def test_should_call_api_with_correct_url_for_music_video():
    _check_data_source_url(MusicVideoDataSource(), '/music',
                           show_fields=Fields,
                           page_size='10',
                           tag='type/video')


def test_should_call_api_with_correct_url_for_music_editors_picks():
    _check_data_source_url(MusicEditorsPicksDataSource(), '/music',
                           show_editors_picks='true',
                           show_fields=Fields,
                           page_size='10',
                           tag='-tone/news')


def test_should_call_api_with_correct_url_for_music_audio():
    _check_data_source_url(MusicAudioDataSource(), '/music',
                           show_fields=Fields,
                           page_size='10',
                           tag='type/audio')


def test_should_call_api_with_correct_url_for_music_news():
    _check_data_source_url(MusicNewsDataSource(), '/music',
                           show_fields=Fields,
                           page_size='10',
                           tag='tone/news')


def test_should_call_api_with_correct_url_for_top_stories():
    _check_data_source_url(TopStoriesDataSource(), '/',
                           show_fields=Fields,
                           page_size='10',
                           show_editors_picks='true')


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


def test_if_most_viewed_are_included_these_alone_should_be_returned():
    pass

def test_it_is_an_error_to_ask_for_both_editors_picks_and_most_viewed():
    class FaultyClass(ItemDataSource):
        pass


def test_an_editors_picks_data_source_should_know_how_to_process_response():
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
    # non-editors' picks results should be appended at end
    result = data[3]
    assert result['id'] == 'sport/video/2013/jan/09/relay-runners-start-brawl-video'


def test_an_editors_picks_data_source_should_should_not_barf_if_there_are_no_normal_results_in_the_response():
    fetcher = ApiStubFetcher()
    client = Client('http://somewhere.com/', API_KEY, fetcher)
    data_source = SportDataSource()
    data = data_source.fetch_data(client)
    assert len(data) == 1


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

    if not expected_args.has_key('tag'):
        expected_args['tag'] = '-news/series/picture-desk-live'
    else:
        expected_args['tag'] += ',-news/series/picture-desk-live'

    fetcher = UrlCheckingFetcher(expected_path, **expected_args)
    client = Client('http://content.guardianapis.com/', API_KEY, fetcher)
    data_source.fetch_data(client)


if __name__ == '__main__':
    test_should_call_api_with_correct_url_for_sport_section()
    test_should_call_api_with_correct_url_for_culture_section()
    test_should_call_api_with_correct_url_for_most_viewed()
    test_should_call_api_with_correct_url_for_pic_of_the_day()
    test_should_call_api_with_correct_url_for_top_stories()
    test_should_call_api_with_correct_url_for_eye_witness()
    test_should_call_api_with_correct_url_for_media_section()
    test_should_call_api_with_correct_url_for_media_comment()
    test_should_call_api_with_correct_url_for_media_monkey()
    test_should_call_api_with_correct_url_for_music_blog()
    test_should_call_api_with_correct_url_for_music_news()
    test_should_call_api_with_correct_url_for_music_video()
    test_should_call_api_with_correct_url_for_music_audio()
    test_should_call_api_with_correct_url_for_music_editors_picks()

    test_if_most_viewed_are_included_these_alone_should_be_returned()
    test_it_is_an_error_to_ask_for_both_editors_picks_and_most_viewed()
    test_a_search_data_source_should_know_how_to_process_response()
    test_an_editors_picks_data_source_should_know_how_to_process_response()
    test_an_editors_picks_data_source_should_should_not_barf_if_there_are_no_normal_results_in_the_response()
    test_fetch_all_should_retrieve_data_for_each_data_source_and_return_a_map_indexed_as_input_map()
