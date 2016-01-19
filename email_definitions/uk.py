import logging

import pysistence as immutable

import data_source as ds
import data_sources.technology as tech_data

import handlers
import mail_renderer as mr

from container_api import container

client = mr.client


class DailyEmail(handlers.EmailTemplate):
	recognized_versions = ['v1', 'v1-register', 'india', 'v2015', 'nhs']

	ad_tag = 'email-guardian-today'
	ad_config = {
		'leaderboard_v1': 'Top',
		'leaderboard_v2': 'Bottom'
	}

	base_data_sources = immutable.make_dict({
		'business': ds.BusinessDataSource(client),
		'technology': tech_data.TechnologyDataSource(client),
		'travel': ds.TravelDataSource(client),
		'lifeandstyle': ds.LifeAndStyleDataSource(client),
		'sport': ds.SportDataSource(client),
		'comment': ds.CommentIsFreeDataSource(client),
		'culture': ds.CultureDataSource(client),
		'top_stories': ds.TopStoriesDataSource(client),
		'eye_witness': ds.EyeWitnessDataSource(client),
		'most_viewed': ds.MostViewedDataSource(client),
		})

	data_sources = immutable.make_dict({
		'v1': base_data_sources,
		'v1-register': base_data_sources,
		'india': base_data_sources.using(
			india_recent = ds.IndiaDataSource(client),
			),
		'v2015': base_data_sources,
		'nhs': base_data_sources.using(
			nhs_special = container.for_id('346f91dc-60a5-41f1-a78e-513f6f379cec'),
			top_stories = container.for_id('uk-alpha/news/regular-stories')
			),
	})

	base_priorities = immutable.make_list(('top_stories', 6),
		('most_viewed', 6),
		('sport', 3), ('comment', 3), ('culture', 3),
		('business', 2), ('technology', 2), ('travel', 2),
		('lifeandstyle', 2), ('eye_witness', 1))

	priority_list = immutable.make_dict({
		'v1': base_priorities,
		'v1-register': base_priorities,
		'india': [('top_stories', 6), ('india_recent', 5), ('most_viewed', 6),
					('sport', 3), ('comment', 3), ('culture', 3),
					('business', 2), ('technology', 2), ('travel', 2),
					('lifeandstyle', 2), ('eye_witness', 1)],
		'v2015': base_priorities,
		'nhs': base_priorities.cons(('nhs_special', 2)),
		})

	template_names = immutable.make_dict({
		'v1': 'uk/daily/v1',
		'v1-register': 'uk/daily/v1-register',
		'india': 'uk/daily/india',
		'v2015': 'uk/daily/v2015',
		'nhs': 'uk/daily/nhs',
	})

	def exclude_from_deduplication(self):
		return immutable.make_list('eye_witness')
