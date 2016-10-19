import logging
import os
from urlparse import urlparse

import pysistence as immutable

if os.environ.has_key('RUNNING_UNIT_TESTS'):
    from prefetch import perma_cache_stub as perma_cache
else:
    from prefetch import perma_cache

# Always exclude picture desk due to media problems
DEFAULT_TAGS = ['-news/series/picture-desk-live']
DEFAULT_SHOW_TAGS = ['type', 'tone', 'keyword']

class DataSource(object):
    def __init__(self, client):
        self.client = client
        self.tags = []
        self.fields = ['trailText', 'headline', 'liveBloggingNow', 'standfirst', 'commentable', 'thumbnail', 'byline']
        self.page_size = 10
        self.content_type = None
        self.show_elements = None
        self.from_date = None
        self.show_most_viewed = False
        self.short_url = None
        self.section = None
        self.production_office = None
        self.show_tags = None

    def fetch_data(self):
        criteria = self._build_criteria()
        data = self._do_call(**criteria)
        return list(data)

    def fetch_title_override(self):
        return None

    def _build_criteria(self):
        criteria = {}

        if self.fields:
            criteria['show-fields'] = ','.join(self.fields)

        if self.content_type:
            self.tags.append('type/%s' % self.content_type)

        for default_tag in DEFAULT_TAGS:
            if default_tag not in self.tags:
                self.tags.append(default_tag)
        
        criteria['tag'] = ','.join(set(self.tags))

        show_tags = DEFAULT_SHOW_TAGS

        if self.show_tags:
            show_tags = show_tags + DEFAULT_SHOW_TAGS

        criteria['show-tags'] = ','.join(set(show_tags))

        if self.show_most_viewed:
            criteria['show-most-viewed'] = 'true'

        if self.page_size:
            criteria['page-size'] = self.page_size

        if self.from_date:
            criteria['from-date'] = self.from_date

        # TODO: Are we even using this?
        if self.short_url:
            criteria['short_url'] = self.short_url

        criteria['user-tier']='internal'

        for attr in ['production_office', 'section', 'show_elements']:
            attr_value = getattr(self,attr)
            if attr_value:
                criteria[attr] = attr_value

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
            if not url in [content_item['webUrl'] for content_item in content_list
             if 'webUrl' in content_item and url in content_item['webUrl']]:
                continue
            [content_item for content_item in content_list
             if url in content_item['webUrl']][0]['share_count'] = shared_count

        return content_list


class OphanDataSource(DataSource):
    def __init__(self, client, multi_content_data_source, fetcher, n_items):
        DataSource.__init__(self, client)
        self.multi_content_data_source = multi_content_data_source
        self.fetcher = fetcher
        self.n_items = n_items

    def _do_call(self, **criteria):
        urls = self.fetcher.fetch()
        #logging.info(urls)
        content_ids = [urlparse(url).path for(url, count) in urls]
        self.multi_content_data_source.content_ids = content_ids
        return self.multi_content_data_source.fetch_data()

    def fetch_data(self):
        # get data from
        # put results in datastore with key mt_ids
        return DataSource.fetch_data(self)


# class MostSharedDataSource(OphanDataSource):
#     def __init__(self, multi_content_data_source, fetcher, shared_count_interpolator, n_items=10):
#         OphanDataSource.__init__(self, None, multi_content_data_source, fetcher, n_items)
#         self.shared_count_interpolator  = shared_count_interpolator

#     def _do_call(self, **criteria):
#         most_shared_comment = super(OphanDataSource, self)._do_call(**criteria)
#         return self.shared_count_interpolator.interpolate(shared_urls_with_counts, most_shared_comment)

#     def __repr__(self):
#         return os.environ['CURRENT_VERSION_ID'] + "OphanMostSharedData"

class MostSharedDataSource(DataSource):

    def __init__(self, multi_content_data_source, most_shared_fetcher, shared_count_interpolator, n_items=10, result_decorator=None):
        DataSource.__init__(self, None)

        self.multi_content_data_source = multi_content_data_source
        self.multi_content_data_source.fields.append('shortUrl')

        self.most_shared_fetcher = most_shared_fetcher
        self.shared_count_interpolator  = shared_count_interpolator
        self.n_items = n_items
        self.result_decorator = result_decorator

    def _do_call(self, **criteria):

        shared_urls_with_counts = self.most_shared_fetcher.fetch_most_shared()

        content_ids = [urlparse(url).path for(url, count) in shared_urls_with_counts]
        self.multi_content_data_source.content_ids = content_ids
        most_shared_comment = self.multi_content_data_source.fetch_data()
        results = self.shared_count_interpolator.interpolate(shared_urls_with_counts, most_shared_comment)

        if self.result_decorator:
            results = self.result_decorator(results)
        return results

    def __repr__(self):
        return os.environ['CURRENT_VERSION_ID'] + "OphanMostSharedData"

class SearchDataSource(DataSource):
    def __init__(self, client):
        DataSource.__init__(self, client)

    def _do_call(self, **criteria):
        return self.client.search_query(**criteria)


class ItemDataSource(DataSource):
    def __init__(self, client, content_id='', show_editors_picks=False, show_most_viewed=False, only_editors_picks=False):
        DataSource.__init__(self, client)
        if show_editors_picks and show_most_viewed:
            raise DataSourceException('Cannot show most_viewed and editors_picks at the same time')
        self.content_id = content_id
        self.show_editors_picks = show_editors_picks
        self.show_most_viewed = show_most_viewed
        self.only_editors_picks = only_editors_picks
        self.show_elements = "image"

    def _do_call(self, **criteria):
        return self.client.item_query(self.content_id, self.show_editors_picks, self.show_most_viewed, self.only_editors_picks, **criteria)


