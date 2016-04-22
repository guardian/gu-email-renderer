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

def get_image(content, image_type='thumbnail', max_width=None):
	if not 'elements' in content:
		logging.debug(content)
		return None

	images = [element for element in content['elements'] if element['relation'] == image_type]

	if not images:
		return None

	def too_big(image):
		width = int(image['typeData']['width'])
		return max_width and width > max_width

	def best_image(current_best_image, image):
		if not current_best_image:
			return image

		if current_best_image['typeData']['width'] > image['typeData']['width']:
			return current_best_image
		return image

	def smallest_image(current_smallest_image, image):
		if not current_smallest_image:
			return image

		if current_smallest_image['typeData']['width'] < image['typeData']['width']:
			return current_smallest_image

		return image

	all_assets = [asset for asset in images[0]['assets']]

	if not all_assets:
		logging.warning("No image assets found for content item: {}".format(content.get("id", "Unknown")))

	filtered_assets = [asset for asset in all_assets if not too_big(asset)]

	if not filtered_assets and all_assets:
		return reduce(smallest_image, all_assets)

	biggest_image = reduce(best_image, filtered_assets)
	return biggest_image

def get_tone(content):
	d = {d["type"]: dict(d, index=i) for (i, d) in enumerate(content["tags"])}
	if "tone" in d:
		return d["tone"]["id"]
	else:
		return "Article"

def get_keyword(content):
	for tag in content["tags"]:
		if tag["type"] == "keyword" and "sectionId" in tag and tag["id"].split("/")[1] != tag["sectionId"]:
			return tag["webTitle"]
	return "Article"

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