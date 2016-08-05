from data_source import MultiContentDataSource, OphanDataSource
from ophan_calls import MostPopularByTagFetcher

def mostPopularByTag(client, ophan_client, keywordTag):
	return OphanDataSource(
		client=client,
		multi_content_data_source=MultiContentDataSource(client=client, name='most_popular_by_tag'),
		fetcher=MostPopularByTagFetcher(ophan_client, keywordTag=keywordTag),
		n_items=4
	)