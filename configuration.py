# -*- coding: utf-8 -*- 

from google.appengine.ext import ndb

class Configuration(ndb.Model):
	key = ndb.StringProperty(required=True)
	value = ndb.StringProperty(required=True)

def read(key, default=None):
	results = Configuration.query(Configuration.key == key)

	if not results.iter().has_next():
		return default

	key_value = results.iter().next().value

	return key_value

def write(key, value):
	config = Configuration(id=key, key=key, value=value)
	config.put()
	return config

# You cannot edit the datastore locally without something in it!
# Write this key so we can view/edit stuff (the value is not used)
write("TEST", "test")