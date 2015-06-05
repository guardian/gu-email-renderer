import webapp2

import mail_renderer as mr
import handlers
import deduplication

import data_source as ds
import data_sources as dss

from discussionapi.discussion_client import DiscussionFetcher, DiscussionClient

client = mr.client

class EditorsPicks(handlers.EmailTemplate):
    recognized_versions = ['v1']

    data_sources = {}
    data_sources['v1'] = { 'editors_picks' : ds.TopStoriesDataSource(client) }
    priority_list = {'v1': [('editors_picks', 3)]}
    template_names = {'v1': 'editors-picks'}

class MostCommented(handlers.EmailTemplate):
    recognized_versions = ['v1']
    n_items=6

    discussion_client = DiscussionClient(mr.discussion_base_url)
    discussion_fetcher = DiscussionFetcher(discussion_client)
    multi_content_data_source = ds.MultiContentDataSource(client=client, name='most_commented')
    comment_count_interpolator = ds.CommentCountInterpolator()

    most_commented_data_source = ds.MostCommentedDataSource(
        discussion_fetcher=discussion_fetcher,
        multi_content_data_source=multi_content_data_source,
        comment_count_interpolator=comment_count_interpolator
        )

    data_sources = {}
    data_sources['v1'] = {
        'most_commented': most_commented_data_source
        }

    priority_list = {'v1': [('most_commented', n_items)]}
    template_names = {'v1': 'most-commented'}


class MostViewed(handlers.EmailTemplate):
    recognized_versions = ['v1']

    data_sources = {}
    data_sources['v1'] = { 'most_viewed' : ds.MostViewedDataSource(client) }
    priority_list = {'v1': [('most_viewed', 3)]}
    template_names = {'v1': 'most-viewed'}

class Headline(webapp2.RequestHandler):

    def get(self, edition="uk"):

        data_sources = {'top_stories': dss.headlines.for_edition(edition)}
        priority_list = [('top_stories', 1)]
        template_data = {}
        retrieved_data = handlers.EmailTemplate.fetch_all(data_sources)
        trail_block = deduplication.build_unique_trailblocks(retrieved_data,priority_list)
        stories = trail_block.get('top_stories')
        headlines = [s.get('webTitle') for s in stories]
        if headlines:
            headline = headlines[0]
            template_data['headline'] = headline
        template = handlers.jinja_environment.get_template('headline.html')
        self.response.out.write(template.render(template_data))