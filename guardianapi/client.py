import logging
try:
    import simplejson
except ImportError:
    from django.utils import simplejson
import urllib, urlparse
import fetchers

class Client(object):
    # TODO: which one is it? Get it from a config object



    def __init__(self, base_url, api_key, fetcher=None):
        self.base_url = base_url
        self.api_key = api_key
        self.fetcher = fetcher
        if not self.fetcher:
            self.fetcher = fetchers.best_fetcher()

    def _do_call(self, endpoint, **kwargs):
        fixed_kwargs = self._fix_kwargs(kwargs)

        url = '%s?%s' % (
            urlparse.urljoin(self.base_url, endpoint),
            urllib.urlencode(fixed_kwargs),
        )

        headers, response = self.fetcher.get(url)
        logging.info('Retrieved url: %s. Headers: %s' % (url, headers))

        return simplejson.loads(response)

    def _fix_kwargs(self, kwargs):
        fixed_kwargs = {'format': 'json', 'api-key': self.api_key}

        for key in kwargs.keys():
            fixed_key = key.replace('_', '-')
            fixed_kwargs[fixed_key] = kwargs[key]

        return fixed_kwargs

    def search(self, **kwargs):
        json = self._do_call('search', **kwargs)
        return json['response']['results']

    def editors_picks(self, **kwargs):
        kwargs['show-editors-picks'] = 'true'
        json = self._do_call('', **kwargs)
        return json['response']['editorsPicks']

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.base_url)



