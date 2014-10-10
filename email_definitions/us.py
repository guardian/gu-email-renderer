from pysistence import make_dict

import mail_renderer as mr

from data_source import BusinessDataSource, \
	CommentIsFreeDataSource, CultureDataSource, TopStoriesDataSource, \
	VideoDataSource
from data_source import MultiContentDataSource, MostSharedCountInterpolator, MostSharedDataSource

from data_sources import us as data
from data_sources import technology as tech_data

from ophan_calls import OphanClient, MostSharedFetcher

clientUS = mr.clientUS
ophan_client = OphanClient(mr.ophan_base_url, mr.ophan_key)

class DailyEmailUS(mr.EmailTemplate):
    recognized_versions = ['v1', 'v3', 'v6', ]

    ad_tag = 'email-guardian-today-us'
    ad_config = {
        'leaderboard_v1': 'Top',
        'leaderboard_v2': 'Bottom'
    }

    base_data_sources = make_dict({
        'business': BusinessDataSource(clientUS),
        'money': data.USMoneyDataSource(clientUS),
        'technology': tech_data.TechnologyDataSource(clientUS),
        'sport': data.SportUSDataSource(clientUS),
        'comment': CommentIsFreeDataSource(clientUS),
        'culture': CultureDataSource(clientUS),
        'top_stories': TopStoriesDataSource(clientUS),
        'video': VideoDataSource(clientUS),
    })

    data_sources = {
        'v1' : base_data_sources,
        'v3' : base_data_sources,
        'v6' : base_data_sources.using(
            most_shared_us = MostSharedDataSource(
                most_shared_fetcher=MostSharedFetcher(ophan_client, country='us'),
                multi_content_data_source=MultiContentDataSource(client=clientUS, name='most_shared_us'),
                shared_count_interpolator=MostSharedCountInterpolator()
            )
        ),
    }

    priority_list = {}
    priority_list['v1'] = [('top_stories', 6), ('video', 3), ('sport', 3), ('comment', 3),
                           ('culture', 3), ('business', 2), ('money', 2), ('technology', 2)]
    priority_list['v3'] = [('top_stories', 6), ('video', 3), ('sport', 3), ('comment', 3),
                           ('culture', 3), ('business', 2), ('money', 2), ('technology', 2)]
    priority_list['v6'] = [('top_stories', 6), ('video', 3), ('sport', 3),
        ('comment', 3), ('culture', 3), ('business', 2), ('money', 2),
        ('technology', 2), ('most_shared_us', 6), ]

    template_names = {
        'v1': 'daily-email-us',
        'v3': 'daily-email-us-v3',
        'v6' : 'us/daily/v6',
    }
