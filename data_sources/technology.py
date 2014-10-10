from data_source import DataSource, ItemDataSource, SearchDataSource


class TechnologyDataSource(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, 'technology', show_editors_picks=True)
        self.name = 'technology' + client.edition

    def __repr__(self):
        return str(self.__class__) + self.name

class TechnologyMostViewedDataSource(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, section='technology', show_most_viewed=True)


class TechnologyBlogDataSource(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, section='technology')
        self.tags = ['(technology/blog|technology/appsblog)']


class TechnologyGamesDataSource(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, section='technology/games')
        self.tags = ['-technology/series/chatterbox,-type/video']


class TechnologyPodcastDataSource(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, section='technology')
        self.tags = ['type/podcast']


class TechnologyVideoDataSource(SearchDataSource):
    def __init__(self, client):
        DataSource.__init__(self, client)
        self.content_type = 'video'
        self.section = 'technology'
        # self.page_size = 1
        self.show_elements = 'video'

