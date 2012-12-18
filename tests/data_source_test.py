#! /usr/bin/python

import sys
import urllib
from urllib2 import urlparse
from data_source import CultureDataSource, SportDataSource, MostViewedDataSource, PicOfDayDataSource, TopStoriesDataSource
from guardianapi.client import Client
from datetime import datetime

#API_KEY = 'dummy_api_key'
API_KEY = '***REMOVED***'
Fields = 'trailText,headline,liveBloggingNow,standfirst,commentable,thumbnail,byline'

class UrlCheckingStubFetcher:
    def __init__(self, expected_path, **expected_args):
        self.expected_path = expected_path
        self.expected_args = self._quote_params(expected_args)

    def assert_expected_url_equals(self, actual_url):
        (scheme, netloc, path, params, query, fragment) = urlparse.urlparse(actual_url)
        actual_args = dict([arg.split('=') for arg in query.split('&')])

        assert len(actual_args) == len(self.expected_args), 'actual: %d, expected: %d' \
            % (len(actual_args), len(self.expected_args))
        for key in actual_args:
            actual_arg = actual_args[key]
            expected_arg = self.expected_args[key]
            assert actual_arg == expected_arg, 'actual: %s, expected: %s' % (actual_arg, expected_arg)

        assert self.expected_path == path

    def get(self, url):
        print 'Url is: %s' % url
        self.assert_expected_url_equals(url)
        return (None, '{"response": {"results": []}}')

    def _quote_params(self, query_params):
        quoted_params = {}
        for key in query_params.keys():
            new_key = key.replace('_', '-')
            new_value = urllib.quote_plus(query_params[key])
            quoted_params[new_key] = new_value
        return quoted_params


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
                           from_date=from_date,
                           show_most_viewed='true')


def test_should_call_api_with_correct_url_for_pic_of_the_day():
    _check_data_source_url(PicOfDayDataSource(), '/search',
                           show_fields=Fields,
                           page_size='1',
                           show_media='picture',
                           tag='artanddesign/series/picture-of-the-day,type/picture')


def test_should_call_api_with_correct_url_for_top_stories():
    _check_data_source_url(TopStoriesDataSource(), '/',
                           show_fields=Fields,
                           page_size='10',
                           show_editors_picks='true',
                           tag='type/article',
                           section='uk|world')



def _check_data_source_url(data_source, expected_path, **expected_args):
    print 'Testing url for %s' % data_source.__class__
    expected_args['api-key'] = API_KEY
    expected_args['format'] = 'json'
    fetcher = UrlCheckingStubFetcher(expected_path, **expected_args)
    client = Client(API_KEY, fetcher)
    data_source.fetch_data(client)


if __name__ == '__main__':
    test_should_call_api_with_correct_url_for_sport_section()
    test_should_call_api_with_correct_url_for_culture_section()
    test_should_call_api_with_correct_url_for_most_viewed()
    test_should_call_api_with_correct_url_for_pic_of_the_day()
    test_should_call_api_with_correct_url_for_top_stories()
