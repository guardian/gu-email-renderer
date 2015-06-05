
from mail_renderer import client
import data_source

class ItemDataSource(data_source.ItemDataSource):
	def __init__(self, content_id, production_office=None):
		data_source.ItemDataSource.__init__(self, client, content_id=content_id, show_most_viewed=True)

		if production_office:
			self.production_office = production_office
