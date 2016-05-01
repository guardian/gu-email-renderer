import unittest

import sorts

def create_item(id, tag_ids):
	return {
		"id": id,
		"tags" : [{"id": tag_id} for tag_id in tag_ids]
	}

class InapplicableSortTest(unittest.TestCase):

	def test_should_not_change_order(self):
		data = [{"id": "/1", "tags" : [{"id": 'world/asia-pacific'}]},
			{"id": "/2", "tags" : [{"id": 'world/asia-pacific'}]},]
		
		sorted_data = sorted(data, sorts.au.politics_first)

		self.assertEqual(data, sorted_data)

class ValidSortTest(unittest.TestCase):

	def test_politics_should_come_first(self):
		data = [
			create_item("/1", ["australia-news/australian-politics"]),
			create_item("/2", ["australia-news/victoria-politics"]),
			create_item("/3", ["australia-news/australian-politics"]),
			]

		expected_ids = ["/1", "/3", "/2"]

		sorted_data = sorted(data, sorts.au.politics_first)

		self.assertEqual([c["id"] for c in sorted_data], expected_ids)