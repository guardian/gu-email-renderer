import logging
import os
from urlparse import urlparse

if os.environ.has_key('RUNNING_UNIT_TESTS'):
    from prefetch import perma_cache_stub as perma_cache
else:
    from prefetch import perma_cache

# Always exclude picture desk due to media problems
DEFAULT_TAGS = ['-news/series/picture-desk-live']

class DataSource(object):
    def __init__(self, client):
        self.client = client
        self.tags = []
        self.fields = ['trailText', 'headline', 'liveBloggingNow', 'standfirst', 'commentable', 'thumbnail', 'byline']
        self.page_size = 10
        self.content_type = None
        self.show_media = None
        self.from_date = None
        self.show_most_viewed = False
        self.short_url = None


    def fetch_data(self):
        criteria = self._build_criteria()
        data = self._do_call(**criteria)
        return list(data)


    def _build_criteria(self):
        criteria = {}

        if self.fields:
            criteria['show-fields'] = ','.join(self.fields)

        if self.content_type:
            self.tags.append('type/%s' % self.content_type)

        self.tags += DEFAULT_TAGS
        criteria['tag'] = ','.join(self.tags)

        if self.show_most_viewed:
            criteria['show-most-viewed'] = 'true'

        if self.page_size:
            criteria['page-size'] = self.page_size

        if self.show_media:
            criteria['show-media'] = self.show_media

        if self.from_date:
            criteria['from-date'] = self.from_date

        # TODO: Are we even using this?
        if self.short_url:
            criteria['short_url'] = self.short_url

        criteria['user-tier']='internal'

        return criteria


class CommentCountInterpolator(object):

    def interpolate(self, comment_count_list, content_list):
        def has_path(url, path):
            return urlparse(url).path == path

        for (short_url, comment_count) in comment_count_list:
            [content_item for content_item in content_list
             if has_path(content_item['fields']['shortUrl'], short_url)][0]['comment_count'] = comment_count

        return content_list


class MostCommentedDataSource(DataSource):
    def __init__(self, discussion_fetcher, multi_content_data_source, comment_count_interpolator, n_items=10):
        DataSource.__init__(self, None) # TODO: client is None. Bad?

        self.discussion_fetcher = discussion_fetcher
        self.multi_content_data_source = multi_content_data_source
        self.multi_content_data_source.fields.append('shortUrl')
        self.comment_count_interpolator = comment_count_interpolator
        self.n_items = n_items

    def _do_call(self, **criteria):
        item_count_pairs = self.discussion_fetcher.fetch_most_commented(self.n_items)
        content_ids = [id for (id, count) in item_count_pairs]

        self.multi_content_data_source.content_ids = content_ids
        most_commented_content = self.multi_content_data_source.fetch_data()

        return self.comment_count_interpolator.interpolate(content_list=most_commented_content, comment_count_list=item_count_pairs)


class ItemPlusBlogDataSource(DataSource):

    def __init__(self, content_item_data_source, blog_data_source):
        DataSource.__init__(self, None)
        self.content_item_data_source = content_item_data_source
        self.blog_data_source = blog_data_source

    def _do_call(self, **criteria):
        content_data = self.content_item_data_source.fetch_data()
        blog_data = self.blog_data_source.fetch_data()
        return blog_data[:1] + content_data


class MostSharedCountInterpolator(object):
    def interpolate(self, shared_count_list, content_list ):
        for( url, shared_count ) in shared_count_list:
            [content_item for content_item in content_list
             if url in content_item['webUrl']][0]['share_count'] = shared_count

        return content_list


