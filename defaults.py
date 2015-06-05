import pysistence as immutable

content_item_fields = ['trailText',
	'headline',
	'liveBloggingNow',
	'standfirst',
	'commentable',
	'thumbnail',
	'byline']

MAX_MEMCACHE_LENGTH=1000000
CACHE_TIME=2*60