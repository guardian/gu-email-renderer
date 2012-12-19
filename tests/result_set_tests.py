from data_source import take_unique_subsets

def test_should_be_able_to_dedupe_result_sets():

    size = 3
    data = {
        'sport': [{'id': 6}, {'id': 7}, {'id': 8}, {'id': 9}, {'id': 10}, {'id': 11}],
        'chess': [{'id': 1}, {'id': 2}, {'id': 3}, {'id': 4}],
        'news': [{'id': 3}, {'id': 4}, {'id': 5}, {'id': 6}, {'id': 7}, {'id': 8}],
        'travel': [{'id': 9}, {'id': 10}, {'id': 11}, {'id': 12}]}

    priority_list = ['chess', 'news', 'sport', 'travel']

    deduped_data = take_unique_subsets(size, data, priority_list)

    assert deduped_data['chess'] == [{'id': 1}, {'id': 2}, {'id': 3}]
    assert deduped_data['news'] == [{'id': 4}, {'id': 5}, {'id': 6}]
    assert deduped_data['sport'] == [{'id': 7}, {'id': 8}, {'id': 9}]
    assert deduped_data['travel'] == [{'id': 10}, {'id': 11}, {'id': 12}]

def test_we_never_show_dupes_even_if_we_run_out_of_items():
    size = 4
    data = {
        'sport': [{'id': 6}, {'id': 7}, {'id': 8}, {'id': 9}, {'id': 10}, {'id': 11}],
        'chess': [{'id': 1}, {'id': 2}, {'id': 3}, {'id': 4}],
        'news': [{'id': 3}, {'id': 4}, {'id': 5}, {'id': 6}, {'id': 7}, {'id': 8}],
        'travel': [{'id': 9}, {'id': 10}, {'id': 11}, {'id': 12}]}

    priority_list = ['chess', 'news', 'sport', 'travel']

    deduped_data = take_unique_subsets(size, data, priority_list)

    assert deduped_data['chess'] == [{'id': 1}, {'id': 2}, {'id': 3}, {'id': 4}]
    assert deduped_data['news'] == [{'id': 5}, {'id': 6}, {'id': 7}, {'id': 8}]
    assert deduped_data['sport'] == [{'id': 9}, {'id': 10}, {'id': 11}]
    assert deduped_data['travel'] == [{'id': 12}]


if __name__ == '__main__':
    test_should_be_able_to_dedupe_result_sets()
    test_we_never_show_dupes_even_if_we_run_out_of_items()