class MostSharedDataSource(DataSource):

    def __init__(self, multi_content_data_source, most_shared_fetcher, shared_count_interpolator, n_items=10):
        DataSource.__init__(self, None)

        self.multi_content_data_source = multi_content_data_source
        self.most_shared_fetcher = most_shared_fetcher
        self.shared_count_interpolator  = shared_count_interpolator
        self.n_items = n_items


    @perma_cache
    def fetch_data(self):
        # get data from
        # put results in datastore with key made from self.__repr__
        return DataSource.fetch_data(self)

    def _do_call(self, **criteria):

        shared_urls_with_counts = self.most_shared_fetcher.fetch_most_shared()
        #import pdb; pdb.set_trace()
        content_ids = [urlparse(url).path for(url, count) in shared_urls_with_counts]
        self.multi_content_data_source.content_ids = content_ids
        most_shared_comment = self.multi_content_data_source.fetch_data()
        return self.shared_count_interpolator.interpolate(shared_urls_with_counts, most_shared_comment)

    def __repr__(self):
        return os.environ['CURRENT_VERSION_ID'] + "OphanMostSharedData"


class SearchDataSource(DataSource):
    def __init__(self, client):
        DataSource.__init__(self, client)

    def _do_call(self, **criteria):
        return self.client.search_query(**criteria)


class ItemDataSource(DataSource):
    def __init__(self, client, section='', show_editors_picks=False, show_most_viewed=False):
        DataSource.__init__(self, client)
        if show_editors_picks and show_most_viewed:
            raise DataSourceException('Cannot show most_viewed and editors_picks at the same time')
        self.section = section
        self.show_editors_picks = show_editors_picks
        self.show_most_viewed = show_most_viewed

    def _do_call(self, **criteria):
        return self.client.item_query(self.section, self.show_editors_picks, self.show_most_viewed, **criteria)


class MultiContentDataSource(ItemDataSource):
    def __init__(self, client, name):
        ItemDataSource.__init__(self, client)
        self.content_ids = None
        self.name = name

    def _do_call(self, **criteria):
        if not self.content_ids:
            raise DataSourceException("content_ids must be set before calling fetch_data()")

        result = []
        for id in self.content_ids:
            result.extend(self.client.content_query(id, **criteria))
        return result

    def __repr__(self):
        return str(self.__class__) + self.name


class ContentDataSource(ItemDataSource):
    def __init__(self, client, content_id):
        ItemDataSource.__init__(self, client, section=content_id)
        self.page_size = None

    def _do_call(self, **criteria):
        return self.client.content_query(self.section, **criteria)


class CultureDataSource(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, 'culture', show_editors_picks=True)
        self.name = 'culture' + client.edition

    def __repr__(self):
        return str(self.__class__) + self.name


class BusinessDataSource(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, 'business', show_editors_picks=True)
        self.name = 'business' + client.edition

    def __repr__(self):
        return str(self.__class__) + self.name


class CommentIsFreeDataSource(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, 'commentisfree', show_editors_picks=True)
        self.name = 'comment' + client.edition

    def __repr__(self):
        return str(self.__class__) + self.name


class AusCommentIsFreeDataSource(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, 'commentisfree', show_editors_picks=True)
        self.tags = ['world/australia']


class TechnologyDataSource(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, 'technology', show_editors_picks=True)
        self.name = 'technology' + client.edition

    def __repr__(self):
        return str(self.__class__) + self.name


class TravelDataSource(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, 'travel', show_editors_picks=True)


class ScienceDataSource(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, 'science', show_editors_picks=True)


class EnvironmentDataSource(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, 'environment', show_editors_picks=True)


class LifeAndStyleDataSource(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, 'lifeandstyle', show_editors_picks=True)


class SportDataSource(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, 'sport', show_editors_picks=True)


class SportUSDataSource(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, 'sport/us-sport', show_editors_picks=True)


class AusSportDataSource(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, 'sport/australia-sport', show_editors_picks=True)


class MediaDataSource(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, 'media', show_editors_picks=True)


class MediaBlogDataSource(ItemDataSource):
    def __init__(self, client ):
        ItemDataSource.__init__(self, client, section='media/media-blog')


class MediaMonkeyDataSource(ItemDataSource):
    def __init__(self, client ):
        ItemDataSource.__init__(self, client, section='media/mediamonkeyblog')
        self.fields.append('body')


