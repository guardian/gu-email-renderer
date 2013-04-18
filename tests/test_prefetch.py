import unittest2

from prefetch import perma_cache
from google.appengine.ext import db
from google.appengine.ext import testbed
from prefetch import CachedData
from django.utils import simplejson as json


class MockDataSource:
    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return self.id



class TestPrefetch(unittest2.TestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()

    def test_permacache_should_always_write_returned_to_db(self):
        def data_source_fetch_data(data_source):
            return [{'data': 1}, {'data': 2}]

        cache_key = '23421'
        data_source = MockDataSource(cache_key)
        data_returned_from_fetch_all = perma_cache(data_source_fetch_data)(data_source)

        key = db.Key.from_path("CachedData", cache_key)
        data_from_database = CachedData.get(key).data
        data_from_database_rehydrated = json.loads(data_from_database)
        self.assertEquals(data_from_database_rehydrated, data_returned_from_fetch_all)
