from google.appengine.api import urlfetch

def for_id(container_id):
	return ContainerDataSource(container_id)

class ContainerDataSource:
	def __init__(self, container_id):
		self.container_id = container_id

	def fetch_data(self):
		return []