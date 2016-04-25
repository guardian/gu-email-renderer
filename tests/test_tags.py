import unittest

import tags

class TestTags(unittest.TestCase):

    def test_should_detect_whether_a_tag_present(self):
    	stub_content_item = {
    		'tags': [
	    		{
	    			'id': 'world/syria'
	    		}
    		]
    	}

    	self.assertTrue(tags.has_tag('world/syria', stub_content_item))

    def test_should_detect_whether_a_tag_is_absent(self):
    	pass
