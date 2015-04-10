import re
import logging
import urllib, urlparse
import copy

first_paragraph_pattern = re.compile('.*?<p>(.+?)</p>.*', re.DOTALL | re.IGNORECASE)

def first_paragraph(text):
    match = first_paragraph_pattern.match(text)
    if match:
        return match.groups()[0].strip()
    else:
        logging.error('Failed to extract first paragraph from text: %s' % text)
        return text

def urlencode(url):
    return  urllib.quote_plus(url.encode('utf8'))

def largest_trail_image(content):
	thumbnails = [element for element in content['elements'] if element['relation'] == 'thumbnail']
	if not thumbnails:
		return {}

	def widest_image(current_largest_image, image):
		if not current_largest_image:
			return image

		if current_largest_image['typeData']['width'] > image['typeData']['width']:
			return current_largest_image
		return image

	largest_thumbnail = reduce(widest_image, thumbnails[0]['assets'])

	return largest_thumbnail

def largest_image(content):
	thumbnails = [element for element in content['elements'] if element['relation'] == 'main']
	if not thumbnails:
		return {}

	def widest_image(current_largest_image, image):
		if not current_largest_image:
			return image

		if current_largest_image['typeData']['width'] > image['typeData']['width']:
			return current_largest_image
		return image

	largest_thumbnail = reduce(widest_image, thumbnails[0]['assets'])

	return largest_thumbnail

def image_of_width(content, width, image_type='thumbnail'):
	images = [element for element in content['elements'] if element['relation'] == image_type]
	
	if not images:
		return None

	for image in images:
		if 'typeData' in image and 'width' in image['typeData'] and image['typeData']['width'] == str(width):
			return copy.deepcopy(image)

	return None
