
def safeget(dct, page_type, *keys):
    for key in keys:
        try:
            dct = dct[key]
        except KeyError:
            logging.error("Could not extract poster image and alt text for  " + page_type + + dict)
            return None
    return dct