from functools import partial

import pysistence as immutable

import mail_renderer as mr

import data_source as ds

from data_source import BusinessDataSource, \
	CommentIsFreeDataSource, CultureDataSource, TopStoriesDataSource, \
	VideoDataSource
from data_source import MultiContentDataSource, MostSharedCountInterpolator, MostSharedDataSource

from data_sources import us as data
from data_sources import technology as tech_data

from ophan_calls import OphanClient, MostSharedFetcher
from discussionapi.discussion_client import DiscussionFetcher, DiscussionClient, add_comment_counts

clientUS = mr.clientUS
ophan_client = OphanClient(mr.ophan_base_url, mr.ophan_key)
discussion_client = DiscussionClient(mr.discussion_base_url)

class DailyEmailUS(mr.EmailTemplate):
    recognized_versions = immutable.make_list('v1', 'v3', 'v6', 'v7')

    ad_tag = 'email-guardian-today-us'
    ad_config = {
        'leaderboard_v1': 'Top',
        'leaderboard_v2': 'Bottom'
    }

    base_data_sources = immutable.make_dict({
        'business': BusinessDataSource(clientUS),
        'technology': tech_data.TechnologyDataSource(clientUS),
        'sport': data.SportUSDataSource(clientUS),
        'comment': CommentIsFreeDataSource(clientUS),
        'culture': CultureDataSource(clientUS),
        'top_stories': TopStoriesDataSource(clientUS),
        'video': VideoDataSource(clientUS),
    })

    most_shared_us = MostSharedDataSource(
                most_shared_fetcher=MostSharedFetcher(ophan_client, country='us'),
                multi_content_data_source=MultiContentDataSource(client=clientUS, name='most_shared_us'),
                shared_count_interpolator=MostSharedCountInterpolator()
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
    recognized_versions = ['v1']

    ad_tag = 'email-speakers-corner'
    ad_config = {
        'leaderboard': 'Top'
    }

    most_shared_data_source = ds.MostSharedDataSource(
        most_shared_fetcher=MostSharedFetcher(ophan_client, section='commentisfree', country='us'),
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
        'v1': 'us/opinion/v1',
    }