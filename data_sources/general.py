
from clients import client
import data_source

class ItemDataSource(data_source.ItemDataSource):
	def __init__(self, content_id,
		production_office=None,
		tags=None,
		show_most_viewed=False,
		show_editors_picks=False):

		data_source.ItemDataSource.__init__(self, client,
			content_id=content_id,
			show_most_viewed=show_most_viewed,
			show_editors_picks=show_editors_picks)

		if production_office:
			self.production_office = production_office

		if tags:
			self.tags = tags
