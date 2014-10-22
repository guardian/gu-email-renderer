import mail_renderer as mr
from discussionapi.discussion_client import DiscussionFetcher, DiscussionClient
from data_source import MostCommentedDataSource, \
	MostSharedDataSource, MostSharedCountInterpolator, MultiContentDataSource, CommentCountInterpolator
from data_sources import technology as tech_ds

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

    data_sources = {
        'v1': {
            'tech_news': tech_ds.TechnologyDataSource(mr.client),
            'tech_most_commented': tech_most_commented,
            'tech_games': tech_ds.TechnologyGamesDataSource(mr.client),
            'tech_blog': tech_ds.TechnologyBlogDataSource(mr.client),
            'tech_podcast': tech_ds.TechnologyPodcastDataSource(mr.client),
            'tech_video': tech_ds.TechnologyVideoDataSource(mr.client)
        }
    }

    priority_list = {
        'v1': [('tech_video', 1), ('tech_news', 5), ('tech_most_commented', 3), ('tech_games', 3), ('tech_blog', 5), ('tech_podcast', 1)]
    }

    template_names = {'v1': 'zip-file'}

