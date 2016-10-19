import unittest
import webapp2
from handlers import EmailTemplate
from webob.exc import HTTPNotFound


class Mock(object):
    def __getattr__(self, name): return lambda *args: args

class MockResponse(object):
    out = Mock()

class MockCache(object):
    def __init__(self):
        self.data = {}

    def add(self, key, page, time):
        self.data[key] = page

    def get(self, key):
        if self.data.has_key(key):
            return self.data[key]

class MockAdFetcher(object):
    def leaderboard(self):
        return {}


class MockTemplate(object):
    def __init__(self, template_name):
        self.template_name = template_name

    def render(self, ads, date, **trail_blocks):
        return self.template_name


class MockDataSource(object):
    def __init__(self):
        self.data_fetched = False

    def fetch_data(self):
        self.data_fetched = True
        return [{'id': i} for i in range(20)]
    
    def fetch_title_override(self):
        return None


class TestRenderer(EmailTemplate):

    def __init__(self):
        self.response = MockResponse()
        self.cache = MockCache()
        self.ad_fetcher = MockAdFetcher()
        self.recognized_versions = ['v1', 'v2']

    data_sources = {}
    data_sources['v1'] = {'data_source_1': MockDataSource(), 'data_source_2': MockDataSource()}
    data_sources['v2'] = {'data_source_3': MockDataSource()}

    priority_list = {}
    priority_list['v1'] = [('data_source_1', 2), ('data_source_2', 2)]
    priority_list['v2'] = [('data_source_3', 4)]

    ad_tag = ''
    ad_config = {}

    template_names = {'v1': 'template_1', 'v2': 'template_2'}

    def resolve_template(self, template_name):
        return MockTemplate(template_name)


class TestMailRenderer(unittest.TestCase):
    def test_should_use_data_sources_appropriate_to_version(self):
        renderer = TestRenderer()
        renderer.get('v2')

        for data_source in renderer.data_sources['v1'].values():
            self.assertFalse(data_source.data_fetched)
        for data_source in renderer.data_sources['v2'].values():
            self.assertTrue(data_source.data_fetched)

    def test_should_use_template_appropriate_to_version(self):
        renderer = TestRenderer()
        renderer.get('v2')
        self.assertTrue(len(renderer.cache.data) == 1)
        self.assertEquals(renderer.cache.data.values()[0], 'template_2.html')


    def test_should_throw_404_if_invoked_with_unrecognized_version(self):
        renderer = TestRenderer()
        try:
            renderer.get('v3')
        except HTTPNotFound:
            pass
        except Exception, e:
            self.fail('Unexpected exception: %s' % e)
        else:
            self.fail('Should have thrown HTTPNotFound')
