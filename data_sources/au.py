from data_source import ItemDataSource, SearchDataSource

class AusCultureBlogDataSource(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, 'au/culture', show_editors_picks=True)

class SportDataSource(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, 'au/sport', show_editors_picks=True)

class AusFoodBlogDataSource(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, "lifeandstyle/australia-food-blog")

class AusCommentIsFreeDataSource(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, '/au/commentisfree', show_editors_picks=True, only_editors_picks=True)

class AustralianPoliticsDataSource(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, section='australia-news/australian-politics')

class AustralianPoliticsVideoDataSource(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, section='australia-news/australian-politics')
        self.tags = ['type/video']

class AusVideoDataSource(SearchDataSource):
    def __init__(self, client):
        SearchDataSource.__init__(self, client)
        self.tags = ['type/video,australia-news/australia-news']

