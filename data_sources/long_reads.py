from data_source import DataSource, ItemDataSource, SearchDataSource

class Reads(SearchDataSource):
    def __init__(self, client):
        DataSource.__init__(self, client)
        self.tags = ['news/series/the-long-read,-tone/audio']

class Audio(ItemDataSource):
	def __init__(self, client):
		ItemDataSource.__init__(self, client, content_id='news/series/the-audio-long-read')