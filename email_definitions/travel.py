import pysistence as immutable

import handlers
import mail_renderer as mr

import data_source as ds

client = mr.client

class TheFlyer(handlers.EmailTemplate):
    recognized_versions = immutable.make_list('v1')

    ad_tag = 'email-the-flyer'
    ad_config = {
        'leaderboard': 'Top'
    }

    data_sources = immutable.make_dict({
        'v1': {
            'travel_picks': ds.TravelDataSource(client),
            'travel_most_viewed': ds.TravelMostViewedDataSource(client),
            'travel_top_ten': ds.TravelTopTenDataSource(client),
            'travel_video': ds.TravelVideoDataSource(client),
            'travel_tips': ds.TravelTipsDataSource(client),
        }
    })

    priority_list = immutable.make_dict({
        'v1': [('travel_video', 1), ('travel_picks', 5), ('travel_most_viewed', 3),
               ('travel_top_ten', 5), ('travel_tips', 1)]
    })

    template_names = immutable.make_dict({'v1': 'travel/the-flyer'})