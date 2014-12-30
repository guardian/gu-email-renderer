import pysistence as immutable

import mail_renderer as mr

import data_source as ds
import data_sources as dss

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

class Bookmarks(mr.EmailTemplate):
    recognized_versions = immutable.make_list('v1')

    ad_tag = 'email-bookmarks'
    ad_config = immutable.make_dict({
        'leaderboard_v1': 'Top',
        'leaderboard_v2': 'Bottom'
    })

    base_data_sources = immutable.make_dict({
        'books_picks': dss.culture.BooksEditorsPicks(client),
        'book_reviews': dss.culture.BookReviews(client),
        'books_blog': dss.culture.BooksBlog(client),
        'book_podcasts': dss.culture.BookPodcasts(client),
        'books_most_viewed': dss.culture.BooksMostViewed(client),
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
            ('book_podcasts', 1),)    
    })
    template_names = immutable.make_dict({
        'v1': 'culture/bookmarks/v1',
    })