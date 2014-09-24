import unittest
from data_source import build_unique_trailblocks


class TestResultSets(unittest.TestCase):

    def test_should_be_able_to_dedupe_result_sets(self):
        size = 3
        data = {
            'sport': [{'id': 6}, {'id': 7}, {'id': 8}, {'id': 9}, {'id': 10}, {'id': 11}],
            'chess': [{'id': 1}, {'id': 2}, {'id': 3}, {'id': 4}],
            'news': [{'id': 3}, {'id': 4}, {'id': 5}, {'id': 6}, {'id': 7}, {'id': 8}],
            'travel': [{'id': 9}, {'id': 10}, {'id': 11}, {'id': 12}]}

        priority_list = [('chess', 2), ('news', 4), ('sport', 1), ('travel', 3)]

        deduped_data = build_unique_trailblocks(data, priority_list)

        self.assertEquals(deduped_data['chess'], [{'id': 1}, {'id': 2}])
        self.assertEquals(deduped_data['news'], [{'id': 3}, {'id': 4}, {'id': 5}, {'id': 6}])
        self.assertEquals(deduped_data['sport'], [{'id': 7}])
        self.assertEquals(deduped_data['travel'], [{'id': 9}, {'id': 10}, {'id': 11}])

    def test_we_never_show_dupes_even_if_we_run_out_of_items(self):
        size = 4
        data = {
            'sport': [{'id': 6}, {'id': 7}, {'id': 8}, {'id': 9}, {'id': 10}, {'id': 11}],
            'chess': [{'id': 1}, {'id': 2}, {'id': 3}, {'id': 4}],
            'news': [{'id': 3}, {'id': 4}, {'id': 5}, {'id': 6}, {'id': 7}, {'id': 8}],
            'travel': [{'id': 9}, {'id': 10}, {'id': 11}, {'id': 12}]}

        priority_list = [('chess', size), ('news', size), ('sport', size), ('travel', size)]

        deduped_data = build_unique_trailblocks(data, priority_list)

        self.assertEquals(deduped_data['chess'], [{'id': 1}, {'id': 2}, {'id': 3}, {'id': 4}])
        self.assertEquals(deduped_data['news'], [{'id': 5}, {'id': 6}, {'id': 7}, {'id': 8}])
        self.assertEquals(deduped_data['sport'], [{'id': 9}, {'id': 10}, {'id': 11}])
        self.assertEquals(deduped_data['travel'], [{'id': 12}])
