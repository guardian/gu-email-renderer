import mail_renderer as mr

import data_source as ds

from guardianapi.apiClient import ApiClient

client = ApiClient(mr.base_url, mr.api_key, edition="uk")

class FilmToday(mr.EmailTemplate):
    recognized_versions = ['v1']

    ad_tag = 'email-film-today'
    ad_config = {
        'leaderboard': 'Top'
    }

    data_sources = {
        'v1': {
            'film_today_latest': ds.FilmTodayLatestDataSource(client)
        }
    }

    priority_list = {
        'v1': [('film_today_latest', 10)]
    }

    template_names = {'v1': 'film-today-v1'}

class SleeveNotes(mr.EmailTemplate):
    recognized_versions = ['v1', 'v2', 'v3']

    ad_tag = 'email-sleeve-notes'
    ad_config = {
        'leaderboard': 'Top',
        'leaderboard2': 'Bottom',
    }

    data_sources = {}
    data_sources['v1'] = {
        'music_most_viewed': ds.MusicMostViewedDataSource(client),
        'music_picks': ds.MusicEditorsPicksDataSource(client),
        'music_blog': ds.MusicBlogDataSource(client),
        'music_watch_listen': ds.MusicWatchListenDataSource(client),
        'music_further': ds.MusicEditorsPicksDataSource(client),
        }
    data_sources['v2'] = data_sources['v1']
    data_sources['v3'] = data_sources['v1']

    priority_list = {}
    priority_list['v1'] = [('music_most_viewed', 3), ('music_picks', 5), ('music_blog', 5),
                           ('music_watch_listen', 5), ('music_further', 3)]

    priority_list['v2'] = priority_list['v1']
    priority_list['v3'] = priority_list['v1']

    template_names = {'v1': 'sleeve-notes-v1',
                      'v2': 'sleeve-notes-v2',
                      'v3': 'sleeve-notes-v3'}


