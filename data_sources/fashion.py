from data_source import DataSource, ItemDataSource, SearchDataSource

class FashionEditorsPicksDataSource(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, content_id='fashion', show_editors_picks=True)
        self.page_size = 20


class FashionMostViewedDataSource(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, content_id='fashion', show_most_viewed=True)

class FashionSaliHughesDataSource(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, content_id='fashion')
        self.tags = ['fashion/series/sali-hughes-beauty']

class JCMOnFashion(ItemDataSource):
	def __init__(self, client):
		ItemDataSource.__init__(self, client, content_id='fashion')
		self.tags = ['fashion/series/jess-cartner-morley-on-fashion']

class FashionNewsDataSource(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, content_id='fashion')


class FashionBlogDataSource(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, content_id='fashion/fashion-blog')


class FashionNetworkDataSource(ItemDataSource):
    def __init__(self, client ):
        ItemDataSource.__init__(self, client, content_id='fashion/series/guardian-fashion-blogs-network')


class FashionStylewatchDataSource(SearchDataSource):
    def __init__(self, client):
        DataSource.__init__(self, client)
        self.tags = ['fashion/series/stylewatch']
        # self.page_size = 1
        self.show_elements = 'image'


class FashionGalleryDataSource(SearchDataSource):
    def __init__(self, client):
        DataSource.__init__(self, client)
        self.content_type = 'gallery'
        self.tags = ['(fashion/series/fashion-for-all-ages|fashion/series/key-fashion-trends-of-the-season|fashion/series/fashion-line-up)']
        # self.page_size = 1
        self.show_elements = 'image'


class FashionVideoDataSource(SearchDataSource):
    def __init__(self, client):
        DataSource.__init__(self, client)
        self.content_type = 'video'
        self.tags = ['theguardian/series/how-to-dress']
        # self.page_size = 1
        self.show_elements = 'video'

