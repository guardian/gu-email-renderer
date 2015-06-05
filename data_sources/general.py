
from mail_renderer import client
import data_source

class ItemDataSource(data_source.ItemDataSource):
	def __init__(self, content_id, production_office=None, show_most_viewed=False):
		data_source.ItemDataSource.__init__(self, client, content_id=content_id, show_most_viewed=show_most_viewed)

		if production_office:
			self.production_office = production_office
