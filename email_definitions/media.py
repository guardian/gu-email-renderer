import mail_renderer as mr
import data_source as ds

class MediaBriefing(mr.EmailTemplate):
    recognized_versions = ['v1']
    cache_bust=True

    ad_tag = 'email-media-briefing'
    ad_config = {
        'leaderboard_v1': 'Top',
        'leaderboard_v2': 'Bottom'
    }

    data_sources = {}
    data_sources['v1'] = {
        'media_stories': ds.MediaDataSource(mr.client),
        'media_monkey': ds.MediaMonkeyDataSource(mr.client),
        'media_briefing': ds.MediaBriefingDataSource(mr.client)
        }

    priority_list = {}
    priority_list['v1'] = [('media_stories', 10), ('media_monkey', 1), ('media_briefing', 1)]

    template_names = {'v1': 'media/media-briefing'}