import logging
import os
import json

import urllib, urlparse
import fetchers

class ApiClient(object):

    def __init__(self, base_url, api_key, fetcher=None, edition=''):
        self.base_url = base_url
        self.api_key = api_key
        self.edition = edition
        self.fetcher = fetcher
        if not self.fetcher:
            self.fetcher = fetchers.best_fetcher()

    def _do_call(self, endpoint, **kwargs):
        fixed_kwargs = self._fix_kwargs(kwargs)

        url = '{0}?{1}'.format(
            urlparse.urljoin(self.base_url, endpoint),
            urllib.urlencode(fixed_kwargs)
        )

        #logging.info('Requesting url: {0}'.format(url))

        headers, response = self.fetcher.get(url)

        if not response:
            return {}
        #logging.info('Retrieved url: %s. Headers: %s' % (url, headers))
        return json.loads(response)

    def _fix_kwargs(self, kwargs):
        fixed_kwargs = {'format': 'json', 'api-key': self.api_key}

        for key in kwargs.keys():
            fixed_key = key.replace('_', '-')
            fixed_kwargs[fixed_key] = kwargs[key]

        return fixed_kwargs

    def search_query(self, **kwargs):
        json = self._do_call('search', **kwargs)
        return json['response']['results']

    def item_query(self, content_id='', show_editors_picks=False, show_most_viewed=False, only_editors_picks=False, **kwargs):
        if show_editors_picks:
            kwargs['show-editors-picks'] = 'true'
        if show_most_viewed:
            kwargs['show_most_viewed'] = 'true'
        if self.edition:
            kwargs['edition'] = self.edition

        json = self._do_call(content_id, **kwargs)

        if not 'response' in json:
            logging.warning('Item query did not send expected response')
            logging.warning(json)

        results = []
        if json['response'].has_key('results'):
            results = json['response']['results']

        if show_editors_picks:
            editors_picks = json['response']['editorsPicks']
        else:
            editors_picks = []

        if show_most_viewed:
            return json['response']['mostViewed']

        if only_editors_picks:
            return editors_picks
        
        return editors_picks + results


    def content_query(self, content_id, **kwargs):
        json = self._do_call(content_id, **kwargs)

        results = []
        if 'response' in json and json['response'].has_key('content'):
            results = [json['response']['content']]

        return results

    def __repr__(self):
        return '<%s: %s-%s>' % (self.__class__.__name__, self.base_url)
