import mail_renderer as mr
from data_source import FilmTodayLatestDataSource

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
            'film_today_latest': FilmTodayLatestDataSource(client)
        }
    }

    priority_list = {
        'v1': [('film_today_latest', 10)]
    }

    template_names = {'v1': 'film-today-v1'}

