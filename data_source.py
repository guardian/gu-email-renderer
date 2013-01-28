
class DataSource(object):
    def __init__(self):
        self.fields = ['trailText', 'headline', 'liveBloggingNow', 'standfirst', 'commentable', 'thumbnail', 'byline']
        self.tags = []
        self.page_size = 10
        self.content_type = None
        self.show_media = None
        self.from_date = None
        self.show_most_viewed = False


    def fetch_data(self, client):
        criteria = self._build_criteria()
        data = self._do_call(client, **criteria)
        return list(data)


    def _build_criteria(self):
        criteria = {}

        # Always exclude picture desk due to media problems
        self.tags.append('-news/series/picture-desk-live')

        if self.fields:
            criteria['show-fields'] = ','.join(self.fields)

        if self.content_type:
            self.tags.append('type/%s' % self.content_type)

        if self.tags:
            criteria['tag'] = ','.join(self.tags)

        if self.show_most_viewed:
            criteria['show-most-viewed'] = 'true'

        if self.page_size:
            criteria['page-size'] = self.page_size

        if self.show_media:
            criteria['show-media'] = self.show_media

        if self.from_date:
            criteria['from-date'] = self.from_date

        return criteria


class SearchDataSource(DataSource):
    def _do_call(self, client, **criteria):
        return client.search_query(**criteria)


class ItemDataSource(DataSource):
    def __init__(self, section='', show_editors_picks=True):
        DataSource.__init__(self)
        self.section = section
        self.show_editors_picks = show_editors_picks

    def _do_call(self, client, **criteria):
        return client.item_query(self.section, self.show_editors_picks, **criteria)


class CultureDataSource(ItemDataSource):
    def __init__(self):
        ItemDataSource.__init__(self, 'culture')


class SportDataSource(ItemDataSource):
    def __init__(self):
        ItemDataSource.__init__(self, 'sport')


class MediaDataSource(ItemDataSource):
    def __init__(self):
        ItemDataSource.__init__(self, 'media')


class MediaMonkeyDataSource(ItemDataSource):
    def __init__(self):
        ItemDataSource.__init__(self, section='media/mediamonkeyblog', show_editors_picks=False)
        self.fields.append('body')


# TODO: force this thing to have trailblock
class MediaCommentDataSource(ItemDataSource):
    def __init__(self):
        ItemDataSource.__init__(self, section='media', show_editors_picks=False)
        self.tags = ['tone/comment']


class PicOfDayDataSource(SearchDataSource):
    def __init__(self):
        DataSource.__init__(self)
        self.content_type = 'picture'
        self.tags = ['artanddesign/series/picture-of-the-day']
        self.page_size = 1
        self.show_media = 'picture'


class EyeWitnessDataSource(SearchDataSource):
    def __init__(self):
        DataSource.__init__(self)
        self.content_type = 'picture'
        self.tags = ['world/series/eyewitness']
        self.page_size = 1
        self.show_media = 'picture'


class MostViewedDataSource(SearchDataSource):
    def __init__(self):
        DataSource.__init__(self)
        self.show_media = 'picture'
        self.show_most_viewed = True


class TopStoriesDataSource(ItemDataSource):
    pass


def build_unique_trailblocks(_, data, priority_list):
    """
    data is a map of type string->list list is a list of maps each of
    which contains the field 'id'.  priority_list is a list of pairs:
    (name, number). <name> is the is a key in data (the name of a
    datasource) and <number> is the number of items to take from the
    datasource.
    """

    items_seen_so_far = set()
    unique_subsets = {}

    for (data_set_name, size) in priority_list:
        unique_subset = []
        unique_subsets[data_set_name] = unique_subset
        source_data = data[data_set_name]
        for item in source_data:
            if item['id'] not in items_seen_so_far and len(unique_subset) < size:
                unique_subset.append(item)
                items_seen_so_far.add(item['id'])

    return unique_subsets


def fetch_all(client, data_sources):
    """
    data is a map of type string->data_source.
    return a map with same keys as data, and retrieved data as values
    """
    retrieved_data_map = {}
    for key in data_sources.keys():
        retrieved_data = data_sources[key].fetch_data(client)
        retrieved_data_map[key] = retrieved_data

    return retrieved_data_map
