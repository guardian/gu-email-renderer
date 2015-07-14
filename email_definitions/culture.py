import pysistence as immutable

import mail_renderer as mr
import handlers

import data_source as ds
import data_sources as dss

from guardianapi.apiClient import ApiClient

from container_api import container

client = ApiClient(mr.base_url, mr.api_key, edition="uk")

class FilmToday(handlers.EmailTemplate):
    recognized_versions = ['v1', 'v2']

    ad_tag = 'email-film-today'
    ad_config = immutable.make_dict({
        'leaderboard': 'Top'
    })

    data_sources = immutable.make_dict({
        'v1': {
            'film_today_latest': ds.FilmTodayLatestDataSource(client)
        },
        'v2': {
            'film_front': container.for_id('1ce8-6c50-425f-9d32')
        }
    })

    priority_list = immutable.make_dict({
        'v1': [('film_today_latest', 10)],
        'v2': [('film_front', 10)],
    })

    template_names = immutable.make_dict({
        'v1': 'culture/film-today/v1',
        'v2': 'culture/film-today/v2',
    })

class SleeveNotes(handlers.EmailTemplate):
    recognized_versions = ['v1', 'v2', 'v3']

    ad_tag = 'email-sleeve-notes'
    ad_config = {
        'leaderboard': 'Top',
        'leaderboard2': 'Bottom',
    }

    music_editors_picks = dss.general.ItemDataSource(content_id='music', show_editors_picks=True, tags=['-tone/news'])

    base_data_sources = immutable.make_dict({
        'music_most_viewed': dss.general.ItemDataSource(content_id='music', show_most_viewed=True),
        'music_picks': music_editors_picks,
        'music_blog': dss.general.ItemDataSource(content_id='music/musicblog'),
        'music_watch_listen': dss.general.ItemDataSource(content_id='music', tags=['(type/video|type/audio)']),
        'music_further': music_editors_picks,        
        })

    data_sources = immutable.make_dict({
        'v1' : base_data_sources,
        'v2' : base_data_sources,
        'v3' : base_data_sources,
    })

    priorities = immutable.make_list(('music_most_viewed', 3),
        ('music_picks', 5),
        ('music_blog', 5),
        ('music_watch_listen', 5),
        ('music_further', 3))

    priority_list = immutable.make_dict({
        'v1': priorities,
        'v2': priorities,
        'v3': priorities
    })

    template_names = immutable.make_dict({
        'v1': 'culture/sleeve-notes/v1',
        'v2': 'culture/sleeve-notes/v2',
        'v3': 'culture/sleeve-notes/v3',
        })

class CloseUp(handlers.EmailTemplate):
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

class Bookmarks(handlers.EmailTemplate):
    
    recognized_versions = immutable.make_list('v1')

    ad_tag = 'email-bookmarks'
    ad_config = immutable.make_dict({
        'leaderboard': 'Top',
        'leaderboard2': 'Bottom'
    })

    base_data_sources = immutable.make_dict({
        'books_picks': dss.culture.BooksEditorsPicks(client),
        'book_reviews': dss.culture.BookReviews(client),
        'books_blog': dss.culture.BooksBlog(client),
        'book_podcasts': dss.culture.BookPodcasts(client),
        'books_most_viewed': dss.culture.BooksMostViewed(client),
        'how_to_draw': dss.culture.HowToDraw(client),
    })

    data_sources = immutable.make_dict({
        'v1' : base_data_sources,
    })
 
    priority_list = immutable.make_dict({
        'v1': immutable.make_list(
            ('books_picks', 5),
            ('books_most_viewed', 3),
            ('book_reviews', 3),
            ('books_blog', 3),
            ('book_podcasts', 1),
            ('how_to_draw', 1))    
    })
    template_names = immutable.make_dict({
        'v1': 'culture/bookmarks/v1',
    })
