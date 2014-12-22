from data_source import DataSource, ItemDataSource, SearchDataSource

class BooksEditorsPicks(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, content_id='books', show_editors_picks=True)

class BookReviews(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, content_id='books')
        self.tags = ['tone/reviews']

class BooksBlog(ItemDataSource):
	def __init__(self, client):
		ItemDataSource.__init__(self, client, content_id='books/booksblog')