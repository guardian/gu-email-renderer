from data_source import ItemDataSource

class UK(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, 'uk/sport', show_editors_picks=True)
