import pysistence as immutable

import mail_renderer as mr

import data_source as ds
import data_sources.au as au
import data_sources.technology as tech_data

client = mr.client
clientAUS = mr.clientAUS

class DailyEmailAUS(mr.EmailTemplate):
    recognized_versions = ['v1', 'v2', 'v3']

    ad_tag = 'email-guardian-today-aus'
    ad_config = {
        'leaderboard_v1': 'Top',
        'leaderboard_v2': 'Bottom'
    }

    cultureDataSource = ds.ItemPlusBlogDataSource(ds.CultureDataSource(clientAUS), au.AusCultureBlogDataSource(clientAUS))

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
        'v2' : base_data_sources.using(eye_witness=ds.EyeWitnessDataSource(clientAUS)),
        'v3' : base_data_sources,
    }

    priority_list = {}
    priority_list['v1'] = [('top_stories', 6), ('most_viewed', 6), ('sport', 3),
                           ('aus_sport', 3), ('culture',3), ('comment', 3), ('lifeandstyle', 3),
                           ('technology', 2), ('environment', 2), ('science', 2), ('video', 3)]

    priority_list['v2'] = list(priority_list['v1'])
    priority_list['v2'].append(('eye_witness', 1))
    priority_list['v3'] = priority_list['v1']

    template_names = {
        'v1': 'daily-email-aus',
        'v2': 'daily-email-aus-v2',
        'v3' : 'au/daily/v3',
    }
