import pysistence as immutable

import mail_renderer as mr
from discussionapi.discussion_client import DiscussionFetcher, DiscussionClient
from data_source import MostCommentedDataSource, \
	MostSharedDataSource, MostSharedCountInterpolator, MultiContentDataSource, CommentCountInterpolator

import data_sources as dss

class ZipFile(mr.EmailTemplate):
    recognized_versions = ['v1']

    ad_tag = 'email-technology-roundup'
    ad_config = {
        'leaderboard_v1': 'Top',
        'leaderboard_v2': 'Bottom'
    }

    discussion_client = DiscussionClient(mr.discussion_base_url)
    tech_most_commented = MostCommentedDataSource (
        discussion_fetcher = DiscussionFetcher(discussion_client, 'technology'),
        multi_content_data_source = MultiContentDataSource(client=mr.client, name='most_commented'),
        comment_count_interpolator = CommentCountInterpolator()
    )

    data_sources = immutable.make_dict({
        'v1': {
            'tech_news': dss.technology.TechnologyDataSource(mr.client),
            'tech_most_commented': tech_most_commented,
            'tech_games': dss.technology.TechnologyGamesDataSource(mr.client),
            'tech_podcast': dss.technology.TechnologyPodcastDataSource(mr.client),
            'tech_video': dss.technology.TechnologyVideoDataSource(mr.client)
        }
    })

    priority_list = {
        'v1': [('tech_video', 1),
            ('tech_news', 5),
            ('tech_most_commented', 3),
            ('tech_games', 3),
            ('tech_podcast', 1)]
    }

    template_names = {'v1': 'technology/zip-file'}

