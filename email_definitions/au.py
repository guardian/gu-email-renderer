import pysistence as immutable

import mail_renderer as mr

import data_source as ds
import data_sources.au as au
import data_sources.technology as tech_data

from ophan_calls import OphanClient, MostSharedFetcher

client = mr.client
clientAUS = mr.clientAUS

ophan_client = OphanClient(mr.ophan_base_url, mr.ophan_key)

class DailyEmailAUS(mr.EmailTemplate):
    recognized_versions = ['v1', 'v2', 'v3']

    ad_tag = 'email-guardian-today-aus'
    ad_config = {
        'leaderboard_v1': 'Top',
        'leaderboard_v2': 'Bottom'
    }

    cultureDataSource = ds.ItemPlusBlogDataSource(ds.CultureDataSource(clientAUS), au.AusCultureBlogDataSource(clientAUS))
    most_shared_datasource = ds.MostSharedDataSource(
                most_shared_fetcher=MostSharedFetcher(ophan_client, country='au'),
                multi_content_data_source=ds.MultiContentDataSource(client=client, name='most_shared'),
                shared_count_interpolator=ds.MostSharedCountInterpolator()
            )

    base_data_sources = immutable.make_dict({
        'top_stories_code': ds.TopStoriesDataSource(clientAUS),
        'top_stories': ds.TopStoriesDataSource(clientAUS),
        'most_viewed': ds.MostViewedDataSource(clientAUS),
        'sport': ds.SportDataSource(clientAUS),
        'aus_sport': ds.AusSportDataSource(client),
        'culture': cultureDataSource,
        'comment': au.AusCommentIsFreeDataSource(clientAUS),
        'lifeandstyle': ds.LifeAndStyleDataSource(clientAUS),
        'technology': tech_data.TechnologyDataSource(clientAUS),
        'environment': ds.EnvironmentDataSource(clientAUS),
        'science' : ds.ScienceDataSource(clientAUS),
        'video' :  au.AusVideoDataSource(clientAUS),       
        })

    data_sources = {
        'v1' : base_data_sources,
        'v2' : base_data_sources.using(
            eye_witness=ds.EyeWitnessDataSource(clientAUS)),
        'v3' : base_data_sources.using(
            eye_witness=ds.EyeWitnessDataSource(clientAUS),
            most_shared=most_shared_datasource),
    }

    base_priorities = immutable.make_list(
        ('top_stories', 6),
        ('most_viewed', 6),
        ('sport', 3),
        ('aus_sport', 3),
        ('culture',3),
        ('comment', 3),
        ('lifeandstyle', 3),
        ('technology', 2),
        ('environment', 2),
        ('science', 2),
        ('video', 3))

    priority_list = immutable.make_dict({
        'v1' : base_priorities,
        'v2' : base_priorities.concat(immutable.make_list(('eye_witness', 1))),
        'v3' : base_priorities.concat(immutable.make_list(('most_shared', 6))),
        })

    template_names = immutable.make_dict({
        'v1': 'daily-email-aus',
        'v2': 'daily-email-aus-v2',
        'v3': 'au/daily/v3',
    })


class AustralianPolitics(mr.EmailTemplate):
    recognized_versions = ['v1']

    ad_tag = 'email-australian-politics'
    ad_config = {}

    data_sources = {
        'v1': {
            'politics_latest': au.AustralianPoliticsDataSource(client),
            'politics_comment': au.AusCommentIsFreeDataSource(clientAUS),
            'politics_video': au.AustralianPoliticsVideoDataSource(client)
        }
    }

    priority_list = {
        'v1': [('politics_comment', 1), ('politics_video', 1), ('politics_latest', 4)]
    }

    template_names = {'v1': 'australian-politics'}