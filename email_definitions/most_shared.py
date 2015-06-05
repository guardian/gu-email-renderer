import mail_renderer as mr
from ophan_calls import OphanClient, MostSharedFetcher
from data_source import MultiContentDataSource, MostSharedCountInterpolator, MostSharedDataSource

import data_sources as dss

ophan_client = OphanClient(mr.ophan_base_url, mr.ophan_key)

class MostShared(mr.EmailTemplate):
	recognized_versions = ['v1']
	n_items = 6

	most_shared_fetcher = MostSharedFetcher(ophan_client)
	multi_content_data_source = MultiContentDataSource(client=mr.client, name='most_shared')
	shared_count_interpolator = MostSharedCountInterpolator()

	most_shared_data_source = MostSharedDataSource(
		most_shared_fetcher=most_shared_fetcher,
		multi_content_data_source=multi_content_data_source,
		shared_count_interpolator=shared_count_interpolator
	)

	data_sources = {}
	data_sources['v1'] = {
		'most_shared': most_shared_data_source
		}

	ad_tag = ''
	ad_config = {}

	priority_list = {'v1': [('most_shared', n_items)]}
	template_names = {'v1': 'most-shared'}

class MostSharedUK(MostShared):

	data_sources = {
		'v1' :  {
			'most_shared': MostSharedDataSource(
				most_shared_fetcher=MostSharedFetcher(ophan_client, country='gb'),
				multi_content_data_source=MultiContentDataSource(client=mr.client, name='most_shared'),
				shared_count_interpolator=MostSharedCountInterpolator()
			),
		},
	}

class MostSharedAU(MostShared):

	data_sources = {
		'v1' :  {
			'most_shared': dss.social.most_shared(mr.client, ophan_client, 'au'),
		},
	}

class MostSharedUS(MostShared):

	data_sources = {
		'v1' :  {
			'most_shared': MostSharedDataSource(
				most_shared_fetcher=MostSharedFetcher(ophan_client, country='us'),
				multi_content_data_source=MultiContentDataSource(client=mr.client, name='most_shared'),
				shared_count_interpolator=MostSharedCountInterpolator()
			),
		},
	}
