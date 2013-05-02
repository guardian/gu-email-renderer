import re
import logging
import urllib, urlparse

first_paragraph_pattern = re.compile('.*?<p>(.+?)</p>.*', re.DOTALL | re.IGNORECASE)

def first_paragraph(text):
    match = first_paragraph_pattern.match(text)
    if match:
        return match.groups()[0].strip()
    else:
        logging.error('Failed to extract first paragraph from text: %s' % text)
        return text

def urlencode(url):
    return  urllib.quote_plus(url)

                                                                    