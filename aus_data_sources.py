from data_source import ItemDataSource

class AusCultureBlogDataSource(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, 'culture/australia-culture-blog')


class AusFoodBlogDataSource(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, "lifeandstyle/australia-food-blog")


