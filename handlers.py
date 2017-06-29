import os
import logging
import datetime

import jinja2
import webapp2
import htmlmin

from google.appengine.api import memcache

import pysistence as immutable

import deduplication
import template_filters

from ads import AdFetcher

if os.environ.has_key('SERVER_SOFTWARE') and os.environ['SERVER_SOFTWARE'].startswith('Development'):
    URL_ROOT = ''
else:
    URL_ROOT = 'https://gu-email-renderer.appspot.com'

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), "template")),
)

jinja_environment.globals.update({
        'URL_ROOT': URL_ROOT,
    })

jinja_environment.filters.update({
        'first_paragraph': template_filters.first_paragraph,
        'urlencode': template_filters.urlencode,
        'get_image': template_filters.get_image,
        'get_tone': template_filters.get_tone,
        'get_keyword': template_filters.get_keyword,
        'image_of_width': template_filters.image_of_width,
        'asset_url': template_filters.asset_url,
    })

jinja_environment.cache=None


class EmailTemplate(webapp2.RequestHandler):
    cache = memcache
    cache_bust = False
    default_ad_tag = 'email-guardian-today'
    minify = False

    def check_version_id(self, version_id):
        if not version_id in self.recognized_versions:
            logging.exception('Unrecognized version: %s' % version_id)
            logging.info('Valid versions {0}'.format(", ".join(self.recognized_versions)))
            self.abort(404)

    def resolve_template(self, template_name):
        return jinja_environment.get_template(template_name)

    def additional_template_data(self):
        return immutable.make_dict({})

    def exclude_from_deduplication(self):
        return immutable.make_list()

    @staticmethod
    def fetch_all(data_sources):
        """
        data is a map of type string->data_source.
        return a map with same keys as data, and retrieved data as values
        """

        #import pdb;pdb.set_trace()
        retrieved_data_map = {}

        for key, datasource in data_sources.items():
            retrieved_data_map[key] = datasource.fetch_data()

        return retrieved_data_map
    
    @staticmethod
    def fetch_all_title_overrides(data_sources):
        retrieved_data_map = {}

        for key, datasource in data_sources.items():
            title = datasource.fetch_title_override()
            if title is not None: 
                retrieved_data_map[key] = title

        return retrieved_data_map


    def get(self, version_id):
        self.check_version_id(version_id)

        cache_key = version_id + str(self.__class__)
        page = self.cache.get(cache_key)

        if self.cache_bust or not page:
            logging.debug('Cache miss with key: %s' % cache_key)
            retrieved_data = EmailTemplate.fetch_all(self.data_sources[version_id])
            title_overrides = EmailTemplate.fetch_all_title_overrides(self.data_sources[version_id])
            trail_blocks = deduplication.build_unique_trailblocks(retrieved_data,
                self.priority_list[version_id],
                excluded=self.exclude_from_deduplication())
            today = datetime.datetime.now()
            date = today.strftime('%A %d %b %Y')

            template_name = self.template_names[version_id] + '.html'
            template = self.resolve_template(template_name)

            ads = {}

            page = template.render(ads=ads, date=date, data=self.additional_template_data(), title_overrides=title_overrides, **trail_blocks)

            if self.minify:
                page = htmlmin.minify(page)

            self.cache.add(cache_key, page, 300)
        else:
            logging.debug('Cache hit with key: %s' % cache_key)
        
        self.response.out.write(page)

class Index(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('index.html')
        self.response.out.write(template.render())