class MediaCommentDataSource(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, section='media')
        self.tags = ['tone/comment']


class MediaBriefingDataSource(ItemDataSource):
    def __init__(self, client ):
        ItemDataSource.__init__(self, client, section='media/series/media-briefing')


class PicOfDayDataSource(SearchDataSource):
    def __init__(self, client):
        DataSource.__init__(self, client)
        self.content_type = 'picture'
        self.tags = ['artanddesign/series/picture-of-the-day']
        self.page_size = 1
        self.show_media = 'picture'


class EyeWitnessDataSource(SearchDataSource):
    def __init__(self, client):
        DataSource.__init__(self, client)
        self.content_type = 'picture'
        self.tags = ['world/series/eyewitness']
        self.page_size = 1
        self.show_media = 'picture'


class MostViewedDataSource(ItemDataSource):
    def __init__(self, client):
        DataSource.__init__(self, client)
        self.show_media = 'picture'
        self.show_most_viewed = True
        self.show_editors_picks = False
        self.section=''
        self.name = 'most_viewed' + client.edition

    def __repr__(self):
        return str(self.__class__) + self.name


class VideoDataSource(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, 'video', show_editors_picks=True)


class AusVideoDataSource(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, 'video', show_editors_picks=True)
        self.tags = ['(world/australia|sport/australia-sport|world/australian-politics|lifeandstyle/australia-food-blog|culture/australia-culture-blog)']


class FashionMostViewedDataSource(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, section='fashion', show_most_viewed=True)


class FashionAskHadleyDataSource(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, section='fashion')
        self.tags = ['fashion/series/ask-hadley']


class FashionNewsDataSource(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, section='fashion')


class FashionBlogDataSource(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, section='fashion/fashion-blog')


class FashionNetworkDataSource(ItemDataSource):
    def __init__(self, client ):
        ItemDataSource.__init__(self, client, section='fashion/series/guardian-fashion-blogs-network')


class FashionGalleryDataSource(SearchDataSource):
    def __init__(self, client):
        DataSource.__init__(self, client)
        self.content_type = 'gallery'
        self.tags = ['(fashion/series/fashion-for-all-ages|fashion/series/key-fashion-trends-of-the-season|fashion/series/fashion-line-up)']
        # self.page_size = 1
        self.show_media = 'picture'


class FashionVideoDataSource(SearchDataSource):
    def __init__(self, client):
        DataSource.__init__(self, client)
        self.content_type = 'video'
        self.tags = ['theguardian/series/how-to-dress']
        # self.page_size = 1
        self.show_media = 'video'


class MusicMostViewedDataSource(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, section='music', show_most_viewed=True)


class MusicEditorsPicksDataSource(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, section='music', show_editors_picks=True)
        self.tags = ['-tone/news']


class MusicNewsDataSource(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, section='music')
        self.tags = ['tone/news']


class MusicVideoDataSource(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, section='music')
        self.tags = ['type/video']

class MusicWatchListenDataSource(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, section='music')
        self.tags = ['type/video|type/audio']


class MusicAudioDataSource(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, section='music')
        self.tags = ['type/audio']


class MusicBlogDataSource(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, section='music/musicblog')


class TopStoriesDataSource(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, show_editors_picks=True)
        self.name = 'top_stories' + client.edition

    def __repr__(self):
        return str(self.__class__) + self.name


class AusTopStoriesDataSource(TopStoriesDataSource):
    def __init__(self, client):
        TopStoriesDataSource.__init__(self,client)
        self.tags = ['world/australia']


class DataSourceException(Exception):
    pass


def build_unique_trailblocks(data, priority_list):
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


# TODO: put me in email-template
def fetch_all(data_sources):
    """
    data is a map of type string->data_source.
    return a map with same keys as data, and retrieved data as values
    """

    #import pdb;pdb.set_trace()
    retrieved_data_map = {}
    for key in data_sources.keys():
        retrieved_data = data_sources[key].fetch_data()
        retrieved_data_map[key] = retrieved_data

    return retrieved_data_map
