from data_source import ItemDataSource


class WorldNews(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, content_id='world', show_editors_picks=True)
        self.show_elements = 'image'