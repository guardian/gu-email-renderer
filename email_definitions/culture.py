import pysistence as immutable

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

    base_data_sources = immutable.make_dict({
        'music_most_viewed': ds.MusicMostViewedDataSource(client),
        'music_picks': ds.MusicEditorsPicksDataSource(client),
        'music_blog': ds.MusicBlogDataSource(client),
        'music_watch_listen': ds.MusicWatchListenDataSource(client),
        'music_further': ds.MusicEditorsPicksDataSource(client),        
        })

    data_sources = {
        'v1' : base_data_sources,
        'v2' : base_data_sources,
        'v3' : base_data_sources,
    }

    priority_list = {}
    priority_list['v1'] = [('music_most_viewed', 3), ('music_picks', 5), ('music_blog', 5),
                           ('music_watch_listen', 5), ('music_further', 3)]

    priority_list['v2'] = priority_list['v1']
    priority_list['v3'] = priority_list['v1']

    template_names = immutable.make_dict({
        'v1': 'sleeve-notes-v1',
        'v2': 'sleeve-notes-v2',
        'v3': 'sleeve-notes-v3',
        })

class CloseUp(mr.EmailTemplate):
    recognized_versions = ['v1', 'v2', 'v3']

    ad_tag = 'email-close-up'
    ad_config = {
        'leaderboard_v1': 'Top',
        'leaderboard_v2': 'Bottom'
    }

    base_data_sources = immutable.make_dict({
        'film_week': ds.FilmOfTheWeekDataSource(client),
        'film_picks': ds.FilmEditorsPicksDataSource(client),
        'film_show': ds.FilmShowDataSource(client),
        'film_most_viewed': ds.FilmMostViewedDataSource(client),
        'film_interviews': ds.FilmInterviewsDataSource(client),
        'film_blogs': ds.FilmBlogsDataSource(client),
        'film_quiz': ds.FilmQuizDataSource(client)
        })

    data_sources = immutable.make_dict({
        'v1': base_data_sources,
        'v2': base_data_sources,
        'v3': base_data_sources,
    })

    priority_list = {}
    priority_list['v1'] = [('film_week', 1), ('film_show', 1), ('film_interviews', 3),
                           ('film_blogs', 5), ('film_quiz', 1), ('film_picks', 2), ('film_most_viewed', 3)]

    priority_list['v2'] = priority_list['v1']
    priority_list['v3'] = priority_list['v1']

    template_names = immutable.make_dict({
        'v1': 'culture/close-up/v1',
        'v2': 'culture/close-up/v2',
        'v3': 'culture/close-up/v3'
    })

