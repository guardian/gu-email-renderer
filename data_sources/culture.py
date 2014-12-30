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

class BookPodcasts(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, content_id='books')
        self.tags = ['type/audio']

class BooksMostViewed(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, 'books', show_most_viewed=True)

class HowToDraw(SearchDataSource):
    def __init__(self, client):
        DataSource.__init__(self, client)
        self.content_type = 'gallery'
        self.tags = ['childrens-books-site/series/how-to-draw']
        self.show_elements = 'image'