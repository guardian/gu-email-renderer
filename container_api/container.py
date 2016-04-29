import logging
import json
import urllib
import traceback

from google.appengine.api import urlfetch
from google.appengine.api import memcache

import defaults
import configuration
import capi

def for_id(container_id, sort_function=None):
	return ContainerDataSource(container_id, sort_function=sort_function)

def for_front(front_id, metadata=None):
	return FrontDataSource(front_id, metadata)

def read_container(container_id, retries=3, sort_function=None):
	container_base_url = configuration.read('CONTAINER_API_BASE_URL')
	try:
		url = "{0}/{1}".format(container_base_url, container_id)
		
		result = urlfetch.fetch(url, deadline=9)
		if result.status_code == 200:
			data = json.loads(result.content)
			live_stories = data.get('collection', {}).get('live', [])
			live_story_ids = [item['id'] for item in live_stories]
			
			stories = [capi.read_item(item_id) for item_id in live_story_ids]

			if sort_function:
				return sorted(stories, sort_function)

			return stories

		return []

	except Exception as e:
		logging.warn('Container API call failed {0}'.format(e))
		logging.warn(traceback.format_exc())

		if retries > 0:
			return read_container(container_id, retries=retries-1)

	return []

class ContainerDataSource:
	def __init__(self, container_id, sort_function=None):
		self.container_id = container_id
		self.sort_function = sort_function

	def fetch_data(self, retries=3):
		return read_container(self.container_id,
			sort_function=self.sort_function)


class FrontDataSource:
	def __init__(self, front_id, metadata=None):
		self.front_id = front_id
		self.metadata = metadata

	def fetch_data(self, retries=3):
		container_api_host = configuration.read('CONTAINER_API_HOST')
		try:
			url = "http://{host}/list/collections/by/front/{front_id}".format(
				host=container_api_host,
				front_id=self.front_id)

			if self.metadata:
				url = "{url}/and/by/metadata/{metadata}".format(
					url=url,
					metadata=self.metadata)
			
			logging.debug(url)

			result = urlfetch.fetch(url, deadline=9)
			
			if result.status_code == 200:
				data = json.loads(result.content)

				containers = data.get('data', [])
				
				resolved_containers = [read_container(container_id) for container_id in containers]
				#logging.info(resolved_containers)
				stories = [capi_item for container_items in resolved_containers for capi_item in container_items]

				#logging.info(stories)
				return stories

			return []

		except Exception as e:
			logging.warn('Container API call failed {0}'.format(e))
			logging.warn(traceback.format_exc())

			if retries > 0:
				return self.fetch_data(retries=retries-1)

		return []