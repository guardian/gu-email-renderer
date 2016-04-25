import unittest

import tags

stub_content_item = {
	'tags': [
		{
			'id': 'world/syria'
		}
	]
}

class TestTags(unittest.TestCase):

    def test_should_detect_whether_a_tag_present(self):
    	self.assertTrue(tags.has_tag('world/syria', stub_content_item))

    def test_should_detect_whether_a_tag_is_absent(self):
    	self.assertFalse(tags.has_tag('world/iraq', stub_content_item))
