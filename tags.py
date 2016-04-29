
def has_tag(tag_id, content_item):
	if not 'tags' in content_item:
		return false

	return tag_id in [tag['id'] for tag in content_item['tags']]