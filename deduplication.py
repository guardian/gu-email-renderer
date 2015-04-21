
def build_unique_trailblocks(data, priority_list, excluded=None):
    """
    data is a map of type string->list list is a list of maps each of
    which contains the field 'id'.  priority_list is a list of pairs:
    (name, number). <name> is the is a key in data (the name of a
    datasource) and <number> is the number of items to take from the
    datasource.
    """

    items_seen_so_far = set()
    unique_subsets = {}

    for (data_set_name, size) in priority_list:

        if excluded and data_set_name in excluded:
            unique_subsets[data_set_name] = data[data_set_name]
            continue

        unique_subset = []
        unique_subsets[data_set_name] = unique_subset
        source_data = data[data_set_name]
        for item in source_data:
            if item['id'] not in items_seen_so_far and len(unique_subset) < size:
                unique_subset.append(item)
                items_seen_so_far.add(item['id'])

    return unique_subsets