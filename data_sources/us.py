from data_source import ItemDataSource

class SportUSDataSource(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, 'us/sport', show_editors_picks=True)
        self.show_tags = ['keyword']
        self.show_elements = 'image'