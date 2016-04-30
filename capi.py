import json
import urllib
import logging

from google.appengine.api import urlfetch
from google.appengine.api import memcache

import pysistence as immutable

import defaults
import configuration


default_params = immutable.make_dict({
	'show-fields': ",".join(defaults.content_item_fields),
	'api-key': configuration.read('CAPI_KEY')
	})

def read_item(internal_id, additional_params=None):
	capi_base_url = configuration.read('CAPI_BASE_URL')

	combined_params = default_params

	if additional_params:
		combined_params = default_params.using(**additional_params)

	item_url = "{0}/{1}?{2}".format(capi_base_url, internal_id, urllib.urlencode(combined_params))
	logging.info(item_url)
	
	cached_response = memcache.get(item_url)

	if cached_response:
		return cached_response

	
	result = urlfetch.fetch(item_url, deadline=8)

	if result.status_code == 200:
		data = json.loads(result.content)
		item_data = data.get('response', {}).get('content', {})

		if len(result.content) < defaults.MAX_MEMCACHE_LENGTH:
			memcache.set(item_url, item_data, defaults.CACHE_TIME)
		return item_data

	return None