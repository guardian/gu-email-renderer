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

def largest_image(content, image_type='thumbnail'):

	if not 'elements' in content:
		logging.debug(content)
		return None

	images = [element for element in content['elements'] if element['relation'] == image_type]
	if not images:
		return None

	def widest_image(current_largest_image, image):
		if not current_largest_image:
			return image

		if current_largest_image['typeData']['width'] > image['typeData']['width']:
			return current_largest_image
		return image

	biggest_image = reduce(widest_image, images[0]['assets'])
	return biggest_image

def image_of_width(content, target_width, image_type='thumbnail'):
	images = [element for element in content['elements'] if element['relation'] == image_type]
	assets = images[0].get('assets', [])

	if not assets:
		return None

	for asset in assets:
		width = asset.get('typeData', {}).get('width', None)
		if width and width == str(target_width):
			return copy.deepcopy(asset)

	return None

def asset_url(asset):
	if not asset:
		return None

	return asset.get('typeData', {}).get('secureFile', None)