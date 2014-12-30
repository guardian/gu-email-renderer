import random
import logging
import json

from functools import wraps
from google.appengine.ext import db

class CachedData(db.Model):
    data = db.TextProperty()


def perma_cache_stub(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return f(*args, **kwargs)

    return wrapper


def perma_cache(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        data_source = args[0]
        cache_key = repr(data_source)
        try:
            retrieved_data = f(*args, **kwargs)
            store_in_db(cache_key, retrieved_data)
            logging.debug('Stored data for %s' % cache_key)
        except Exception, ex:
            logging.error(ex)
        finally:
            data = load_from_db(cache_key)
            logging.debug('Read data for %s' % cache_key)

            return data

    return wrapper


def store_in_db(cache_key, data):
    key = db.Key.from_path("CachedData", cache_key)
    cached_data = CachedData.get_or_insert(key.name())

    data_string = json.dumps(data)

    cached_data.data = data_string
    cached_data.put()


def load_from_db(cache_key):
    key = db.Key.from_path("CachedData", cache_key)
    data_string = CachedData.get(key).data
    return json.loads(data_string)
