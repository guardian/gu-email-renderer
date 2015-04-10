import logging
from functools import partial

import pysistence as immutable

import mail_renderer as mr

import data_source as ds
import data_sources.au as au
import data_sources.technology as tech_data
import data_sources as dss

from ophan_calls import OphanClient, MostSharedFetcher
from discussionapi.discussion_client import DiscussionFetcher, DiscussionClient, add_comment_counts

client = mr.client
clientAUS = mr.clientAUS

ophan_client = OphanClient(mr.ophan_base_url, mr.ophan_key)
discussion_client = DiscussionClient(mr.discussion_base_url)

class DailyEmailAUS(mr.EmailTemplate):
    recognized_versions = ['v1', 'v2', 'v3']

    ad_tag = 'email-guardian-today-aus'
    ad_config = {
        'leaderboard_v1': 'Top',
        'leaderboard_v2': 'Bottom'
    }

    cultureDataSource = ds.ItemPlusBlogDataSource(ds.CultureDataSource(clientAUS), au.AusCultureBlogDataSource(clientAUS))

    base_data_sources = immutable.make_dict({
        'top_stories_code': ds.TopStoriesDataSource(clientAUS),
        'top_stories': ds.TopStoriesDataSource(clientAUS),
        'most_viewed': ds.MostViewedDataSource(clientAUS),
        'aus_sport': au.SportDataSource(client),
        'culture': cultureDataSource,
        'comment': au.AusCommentIsFreeDataSource(clientAUS),
        'lifeandstyle': ds.LifeAndStyleDataSource(clientAUS),
        'technology': tech_data.TechnologyDataSource(clientAUS),
        'environment': au.Environment(clientAUS),
        'science' : ds.ScienceDataSource(clientAUS),
        'video' :  au.AusVideoDataSource(clientAUS),       
        })

    data_sources = {
        'v1' : base_data_sources,
        'v2' : base_data_sources.using(
            eye_witness=ds.EyeWitnessDataSource(clientAUS)),
        'v3' : base_data_sources.using(
            eye_witness=ds.EyeWitnessDataSource(clientAUS),
            most_shared=dss.social.most_shared(clientAUS, ophan_client, 'au')),
    }

    base_priorities = immutable.make_list(
        ('top_stories', 6),
        ('most_viewed', 6),
        ('aus_sport', 5),
        ('culture',3),
        ('comment', 3),
        ('lifeandstyle', 3),
        ('technology', 2),
        ('environment', 2),
        ('science', 2),
        ('video', 3))

    priority_list = immutable.make_dict({
        'v1' : base_priorities,
        'v2' : base_priorities.concat(immutable.make_list(('eye_witness', 1))),
        'v3' : base_priorities.concat(immutable.make_list(('most_shared', 6))),
        })

    template_names = immutable.make_dict({
        'v1': 'au/daily/v1',
        'v2': 'au/daily/v2',
        'v3': 'au/daily/v3',
    })

class Politics(mr.EmailTemplate):
    recognized_versions = immutable.make_list('v1')

    ad_tag = 'email-australian-politics'
    ad_config = {}

    data_sources = immutable.make_dict({
        'v1': {
            'politics_latest': au.AustralianPoliticsDataSource(client),
            'politics_comment': au.AusCommentIsFreeDataSource(clientAUS),
            'politics_video': au.AustralianPoliticsVideoDataSource(client)
        }
    })

    priority_list = {
        'v1': [
            ('politics_comment', 1),
            ('politics_video', 1),
            ('politics_latest', 4)],
    }

    template_names = immutable.make_dict({'v1': 'au/politics'})


class CommentIsFree(mr.EmailTemplate):
    recognized_versions = ['v1']

    ad_tag = 'email-speakers-corner'
    ad_config = {
        'leaderboard': 'Top'
    }

    most_shared_data_source = ds.MostSharedDataSource(
        most_shared_fetcher=MostSharedFetcher(ophan_client, section='commentisfree', country='au'),
        multi_content_data_source=ds.MultiContentDataSource(client=mr.client, name='most_shared'),
        shared_count_interpolator=ds.MostSharedCountInterpolator(),
        result_decorator=partial(add_comment_counts, discussion_client)
    )

    data_sources = {
        'v1': {
            'cif_most_shared': most_shared_data_source,
        },
    }

    priority_list = {
        'v1': [
        ('cif_most_shared', 5),],
    }

    template_names = {
        'v1': 'au/comment-is-free/v1',
    }

class Morning(mr.EmailTemplate):
    recognized_versions = immutable.make_list('v1')

    ad_tag = 'email-australia-morning'
    ad_config = {}

    data_sources = immutable.make_dict({
        'v1': {
            'top_stories': ds.TopStoriesDataSource(clientAUS),
            'most_viewed': ds.MostViewedDataSource(clientAUS),
            'world_news': dss.news.WorldNews(clientAUS),
            'australian_news': dss.au.News(clientAUS),
        }
    })

    priority_list = immutable.make_dict({
        'v1': [
            ('top_stories', 5),
            ('australian_news', 5),
            ('world_news', 5),
            ('most_viewed', 5),
            ],
    })

    template_names = immutable.make_dict({'v1': 'au/morning/v1'})

