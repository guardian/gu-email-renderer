from pysistence import make_dict

import data_source as ds
import data_sources.technology as tech_data

import mail_renderer as mr

client = mr.client


class DailyEmail(mr.EmailTemplate):
    recognized_versions = ['v1', 'v2', 'v3', 'v4', 'v5', 'india', 'MPU_v1a', 'MPU_v1b', 'MPU_v2']

    ad_tag = 'email-guardian-today'
    ad_config = {
        'leaderboard_v1': 'Top',
        'leaderboard_v2': 'Bottom'
    }

    data_sources = {}
    data_sources['v1'] = {
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
        }
    data_sources['v2'] = data_sources['v1']
    data_sources['v4'] = data_sources['v1']
    data_sources['v5'] = data_sources['v1']
    data_sources['MPU_v1a'] = data_sources['v1']
    data_sources['MPU_v1b'] = data_sources['v1']
    data_sources['MPU_v2'] = data_sources['v1']
    data_sources['v3'] = {
        'top_stories': ds.TopStoriesDataSource(client),
        'most_viewed': ds.MostViewedDataSource(client)
    }

    data_sources['india'] = data_sources['v1']
    data_sources['india']['india_recent'] = ds.IndiaDataSource(client)


    priority_list = {}
    priority_list['v1'] = [('top_stories', 6), ('most_viewed', 6),
                           ('sport', 3), ('comment', 3), ('culture', 3),
                           ('business', 2), ('technology', 2), ('travel', 2),
                           ('lifeandstyle', 2), ('eye_witness', 1)]

    priority_list['v2'] = [('top_stories', 6), ('most_viewed', 6), ('eye_witness', 1),
                           ('sport', 3), ('culture', 3), ('business', 2),
                           ('technology', 2), ('travel', 2), ('lifeandstyle', 2)]

    priority_list['v3'] = [('top_stories', 16), ('most_viewed', 16)]

    priority_list['v4'] = priority_list['v1']
    priority_list['v5'] = priority_list['v1']
    priority_list['india'] = [('top_stories', 6), ('india_recent', 5), ('most_viewed', 6),
                           ('sport', 3), ('comment', 3), ('culture', 3),
                           ('business', 2), ('technology', 2), ('travel', 2),
                           ('lifeandstyle', 2), ('eye_witness', 1)]
    priority_list['MPU_v1a'] = priority_list['v1']
    priority_list['MPU_v1b'] = priority_list['v1']
    priority_list['MPU_v2'] = priority_list['v1']

    template_names = {'v1': 'daily-email-v1',
                      'v2': 'daily-email-v2',
                      'v3': 'daily-email-v3',
                      'v4': 'daily-email-v4',
                      'v5': 'daily-email-v5',
                      'india': 'daily-email-india',
                      'MPU_v1a': 'daily-email-v6',
                      'MPU_v1b': 'daily-email-v7',
                      'MPU_v2': 'daily-email-v8',}