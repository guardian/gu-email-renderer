import logging
import json
import urllib
import traceback

from google.appengine.api import urlfetch
from google.appengine.api import memcache

import pysistence as immutable

import defaults
import configuration

default_params = immutable.make_dict({
	'show-fields': ",".join(defaults.content_item_fields),
	'api-key': configuration.read('CAPI_KEY')
	})

def for_id(container_id):
	return ContainerDataSource(container_id)

def read_capi_item(internal_id):
	capi_base_url = configuration.read('CAPI_BASE_URL')

	item_url = "{0}/{1}?{2}".format(capi_base_url, internal_id, urllib.urlencode(default_params))
	#logging.info(item_url)
	
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

class ContainerDataSource:
	def __init__(self, container_id):
		self.container_id = container_id

	def fetch_data(self):
		container_base_url = configuration.read('CONTAINER_API_BASE_URL')
		try:
			url = "{0}/{1}".format(container_base_url, self.container_id)
			
			result = urlfetch.fetch(url, deadline=9)
			if result.status_code == 200:
				data = json.loads(result.content)
				live_stories = data.get('collection', {}).get('live', [])
				live_story_ids = [item['id'] for item in live_stories]
				
				return [read_capi_item(item_id) for item_id in live_story_ids]

			return []

		except Exception as e:
			logging.warn('Container API call failed {0}'.format(e))
			logging.warn(traceback.format_exc())

		return []