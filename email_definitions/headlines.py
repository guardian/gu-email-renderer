import logging

import webapp2

import pysistence as immutable

import handlers
import deduplication

import data_source as ds
import data_sources as dss

from container_api import container

import mail_renderer as mr

def read_headline(content):
    logging.info(content)
    if 'fields' in content and 'headline' in content['fields']:
        return content['fields']['headline']

    return content.get('webTitle')

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

class GenericHeadline(webapp2.RequestHandler):

    def get(self, path="film"):
        logging.info(path)

        path_mapping = immutable.make_dict({
            'film': container.for_id('6d84cd8d-d159-4e9a-ba2f-8852528d2d03'),
            'uk/opinion/v1': container.for_id('uk/commentisfree/regular-stories'),
            'film/v1': ds.FilmTodayLatestDataSource(mr.client),
        })

        if not path in path_mapping.keys():
            webapp2.abort(404, "Path {0} not mapped to a datasource".format(path))
            return

        stories_data_source = path_mapping[path]

        data_sources = {'stories': stories_data_source}
        priority_list = [('stories', 1)]
        template_data = {}
        retrieved_data = handlers.EmailTemplate.fetch_all(data_sources)
        trail_block = deduplication.build_unique_trailblocks(retrieved_data,priority_list)
        stories = trail_block.get('stories')

        headlines = [read_headline(s) for s in stories]
        if headlines:
            headline = headlines[0]
            template_data['headline'] = headline

        template = handlers.jinja_environment.get_template('headline.html')
        self.response.out.write(template.render(template_data))