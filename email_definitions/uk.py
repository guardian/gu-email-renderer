import logging

import pysistence as immutable

import data_source as ds
import data_sources.technology as tech_data

import mail_renderer as mr

client = mr.client


class DailyEmail(mr.EmailTemplate):
	recognized_versions = ['v1', 'india']

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
		'v1' : base_data_sources,
		'india' : base_data_sources.using(
			india_recent = ds.IndiaDataSource(client),
			)
	})

	priority_list = immutable.make_dict({
		'v1': [('top_stories', 6), ('most_viewed', 6),
					('sport', 3), ('comment', 3), ('culture', 3),
					('business', 2), ('technology', 2), ('travel', 2),
					('lifeandstyle', 2), ('eye_witness', 1)],
		'india': [('top_stories', 6), ('india_recent', 5), ('most_viewed', 6),
					('sport', 3), ('comment', 3), ('culture', 3),
					('business', 2), ('technology', 2), ('travel', 2),
					('lifeandstyle', 2), ('eye_witness', 1)],
		})

	template_names = immutable.make_dict({
		'v1': 'uk/daily/v1',
		'india': 'uk/daily/india',
	})

	def exclude_from_deduplication(self):
		return immutable.make_list('eye_witness')