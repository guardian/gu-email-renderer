from pysistence import make_dict

import mail_renderer as mr

import data_source as ds
import data_sources as dss

client = mr.client

class FashionStatement(mr.EmailTemplate):
    recognized_versions = ['v1', 'v2', 'v3']

    ad_tag = 'email-fashion-statement'
    ad_config = {
        'leaderboard_v1': 'Top',
        'leaderboard_v2': 'Bottom'
    }

    base_data_sources = make_dict({
        'fashion_gallery': dss.fashion.FashionGalleryDataSource(client),
		'fashion_most_viewed': dss.fashion.FashionMostViewedDataSource(client),
        'fashion_jcm_on_fashion' : dss.fashion.JCMOnFashion(client)
 
	})

    data_sources = {
    	'v1' : base_data_sources.using(
    		fashion_news = dss.fashion.FashionNewsDataSource(client),
    		fashion_hadley = dss.fashion.FashionAskHadleyDataSource(client),
    		fashion_blog = dss.fashion.FashionBlogDataSource(client),
            fashion_network = dss.fashion.FashionNetworkDataSource(client),
    		),
        'v3': base_data_sources.using(
            fashion_picks = dss.fashion.FashionEditorsPicksDataSource(client),
            fashion_hadley = dss.fashion.FashionAskHadleyDataSource(client),
            fashion_sali = dss.fashion.FashionSaliHughesDataSource(client),
            fashion_stylewatch = dss.fashion.FashionStylewatchDataSource(client),
            fashion_most_viewed = dss.fashion.FashionMostViewedDataSource(client),
        	)
    }
    data_sources['v2'] = data_sources['v1']

    priority_list = {
        'v1': [('fashion_hadley', 1), ('fashion_most_viewed', 6), ('fashion_news', 3), ('fashion_blog', 6), ('fashion_network', 6), ('fashion_gallery', 1)],
        'v3': [('fashion_hadley', 1), ('fashion_sali', 1), ('fashion_stylewatch', 1), ('fashion_picks', 5), ('fashion_most_viewed', 6), ('fashion_gallery', 1)]
    }
    priority_list['v2'] = priority_list['v1']

    template_names = {'v1': 'fashion-statement-v1', 'v2': 'fashion-statement-v2', 'v3': 'fashion-statement-v3'}
