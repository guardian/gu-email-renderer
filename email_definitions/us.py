import mail_renderer as mr

from data_source import BusinessDataSource, TechnologyDataSource, \
	CommentIsFreeDataSource, CultureDataSource, TopStoriesDataSource, \
	VideoDataSource

from data_sources import us as data

clientUS = mr.clientUS

class DailyEmailUS(mr.EmailTemplate):
    recognized_versions = ['v1', 'v3', ]

    ad_tag = 'email-guardian-today-us'
    ad_config = {
        'leaderboard_v1': 'Top',
        'leaderboard_v2': 'Bottom'
    }

    data_sources = {}
    data_sources['v1'] = {
        'business': BusinessDataSource(clientUS),
        'money': data.USMoneyDataSource(clientUS),
        'technology': TechnologyDataSource(clientUS),
        'sport': data.SportUSDataSource(clientUS),
        'comment': CommentIsFreeDataSource(clientUS),
        'culture': CultureDataSource(clientUS),
        'top_stories': TopStoriesDataSource(clientUS),
        'video': VideoDataSource(clientUS),
        }
    data_sources['v3'] = {
        'business': BusinessDataSource(clientUS),
        'money': data.USMoneyDataSource(clientUS),
        'technology': TechnologyDataSource(clientUS),
        'sport': data.SportUSDataSource(clientUS),
        'comment': CommentIsFreeDataSource(clientUS),
        'culture': CultureDataSource(clientUS),
        'top_stories': TopStoriesDataSource(clientUS),
        'video': VideoDataSource(clientUS),
        }

    priority_list = {}
    priority_list['v1'] = [('top_stories', 6), ('video', 3), ('sport', 3), ('comment', 3),
                           ('culture', 3), ('business', 2), ('money', 2), ('technology', 2)]
    priority_list['v2'] = [('top_stories', 6), ('video', 3), ('sport', 3), ('comment', 3),
                           ('culture', 3), ('business', 2), ('money', 2), ('technology', 2)]
    priority_list['v3'] = [('top_stories', 6), ('video', 3), ('sport', 3), ('comment', 3),
                           ('culture', 3), ('business', 2), ('money', 2), ('technology', 2)]
    priority_list['MPU_v1a'] = [('top_stories', 6), ('video', 3), ('sport', 3), ('comment', 3),
                           ('culture', 3), ('business', 2), ('money', 2), ('technology', 2)]
    priority_list['MPU_v1b'] = [('top_stories', 6), ('video', 3), ('sport', 3), ('comment', 3),
                           ('culture', 3), ('business', 2), ('money', 2), ('technology', 2)]

    template_names = {'v1': 'daily-email-us', 'v2': 'daily-email-us-v2', 'v3': 'daily-email-us-v3', 'MPU_v1a': 'daily-email-us-v4', 'MPU_v1b': 'daily-email-us-v5'}
