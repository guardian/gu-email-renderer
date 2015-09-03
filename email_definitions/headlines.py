import webapp2

import handlers
import deduplication

import data_source as ds
import data_sources as dss

from container_api import container

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

class FilmHeadline(webapp2.RequestHandler):

    def get(self, path="film"):

        data_sources = {'stories': container.for_id('6d84cd8d-d159-4e9a-ba2f-8852528d2d03')}
        priority_list = [('stories', 1)]
        template_data = {}
        retrieved_data = handlers.EmailTemplate.fetch_all(data_sources)
        trail_block = deduplication.build_unique_trailblocks(retrieved_data,priority_list)
        stories = trail_block.get('stories')
        headlines = [s.get('webTitle') for s in stories]
        if headlines:
            headline = headlines[0]
            template_data['headline'] = headline
        template = handlers.jinja_environment.get_template('headline.html')
        self.response.out.write(template.render(template_data))

class UKOpinion(webapp2.RequestHandler):

    def get(self):
        data_sources = {'stories': container.for_id('uk/commentisfree/regular-stories')}
        priority_list = [('stories', 1)]
        template_data = {}
        retrieved_data = handlers.EmailTemplate.fetch_all(data_sources)
        trail_block = deduplication.build_unique_trailblocks(retrieved_data,priority_list)
        stories = trail_block.get('stories')
        headlines = [s.get('fields', {}).get('headline') for s in stories]
        if headlines:
            headline = headlines[0]
            template_data['headline'] = headline
        template = handlers.jinja_environment.get_template('headline.html')
        self.response.out.write(template.render(template_data))