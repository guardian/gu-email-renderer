
from data_source import ItemDataSource

import clients

class Headlines(ItemDataSource):
    def __init__(self, client, edition_path):
        ItemDataSource.__init__(self, client, content_id=edition_path, show_editors_picks=True)

edition_headlines = {
	'uk': Headlines(clients.client, 'uk'),
	'us': Headlines(clients.client, 'us'),
	'au': Headlines(clients.client, 'au')
}

def for_edition(edition):
	return edition_headlines.get(edition, edition_headlines['uk'])
