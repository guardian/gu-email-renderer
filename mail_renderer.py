import os
import logging

import webapp2

from guardianapi.apiClient import ApiClient

import configuration
import handlers

# TODO: Hide me away somewhere warm and secret.
api_key = configuration.read('CAPI_KEY')
ophan_key = configuration.read('OPHAN_API_KEY')
base_url=configuration.read('CAPI_BASE_URL')
ophan_base_url = configuration.read('OPHAN_BASE_URL')
discussion_base_url = 'https://discussion.guardianapis.com/discussion-api/'

client = ApiClient(base_url, api_key, edition="uk")
clientUS = ApiClient(base_url, api_key, edition='us')
clientAUS = ApiClient(base_url, api_key, edition='au')

# Super dirty
# import now after the common functionality of this module is defined
# The result of script execution flow

import email_definitions as emails

app = webapp2.WSGIApplication([('/daily-email/(.+)', emails.uk.DailyEmail),
                               ('/daily-email-us/(.+)', emails.us.DailyEmailUS),
                               ('/daily-email-aus/(.+)', emails.au.DailyEmailAUS),
                               ('/australian-politics/(.+)', emails.au.Politics),
                               ('/australian-cif/(.+)', emails.au.CommentIsFree),
                               ('/australia-morning/(.+)', emails.au.Morning),
                               ('/australia-sport/(.+)', emails.au.Sport),
                               ('/us-opinion/(.+)', emails.us.Opinion),
                               ('/close-up/(.+)', emails.culture.CloseUp),
                               ('/fashion-statement/(.+)', emails.fashion.FashionStatement),
                               ('/media-briefing/(.+)', emails.media.MediaBriefing),
                               ('/sleeve-notes/(.+)', emails.culture.SleeveNotes),
                               ('/bookmarks/(.+)', emails.culture.Bookmarks),
                               ('/comment-is-free/(.+)', emails.cif.CommentIsFree),
                               ('/film-today/(.+)', emails.culture.FilmToday),
                               ('/the-flyer/(.+)', emails.travel.TheFlyer),
                               ('/zip-file/(.+)', emails.technology.ZipFile),
                               ('/most-commented/(.+)', emails.developer.MostCommented),
                               ('/most-shared/uk/(.+)', emails.most_shared.MostSharedUK),
                               ('/most-shared/us/(.+)', emails.most_shared.MostSharedUS),
                               ('/most-shared/au/(.+)', emails.most_shared.MostSharedAU),
                               ('/most-shared/(.+)', emails.most_shared.MostShared),
                               ('/most-viewed/(.+)', emails.developer.MostViewed),
                               ('/editors-picks/(.+)', emails.developer.EditorsPicks),
                               ('/longreads/(.+)', emails.long_reads.LongReads),
                               webapp2.Route(r'/headline', handler=emails.developer.Headline),
                               webapp2.Route(r'/headline/film', handler=emails.developer.FilmHeadline),
                               webapp2.Route(r'/headline/<edition>', handler=emails.developer.Headline),
                               webapp2.Route(r'/', handler=handlers.Index)],
                              debug=True)
