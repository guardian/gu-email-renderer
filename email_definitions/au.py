import logging
import datetime
from functools import partial

import pysistence as immutable
import pytz

import mail_renderer as mr
import handlers

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

class DailyEmailAUS(handlers.EmailTemplate):
    recognized_versions = ['v1', 'v2', 'v3', 'v2015']

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
        'v1': base_data_sources,
        'v2': base_data_sources.using(
            eye_witness=ds.EyeWitnessDataSource(clientAUS)),
        'v3': base_data_sources.using(
            eye_witness=ds.EyeWitnessDataSource(clientAUS),
            most_shared=dss.social.most_shared(clientAUS, ophan_client, 'au')),
        'v2015': base_data_sources.without('most_viewed'),
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
        'v1': base_priorities,
        'v2': base_priorities.concat(immutable.make_list(('eye_witness', 1))),
        'v3': base_priorities.concat(immutable.make_list(('most_shared', 6))),
        'v2015': base_priorities.without(('most_viewed', 6)),
        })

    template_names = immutable.make_dict({
        'v1': 'au/daily/v1',
        'v2': 'au/daily/v2',
        'v3': 'au/daily/v3',
        'v2015': 'au/daily/v2015'
    })

class Politics(handlers.EmailTemplate):
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


class CommentIsFree(handlers.EmailTemplate):
    recognized_versions = ['v1']

    most_shared_data_source = ds.MostSharedDataSource(
        most_shared_fetcher=MostSharedFetcher(ophan_client, section='commentisfree', country='au'),
        multi_content_data_source=ds.MultiContentDataSource(client=mr.client, name='most_shared'),
        shared_count_interpolator=ds.MostSharedCountInterpolator(),
        result_decorator=partial(add_comment_counts, discussion_client)
    )

    data_sources = immutable.make_dict({
        'v1': {
            'cif_most_shared': most_shared_data_source,
        },
    })

    priority_list = immutable.make_dict({
        'v1': [
        ('cif_most_shared', 5),],
    })

    template_names = immutable.make_dict({
        'v1': 'au/comment-is-free/v1',
    })

class Morning(handlers.EmailTemplate):
    recognized_versions = immutable.make_list('v1')

    data_sources = immutable.make_dict({
        'v1': {
            'top_stories': ds.TopStoriesDataSource(clientAUS),
            'world_news': dss.news.WorldNews(clientAUS),
            'australian_news': dss.au.News(clientAUS),
        }
    })

    priority_list = immutable.make_dict({
        'v1': [
            ('top_stories', 5),
            ('australian_news', 7),
            ('world_news', 5),
             ],
    })

    template_names = immutable.make_dict(v1='au/morning/v1')

    def additional_template_data(self):
        sydney_tz = pytz.timezone('Australia/Sydney')
        date_format = "%A %d %B %Y"
        return immutable.make_dict(
            sydney_date=datetime.datetime.now(sydney_tz).strftime(date_format)
        )

class Sport(handlers.EmailTemplate):
    recognized_versions = ['v1']

    data_sources = immutable.make_dict({
        'v1': {
            'au_sport': au.SportDataSource(client),
            'uk_sport': dss.sport.UK(client),
        }
    })

    priority_list = immutable.make_dict({
        'v1': [
            ('au_sport', 6),
            ('uk_sport', 4)
            ]
    })

    template_names = immutable.make_dict({
        'v1': 'au/sport/v1',
    })