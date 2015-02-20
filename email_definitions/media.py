import mail_renderer as mr
import data_source as ds

import pysistence as immutable

class MediaBriefing(mr.EmailTemplate):
    recognized_versions = immutable.make_list('v1')
    cache_bust=True

    ad_tag = 'email-media-briefing'
    ad_config = immutable.make_dict({
        'leaderboard_v1': 'Top',
        'leaderboard_v2': 'Bottom'
    })

    data_sources = immutable.make_dict({'v1': {
        'media_stories': ds.MediaDataSource(mr.client),
        'media_monkey': ds.MediaMonkeyDataSource(mr.client),
        'media_briefing': ds.MediaBriefingDataSource(mr.client)
        }
    })

    priority_list = immutable.make_dict({
    	'v1': immutable.make_list(('media_stories', 10),
    		('media_monkey', 1), ('media_briefing', 1)),
    	})

    template_names = immutable.make_dict({'v1': 'media/media-briefing'})