class MultiContentDataSource(ItemDataSource):
    def __init__(self, client, name):
        ItemDataSource.__init__(self, client)
        self.content_ids = None
        self.name = name
        self.show_tags = ['keyword']
        self.show_elements = 'image'

    def _do_call(self, **criteria):
        if not self.content_ids:
            logging.warning("content_ids must be set before calling fetch_data()")
            return []

        result = []
        for id in self.content_ids:
            result.extend(self.client.content_query(id, **criteria))
        return result

    def __repr__(self):
        return str(self.__class__) + self.name


class ContentDataSource(ItemDataSource):
    def __init__(self, client, content_id):
        ItemDataSource.__init__(self, client, content_id=content_id)
        self.page_size = None

    def _do_call(self, **criteria):
        return self.client.content_query(self.content_id, **criteria)


class CultureDataSource(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, 'culture', show_editors_picks=True)
        self.name = 'culture' + client.edition
        self.show_tags = ['keyword']
        self.show_elements = 'image'

    def __repr__(self):
        return str(self.__class__) + self.name


class BusinessDataSource(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, 'business', show_editors_picks=True)
        self.name = 'business' + client.edition
        self.show_tags = ['keyword']
        self.show_elements = 'image'

    def __repr__(self):
        return str(self.__class__) + self.name


class CommentIsFreeDataSource(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, 'commentisfree', show_editors_picks=True)
        self.name = 'comment' + client.edition
        self.show_tags = ['keyword']
        self.show_elements = 'image'

    def __repr__(self):
        return str(self.__class__) + self.name

class CommentIsFreeCartoonDataSource(SearchDataSource):
    def __init__(self, client):
        DataSource.__init__(self, client)
        self.tags = ['commentisfree/series/guardian-comment-cartoon']
        self.show_elements = 'image'

class TravelDataSource(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, 'travel', show_editors_picks=True)


class TravelMostViewedDataSource(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, 'travel', show_most_viewed=True)


class TravelTopTenDataSource(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, 'travel/top10', show_editors_picks=True)


class TravelTipsDataSource(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, 'travel/series/readers-travel-tips')


class TravelVideoDataSource(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client,'travel', show_editors_picks=True)
        self.tags = ['type/video']


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

class MediaDataSource(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, 'media', show_editors_picks=True)


class MediaBlogDataSource(ItemDataSource):
    def __init__(self, client ):
        ItemDataSource.__init__(self, client, content_id='media/media-blog')


class MediaMonkeyDataSource(ItemDataSource):
    def __init__(self, client ):
        ItemDataSource.__init__(self, client, content_id='media/mediamonkeyblog')
        self.fields.append('body')


class MediaCommentDataSource(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, content_id='media')
        self.tags = ['tone/comment']


class MediaBriefingDataSource(ItemDataSource):
    def __init__(self, client ):
        ItemDataSource.__init__(self, client, content_id='media/series/media-briefing')


class PicOfDayDataSource(SearchDataSource):
    def __init__(self, client):
        DataSource.__init__(self, client)
        self.content_type = 'picture'
        self.tags = ['artanddesign/series/picture-of-the-day']
        self.page_size = 1
        self.show_elements = 'image'


class EyeWitnessDataSource(SearchDataSource):
    def __init__(self, client):
        DataSource.__init__(self, client)
        self.content_type = 'picture'
        self.tags = ['world/series/eyewitness']
        self.page_size = 1
        self.show_elements = 'image'


class MostViewedDataSource(ItemDataSource):
    def __init__(self, client):
        DataSource.__init__(self, client)
        self.show_elements = 'image'
        self.show_most_viewed = True
        self.show_editors_picks = False
        self.only_editors_picks = False
        self.content_id=''
        self.name = 'most_viewed' + client.edition

    def __repr__(self):
        return str(self.__class__) + self.name


class VideoDataSource(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, 'video', show_editors_picks=True)
        self.show_tags = ['keyword']
        self.show_elements = 'image'


    def __repr__(self):
        return str(self.__class__) + self.name

class FilmEditorsPicksDataSource(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, content_id='film', show_editors_picks=True)


class FilmMostViewedDataSource(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, content_id='film', show_most_viewed=True)


class FilmBlogsDataSource(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, content_id='film')
        self.tags = ['(film/series/week-in-geek|film/series/reelhistory|film/series/at-the-british-box-office|film/series/bigger-picture|film/series/trailer-review)']


class FilmInterviewsDataSource(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, content_id='film')
        self.tags = ['tone/interview']


class FilmOfTheWeekDataSource(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, content_id='film')
        self.tags = ['film/series/peter-bradshaw-film-of-the-week']


class FilmQuizDataSource(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, content_id='film')
        self.tags = ['tone/quizzes']


class IndiaDataSource(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, content_id='world/india', show_editors_picks=True)

class TopStoriesDataSource(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, show_editors_picks=True)
        self.name = 'top_stories' + client.edition
        self.show_elements = 'image'
        self.show_tags = ['keyword']


    def __repr__(self):
        return str(self.__class__) + self.name


class AusTopStoriesDataSource(TopStoriesDataSource):
    def __init__(self, client):
        TopStoriesDataSource.__init__(self,client)
        self.tags = ['world/australia']


class FilmTodayLatestDataSource(ItemDataSource):
    def __init__(self, client):
        ItemDataSource.__init__(self, client, content_id='film')
        self.page_size = 10


class DataSourceException(Exception):
    pass
