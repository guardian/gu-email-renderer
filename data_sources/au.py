from data_source import ItemDataSource

class AusCultureBlogDataSource(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, 'culture/australia-culture-blog')


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

class AusVideoDataSource(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, 'video', show_editors_picks=True)
        self.tags = ['(sport/australia-sport|australia-news/australian-politics|lifeandstyle/australia-food-blog|culture/australia-culture-blog|sport/series/guardian-australia-sports-highlights)']
