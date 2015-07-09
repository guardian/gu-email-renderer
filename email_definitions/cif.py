import pysistence as immutable

import mail_renderer as mr
import handlers

import data_source as ds

from discussionapi.discussion_client import DiscussionFetcher, DiscussionClient
from ophan_calls import OphanClient, MostSharedFetcher

from container_api import container

client = mr.client

class CommentIsFree(handlers.EmailTemplate):
    recognized_versions = immutable.make_list('v1', 'v2', 'v3')

    ad_tag = 'email-speakers-corner'
    ad_config = {
        'leaderboard': 'Top'
    }

    ophan_client = OphanClient(mr.ophan_base_url, mr.ophan_key)
    most_shared_data_source = ds.MostSharedDataSource(
        most_shared_fetcher=MostSharedFetcher(ophan_client, section='commentisfree'),
        multi_content_data_source=ds.MultiContentDataSource(client=client, name='most_shared'),
        shared_count_interpolator=ds.MostSharedCountInterpolator()
    )

    discussion_client = DiscussionClient(mr.discussion_base_url)
    most_commented_data_source = ds.MostCommentedDataSource (
        discussion_fetcher = DiscussionFetcher(discussion_client, 'commentisfree'),
        multi_content_data_source = ds.MultiContentDataSource(client=client, name='most_commented'),
        comment_count_interpolator = ds.CommentCountInterpolator()
    )

    data_sources = immutable.make_dict({
        'v1': {
            'uk_opinion_front': container.for_id('uk/commentisfree/regular-stories'),
            'cif_cartoon': ds.CommentIsFreeCartoonDataSource(client),
        },
        'v3': {
            'cif_most_shared': most_shared_data_source,
            'cif_cartoon': ds.CommentIsFreeCartoonDataSource(client),
        },
        'v2': {
            'cif_most_commented': most_commented_data_source,
            'cif_cartoon': ds.CommentIsFreeCartoonDataSource(client),
        }
    })

    priority_list = {
        'v3': [('cif_cartoon', 1), ('cif_most_shared', 5)],
        'v2': [('cif_cartoon', 1), ('cif_most_commented', 5)],
        'v1': [('uk_opinion_front', 10), ('cif_cartoon', 1),],
    }

    template_names = immutable.make_dict({
        'v3': 'comment-is-free/v3',
        'v2': 'comment-is-free/v2',
        'v1': 'comment-is-free/v1',
    })

