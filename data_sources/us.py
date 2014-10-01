from data_source import ItemDataSource

class SportUSDataSource(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, 'sport/us-sport', show_editors_picks=True)

class USMoneyDataSource(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, section='money/us-personal-finance')


