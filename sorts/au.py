import logging
import tags

def politics_first(a, b):
    a_has_tag = tags.has_tag("australia-news/australian-politics", a)
    b_has_tag = tags.has_tag("australia-news/australian-politics", b)

    if a_has_tag and not b_has_tag:
        return -1

    if not a_has_tag and b_has_tag:
        return 1

    return 0