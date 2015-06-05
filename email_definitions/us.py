from functools import partial

import pysistence as immutable

import handlers
import mail_renderer as mr

import data_source as ds
import data_sources as dss

from ophan_calls import OphanClient, MostSharedFetcher
from discussionapi.discussion_client import DiscussionFetcher, DiscussionClient, add_comment_counts
from container_api import container

clientUS = mr.clientUS
ophan_client = OphanClient(mr.ophan_base_url, mr.ophan_key)
discussion_client = DiscussionClient(mr.discussion_base_url)

class DailyEmailUS(handlers.EmailTemplate):
    recognized_versions = immutable.make_list('v1', 'v3', 'v6', 'v7')

    ad_tag = 'email-guardian-today-us'
    ad_config = {
        'leaderboard_v1': 'Top',
        'leaderboard_v2': 'Bottom'
    }

    base_data_sources = immutable.make_dict({
        'business': ds.BusinessDataSource(clientUS),
        'technology': dss.technology.TechnologyDataSource(clientUS),
        'sport': dss.us.SportUSDataSource(clientUS),
        'comment': ds.CommentIsFreeDataSource(clientUS),
        'culture': ds.CultureDataSource(clientUS),
        'top_stories': ds.TopStoriesDataSource(clientUS),
        'video': ds.VideoDataSource(clientUS),
    })

    most_shared_us = ds.MostSharedDataSource(
                most_shared_fetcher=MostSharedFetcher(ophan_client, country='us'),
                multi_content_data_source=ds.MultiContentDataSource(client=clientUS, name='most_shared_us'),
                shared_count_interpolator=ds.MostSharedCountInterpolator()
            )

    data_sources = immutable.make_dict({
        'v1': base_data_sources,
        'v3': base_data_sources,
        'v6': base_data_sources.using(
            most_shared_us = most_shared_us
        ),
        'v7': base_data_sources.using(
            most_shared_us = most_shared_us
        ),
    })

    base_priorities = immutable.make_list(('top_stories', 6),
        ('video', 3), ('sport', 3), ('comment', 3),
        ('culture', 3), ('business', 2), ('technology', 2),
        )

    priority_list = immutable.make_dict({
        'v1': base_priorities,
        'v3': base_priorities,
        'v6': base_priorities.cons(('most_shared_us', 6),),
        'v7': base_priorities.without(('business', 2))
            .cons(('most_shared_us', 6))
            .cons(('business', 3)),
    })

    template_names = immutable.make_dict({
        'v1': 'us/daily/v1',
        'v3': 'us/daily/v3',
        'v6': 'us/daily/v6',
        'v7': 'us/daily/v7',
    })

class Opinion(mr.EmailTemplate):
    recognized_versions = ['v1', 'v2', 'v3']

    most_shared_data_source = ds.MostSharedDataSource(
        most_shared_fetcher=MostSharedFetcher(ophan_client, section='commentisfree', country='us'),
        multi_content_data_source=ds.MultiContentDataSource(client=mr.client, name='most_shared'),
        shared_count_interpolator=ds.MostSharedCountInterpolator(),
        result_decorator=partial(add_comment_counts, discussion_client)
    )

    latest_us_opinion = dss.general.ItemDataSource('us/commentisfree', production_office='us')

    data_sources = immutable.make_dict({
        'v1': {
            'cif_most_shared': most_shared_data_source,
        },
         'v2': {
            'cif_most_shared': most_shared_data_source,
            'us_opinion': container.for_id('us-alpha/contributors/feature-stories')
        },
        'v3': {
            'cif_most_shared': most_shared_data_source,
            'latest_us_opinion': latest_us_opinion,
        }
    })

    priority_list = immutable.make_dict({
        'v1': [
            ('cif_most_shared', 5),
        ],
        'v2': [
            ('us_opinion', 3),
            ('cif_most_shared', 5),
            ],
        'v3': [
            ('cif_most_shared', 2),
            ('latest_us_opinion', 3),
        ]
    })

    template_names = immutable.make_dict({
        'v1': 'us/opinion/v1',
        'v2': 'us/opinion/v2',
        'v3': 'us/opinion/v3',
    })