from data_source import ItemDataSource

class SportUSDataSource(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, 'us/sport', show_editors_picks=True)

class USMoneyDataSource(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, content_id='us/money', show_editors_picks=True)


