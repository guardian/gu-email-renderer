import mail_renderer as mr
from ophan_calls import OphanClient, MostSharedFetcher
from data_source import MultiContentDataSource, MostSharedCountInterpolator, MostSharedDataSource

def most_shared(client, ophan_client, country):
	return MostSharedDataSource(
		most_shared_fetcher=MostSharedFetcher(ophan_client, country=country),
		multi_content_data_source=MultiContentDataSource(client=client, name='most_shared'),
		shared_count_interpolator=MostSharedCountInterpolator()
	)