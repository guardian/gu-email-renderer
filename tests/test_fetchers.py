from urllib2 import urlparse
import urllib
import simplejson

Status = """
        {'status': '200', 'content-length': '10614', 'x-content-api-build': '1998', 'proxy-connection': 'keep-alive',
         'vary': 'Accept,Accept-Encoding', 'x-lift-version': '2.4', 'x-gu-jas': 'ea12a9802fea0a87cff65d3d23752cec!600461558@qtp-1761506447-286',
         'keep-alive': '60', 'expires': 'Tue, 18 Dec 2012 15:19:33 GMT', 'server': 'Mashery Proxy', 'date': 'Tue, 18 Dec 2012 15:18:33 GMT',
         '-content-encoding': 'gzip', 'cache-control': 'max-age=20', 'x-gu-httpd': 'ea12a9802fea0a87cff65d3d23752cec', 'x-mashery-responder': 'prod-p-worker-eu-west-1a-14.mashery.com',
         'content-type': 'application/json; charset=utf-8',
         'content-location': 'http://content.guardianapis.com/search?page-size=10&format=json&section=culture&api-key=***REMOVED***&tag=type%2Farticle&show-fields=trailText%2Cheadline%2CliveBloggingNow%2Cstandfirst%2Ccommentable%2Cthumbnail%2Cbyline'}
        """

ContentResponse = """
            {
              "response":{
                "status":"ok",
                "userTier":"internal",
                "total":1,
                "content":{
                  "id":"content_1",
                  "sectionId":"cif",
                  "sectionName":"cif name",
                  "webPublicationDate":"2013-04-09T07:00:09Z",
                  "webTitle":"Toynbee speaks",
                  "webUrl":"http://www.theguardian.com/technology/gamesblog/2013/apr/09/press-start-game-news",
                  "apiUrl":"http://content.guardianapis.com/technology/gamesblog/2013/apr/09/press-start-game-news",
                  "fields":{
                    "trailText":"Stuff happened",
                    "headline":"More stuff happened",
                    "standfirst":"Stand by your man",
                    "thumbnail":"thumb piano",
                    "commentable":"true",
                    "byline":"Keith",
                    "liveBloggingNow":"false"
                  }
                }
              }
            }
            """

BlogItemResponse = """
            {
              "response": {
                "status": "ok",
                "userTier": "internal",
                "total": 1,
                "results": [
                  {
                    "id": "blog id",
                    "sectionId": "blog section id",
                    "sectionName": "blog section name",
                    "webPublicationDate": "2013-05-23T10:38:18Z",
                    "webTitle": "Jeremy Hunt under fire over GP reforms: Politics live blog",
                    "webUrl": "http://www.theguardian.com/politics/blog/2013/may/23/jeremy-hunt-gp-reforms-politics",
                    "apiUrl": "http://content.guardianapis.com/politics/blog/2013/may/23/jeremy-hunt-gp-reforms-politics",
                    "fields": {
                      "trailText": "<p><strong>Andrew Sparrow</strong>'s rolling coverage of all the day's political developments as they happen, including Jeremy Hunt's speech on GP reforms</p>",
                      "headline": "Jeremy Hunt under fire over GP reforms: Politics live blog",
                      "standfirst": "Rolling coverage of all the day's political developments as they happen, including Jeremy Hunt's speech on GP reforms",
                      "thumbnail": "http://static.guim.co.uk/sys-images/Guardian/Pix/pictures/2013/5/23/1369295845937/40ab0163-022a-410b-9b6b-99de396bd91b-140x84.jpeg",
                      "byline": "Andrew Sparrow",
                      "commentable": "true",
                      "liveBloggingNow": "true"
                    }
                  }
                ]
              }
            }
            """
BlogItemsResponse = """
            {
              "response": {
                "status": "ok",
                "userTier": "internal",
                "total": 1,
                "results": [
                  {
                    "id": "blog id 1",
                    "sectionId": "blog section id",
                    "sectionName": "blog section name",
                    "webPublicationDate": "2013-05-23T10:38:18Z",
                    "webTitle": "Jeremy Hunt under fire over GP reforms: Politics live blog",
                    "webUrl": "http://www.theguardian.com/politics/blog/2013/may/23/jeremy-hunt-gp-reforms-politics",
                    "apiUrl": "http://content.guardianapis.com/politics/blog/2013/may/23/jeremy-hunt-gp-reforms-politics",
                    "fields": {
                      "trailText": "<p><strong>Andrew Sparrow</strong>'s rolling coverage of all the day's political developments as they happen, including Jeremy Hunt's speech on GP reforms</p>",
                      "headline": "Jeremy Hunt under fire over GP reforms: Politics live blog",
                      "standfirst": "Rolling coverage of all the day's political developments as they happen, including Jeremy Hunt's speech on GP reforms",
                      "thumbnail": "http://static.guim.co.uk/sys-images/Guardian/Pix/pictures/2013/5/23/1369295845937/40ab0163-022a-410b-9b6b-99de396bd91b-140x84.jpeg",
                      "byline": "Andrew Sparrow",
                      "commentable": "true",
                      "liveBloggingNow": "true"
                    }
                  },
                  {
                    "id": "blog id 2",
                    "sectionId": "blog section id",
                    "sectionName": "blog section name",
                    "webPublicationDate": "2013-05-23T10:38:18Z",
                    "webTitle": "Jeremy Hunt under fire over GP reforms: Politics live blog",
                    "webUrl": "http://www.theguardian.com/politics/blog/2013/may/23/jeremy-hunt-gp-reforms-politics",
                    "apiUrl": "http://content.guardianapis.com/politics/blog/2013/may/23/jeremy-hunt-gp-reforms-politics",
                    "fields": {
                      "trailText": "<p><strong>Andrew Sparrow</strong>'s rolling coverage of all the day's political developments as they happen, including Jeremy Hunt's speech on GP reforms</p>",
                      "headline": "Jeremy Hunt under fire over GP reforms: Politics live blog",
                      "standfirst": "Rolling coverage of all the day's political developments as they happen, including Jeremy Hunt's speech on GP reforms",
                      "thumbnail": "http://static.guim.co.uk/sys-images/Guardian/Pix/pictures/2013/5/23/1369295845937/40ab0163-022a-410b-9b6b-99de396bd91b-140x84.jpeg",
                      "byline": "Andrew Sparrow",
                      "commentable": "true",
                      "liveBloggingNow": "true"
                    }
                  }
                ]
              }
            }
            """

EmptyBlogItemResponse = """
            {
              "response": {
                "status": "ok",
                "userTier": "internal",
                "total": 1,
                "results": []
              }
            }
            """

SectionResponse = """
        {
          "response": {
            "status": "ok",
            "userTier": "internal",
            "total": 1,
            "results": [
              {
                "id": "section id",
                "sectionId": "politics",
                "sectionName": "Politics",
                "webPublicationDate": "2013-05-23T11:11:20Z",
                "webTitle": "Jeremy Hunt under fire over GP reforms: Politics live blog",
                "webUrl": "http://www.theguardian.com/politics/blog/2013/may/23/jeremy-hunt-gp-reforms-politics",
                "apiUrl": "http://content.guardianapis.com/politics/blog/2013/may/23/jeremy-hunt-gp-reforms-politics",
                "fields": {
                  "trailText": "<p><strong>Andrew Sparrow</strong>'s rolling coverage of all the day's political developments as they happen, including Jeremy Hunt's speech on GP reforms</p>",
                  "headline": "Jeremy Hunt under fire over GP reforms: Politics live blog",
                  "standfirst": "Rolling coverage of all the day's political developments as they happen, including Jeremy Hunt's speech on GP reforms",
                  "thumbnail": "http://static.guim.co.uk/sys-images/Guardian/Pix/pictures/2013/5/23/1369295845937/40ab0163-022a-410b-9b6b-99de396bd91b-140x84.jpeg",
                  "commentable": "true",
                  "byline": "Andrew Sparrow",
                  "liveBloggingNow": "true"
                }
              },
              {
                "id": "section id 2",
                "sectionId": "politics",
                "sectionName": "Politics",
                "webPublicationDate": "2013-05-22T22:06:01Z",
                "webTitle": "Hugh Muir's Diary: Trouble behind the curtains in Green-land as members protest at EU selection",
                "webUrl": "http://www.theguardian.com/politics/2013/may/22/hugh-muir-diary-green-show-trial",
                "apiUrl": "http://content.guardianapis.com/politics/2013/may/22/hugh-muir-diary-green-show-trial",
                "fields": {
                  "trailText": "<strong>Hugh Muir:</strong> A question for parties everywhere: how Green was my election?<br /><br />",
                  "headline": "Diary: Trouble behind the curtains in Green-land as members protest at EU selection",
                  "standfirst": "A question for parties everywhere: how Green was my election?",
                  "thumbnail": "http://static.guim.co.uk/sys-images/Guardian/Pix/pictures/2013/5/22/1369243720648/GERALD-RATNER--003.jpg",
                  "commentable": "false",
                  "byline": "Hugh Muir",
                  "liveBloggingNow": "false"
                }
              },
              {
                "id": "politics/2013/may/22/david-cameron-placate-swivel-eyed-loons",
                "sectionId": "politics",
                "sectionName": "Politics",
                "webPublicationDate": "2013-05-22T19:00:00Z",
                "webTitle": "David Cameron tries to placate the swivel-eyed loons with his natural leadership skills",
                "webUrl": "http://www.theguardian.com/politics/2013/may/22/david-cameron-placate-swivel-eyed-loons",
                "apiUrl": "http://content.guardianapis.com/politics/2013/may/22/david-cameron-placate-swivel-eyed-loons",
                "fields": {
                  "trailText": "<p>Tory activists are incensed. But surely a nicely phrased letter will calm them down</p>",
                  "headline": "David Cameron tries to placate the swivel-eyed loons with his natural leadership skills",
                  "standfirst": "Tory activists are incensed. But surely a message of thanks and appreciation will calm them down",
                  "thumbnail": "http://static.guim.co.uk/sys-images/Guardian/Pix/pictures/2013/5/22/1369241033203/Swivel-on-this-Lord-Feldm-005.jpg",
                  "commentable": "true",
                  "byline": "John Crace",
                  "liveBloggingNow": "false"
                }
              }
              ]
            }
        }
        """




class ContentIdRememberingStubClient(object):
    def __init__(self):
        self.content_ids = []

    def content_query(self, content_id, **criteria):
        self.content_ids.append(content_id)

        json =  simplejson.loads(ContentResponse)
        results = []
        if json['response'].has_key('content'):
            results = [json['response']['content']]

        return results

class MultiCalledApiStubFetcher(object):

    def __init__(self):
        self.blog_content_requested = False
        self.content_requested = False

    status = Status

    def get( self, url):
        (_, _, path, _, query, _) = urlparse.urlparse(url)
        if path == "/i/am/content":
            self.content_requested = True
            return (self.status, "{}")



class ApiStubFetcher(object):

    status = Status

    def get(self, url):
        (_, _, path, _, query, _) = urlparse.urlparse(url)
        if path == '/i/am/a/short/url':
            return self.content_result()
        if path == '/search':
            return self.search_results()
        if path == '/sport':
            return self.sport_results()
        if 'show-editors-picks' in query:
            return self.editors_picks_results()
        if 'show-most-viewed' in query:
            return self.most_viewed_results()
        if path == '/i/want/a/blog/item':
            return self.blog_item_response()
        if path == '/i/want/a/empty/blog/item':
            return self.empty_blog_item()
        if path == '/i/want/blog/items':
            return self.several_blog_items()
        if path == '/i/want/a/section':
            return self.section_response()


    def content_result(self):
        response = ContentResponse
        return (self.status, response)

    def section_response(self):
        response =  SectionResponse
        return (self.status, response)

    def blog_item_response(self):
        response = BlogItemResponse
        return(self.status, response)

    def several_blog_items(self):
        response = BlogItemsResponse
        return (self.status, response)

    def empty_blog_item(self):
        response = EmptyBlogItemResponse
        return (self.status, response)

    def most_viewed_results(self):
        response = """
            {
              "response":{
                "status":"ok",
                "userTier":"internal",
                "total":1,
                "results":[{
                    "id":"sport/video/2013/jan/09/relay-runners-start-brawl-video",
                    "sectionId":"sport",
                    "sectionName":"Sport",
                    "webPublicationDate":"2013-01-09T16:15:38Z",
                    "webTitle":"4x400m relay runners start brawl mid-race \u2013 video",
                    "webUrl":"http://www.theguardian.com/sport/video/2013/jan/09/relay-runners-start-brawl-video",
                    "apiUrl":"http://content.guardianapis.com/sport/video/2013/jan/09/relay-runners-start-brawl-video",
                    "fields":{
                      "trailText":"<p>Athletics and mid-race brawling don't usually go hand in hand, so spectators were surprised by action at the Hispanic Games at the New York Armory</p>",
                      "headline":"4x400m relay runners start brawl mid-race \u2013 video",
                      "standfirst":"Athletics and mid-race fighting don't usually go hand in hand, so spectators were surprised to witness Mt. Vernon High runner Rai Benjamin being taken out by an unidentified runner from Thomas Jefferson High School during the Hispanic Games at the New York Armory last weekend. Benjamin had been knocked off course when he ran into a different TJHS runner. Bizarrely, the incident seems to be ignored by race officials and the race continues as if nothing has happened",
                      "thumbnail":"http://static.guim.co.uk/sys-images/Guardian/Pix/audio/video/2013/1/9/1357742154408/4x400-metre-relay-runners-005.jpg",
                      "commentable":"false",
                      "liveBloggingNow":"false"
                    }
                  }],
                  "editorsPicks":[{
                  "id":"world/2012/dec/18/anti-polio-workers-shot-pakistan",
                  "sectionId":"world",
                  "sectionName":"World news",
                  "webPublicationDate":"2012-12-18T10:08:46Z",
                  "webTitle":"Anti-polio workers shot dead in Pakistan",
                  "webUrl":"http://www.theguardian.com/world/2012/dec/18/anti-polio-workers-shot-pakistan",
                  "apiUrl":"http://content.guardianapis.com/world/2012/dec/18/anti-polio-workers-shot-pakistan",
                  "fields":{
                    "trailText":"<p>Five women killed and two men injured in attacks this week raising fears for drive to eradicate crippling disease</p>",
                    "headline":"Anti-polio workers shot dead in Pakistan",
                    "standfirst":"Five women killed and two men injured in attacks this week raising fears for drive to eradicate crippling disease",
                    "thumbnail":"http://static.guim.co.uk/sys-images/Guardian/About/General/2012/12/18/1355824995156/Polio-campaign-003.jpg",
                    "commentable":"false",
                    "byline":"Agencies in Karachi",
                    "liveBloggingNow":"false"
                  }
                }],
                "mostViewed":[{
                  "id":"world/2012/dec/17/white-house-obama-gun-control-newtown",
                  "sectionId":"world",
                  "sectionName":"World news",
                  "webPublicationDate":"2012-12-17T20:24:00Z",
                  "webTitle":"White House says Obama will move swiftly on gun control after Newtown",
                  "webUrl":"http://www.theguardian.com/world/2012/dec/17/white-house-obama-gun-control-newtown",
                  "apiUrl":"http://content.guardianapis.com/world/2012/dec/17/white-house-obama-gun-control-newtown",
                  "fields":{
                    "trailText":"<p>First signs that Democrats are willing to take on pro-gun lobby as even NRA-endorsed senator Joe Manchin says 'we need action'</p>",
                    "headline":"White House says Obama will move swiftly on gun control after Newtown",
                    "standfirst":"First signs that Democrats are willing to take on pro-gun lobby as even NRA-endorsed senator Joe Manchin says 'we need action'",
                    "thumbnail":"http://static.guim.co.uk/sys-images/Guardian/Pix/maps_and_graphs/2012/12/17/1355705992584/Barack-Obama-attends-a-vi-005.jpg",
                    "commentable":"true",
                    "byline":"Ewen MacAskill in Washington",
                    "liveBloggingNow":"false"
                  }
                },{
                  "id":"uk/2012/dec/18/antarctic-territory-queen-cabinet",
                  "sectionId":"uk",
                  "sectionName":"UK news",
                  "webPublicationDate":"2012-12-18T14:07:09Z",
                  "webTitle":"Antarctic territory named for the Queen as monarch attends cabinet",
                  "webUrl":"http://www.theguardian.com/uk/2012/dec/18/antarctic-territory-queen-cabinet",
                  "apiUrl":"http://content.guardianapis.com/uk/2012/dec/18/antarctic-territory-queen-cabinet",
                  "fields":{
                    "trailText":"Queen Elizabeth Land, table mats and hope of a shorter speech among jubilee gifts in first cabinet visit by a monarch since 1781",
                    "headline":"Antarctic territory named for the Queen as monarch attends cabinet",
                    "standfirst":"Queen Elizabeth Land, table mats and hope of a shorter speech among jubilee gifts in first cabinet visit by a monarch since 1781",
                    "thumbnail":"http://static.guim.co.uk/sys-images/Guardian/Pix/pictures/2012/12/18/1355838771424/Queen-attends-cabinet-mee-003.jpg",
                    "commentable":"true",
                    "byline":"Patrick Wintour, political editor",
                    "liveBloggingNow":"false"
                  }
                }]}}
        """

        return (self.status, response)

    def editors_picks_results(self):
        response = """
            {
              "response":{
                "status":"ok",
                "userTier":"internal",
                "total":1,
                "results":[{
                    "id":"sport/video/2013/jan/09/relay-runners-start-brawl-video",
                    "sectionId":"sport",
                    "sectionName":"Sport",
                    "webPublicationDate":"2013-01-09T16:15:38Z",
                    "webTitle":"4x400m relay runners start brawl mid-race \u2013 video",
                    "webUrl":"http://www.theguardian.com/sport/video/2013/jan/09/relay-runners-start-brawl-video",
                    "apiUrl":"http://content.guardianapis.com/sport/video/2013/jan/09/relay-runners-start-brawl-video",
                    "fields":{
                      "trailText":"<p>Athletics and mid-race brawling don't usually go hand in hand, so spectators were surprised by action at the Hispanic Games at the New York Armory</p>",
                      "headline":"4x400m relay runners start brawl mid-race \u2013 video",
                      "standfirst":"Athletics and mid-race fighting don't usually go hand in hand, so spectators were surprised to witness Mt. Vernon High runner Rai Benjamin being taken out by an unidentified runner from Thomas Jefferson High School during the Hispanic Games at the New York Armory last weekend. Benjamin had been knocked off course when he ran into a different TJHS runner. Bizarrely, the incident seems to be ignored by race officials and the race continues as if nothing has happened",
                      "thumbnail":"http://static.guim.co.uk/sys-images/Guardian/Pix/audio/video/2013/1/9/1357742154408/4x400-metre-relay-runners-005.jpg",
                      "commentable":"false",
                      "liveBloggingNow":"false"
                    }
                  }],
                "editorsPicks":[{
                  "id":"world/2012/dec/17/white-house-obama-gun-control-newtown",
                  "sectionId":"world",
                  "sectionName":"World news",
                  "webPublicationDate":"2012-12-17T20:24:00Z",
                  "webTitle":"White House says Obama will move swiftly on gun control after Newtown",
                  "webUrl":"http://www.theguardian.com/world/2012/dec/17/white-house-obama-gun-control-newtown",
                  "apiUrl":"http://content.guardianapis.com/world/2012/dec/17/white-house-obama-gun-control-newtown",
                  "fields":{
                    "trailText":"<p>First signs that Democrats are willing to take on pro-gun lobby as even NRA-endorsed senator Joe Manchin says 'we need action'</p>",
                    "headline":"White House says Obama will move swiftly on gun control after Newtown",
                    "standfirst":"First signs that Democrats are willing to take on pro-gun lobby as even NRA-endorsed senator Joe Manchin says 'we need action'",
                    "thumbnail":"http://static.guim.co.uk/sys-images/Guardian/Pix/maps_and_graphs/2012/12/17/1355705992584/Barack-Obama-attends-a-vi-005.jpg",
                    "commentable":"true",
                    "byline":"Ewen MacAskill in Washington",
                    "liveBloggingNow":"false"
                  }
                },{
                  "id":"uk/2012/dec/18/antarctic-territory-queen-cabinet",
                  "sectionId":"uk",
                  "sectionName":"UK news",
                  "webPublicationDate":"2012-12-18T14:07:09Z",
                  "webTitle":"Antarctic territory named for the Queen as monarch attends cabinet",
                  "webUrl":"http://www.theguardian.com/uk/2012/dec/18/antarctic-territory-queen-cabinet",
                  "apiUrl":"http://content.guardianapis.com/uk/2012/dec/18/antarctic-territory-queen-cabinet",
                  "fields":{
                    "trailText":"Queen Elizabeth Land, table mats and hope of a shorter speech among jubilee gifts in first cabinet visit by a monarch since 1781",
                    "headline":"Antarctic territory named for the Queen as monarch attends cabinet",
                    "standfirst":"Queen Elizabeth Land, table mats and hope of a shorter speech among jubilee gifts in first cabinet visit by a monarch since 1781",
                    "thumbnail":"http://static.guim.co.uk/sys-images/Guardian/Pix/pictures/2012/12/18/1355838771424/Queen-attends-cabinet-mee-003.jpg",
                    "commentable":"true",
                    "byline":"Patrick Wintour, political editor",
                    "liveBloggingNow":"false"
                  }
                },{
                  "id":"world/2012/dec/18/anti-polio-workers-shot-pakistan",
                  "sectionId":"world",
                  "sectionName":"World news",
                  "webPublicationDate":"2012-12-18T10:08:46Z",
                  "webTitle":"Anti-polio workers shot dead in Pakistan",
                  "webUrl":"http://www.theguardian.com/world/2012/dec/18/anti-polio-workers-shot-pakistan",
                  "apiUrl":"http://content.guardianapis.com/world/2012/dec/18/anti-polio-workers-shot-pakistan",
                  "fields":{
                    "trailText":"<p>Five women killed and two men injured in attacks this week raising fears for drive to eradicate crippling disease</p>",
                    "headline":"Anti-polio workers shot dead in Pakistan",
                    "standfirst":"Five women killed and two men injured in attacks this week raising fears for drive to eradicate crippling disease",
                    "thumbnail":"http://static.guim.co.uk/sys-images/Guardian/About/General/2012/12/18/1355824995156/Polio-campaign-003.jpg",
                    "commentable":"false",
                    "byline":"Agencies in Karachi",
                    "liveBloggingNow":"false"
                  }
                }]}}
        """

        return (self.status, response)


    def sport_results(self):
        response = """
            {
              "response":{
                "status":"ok",
                "userTier":"internal",
                "total":1,
                "editorsPicks":[{
                  "id":"world/2012/dec/17/white-house-obama-gun-control-newtown",
                  "sectionId":"world",
                  "sectionName":"World news",
                  "webPublicationDate":"2012-12-17T20:24:00Z",
                  "webTitle":"White House says Obama will move swiftly on gun control after Newtown",
                  "webUrl":"http://www.theguardian.com/world/2012/dec/17/white-house-obama-gun-control-newtown",
                  "apiUrl":"http://content.guardianapis.com/world/2012/dec/17/white-house-obama-gun-control-newtown",
                  "fields":{
                    "trailText":"<p>First signs that Democrats are willing to take on pro-gun lobby as even NRA-endorsed senator Joe Manchin says 'we need action'</p>",
                    "headline":"White House says Obama will move swiftly on gun control after Newtown",
                    "standfirst":"First signs that Democrats are willing to take on pro-gun lobby as even NRA-endorsed senator Joe Manchin says 'we need action'",
                    "thumbnail":"http://static.guim.co.uk/sys-images/Guardian/Pix/maps_and_graphs/2012/12/17/1355705992584/Barack-Obama-attends-a-vi-005.jpg",
                    "commentable":"true",
                    "byline":"Ewen MacAskill in Washington",
                    "liveBloggingNow":"false"
                  }
                }]}}
        """

        return (self.status, response)



    def search_results(self):
        response = """
            {
              "response":{
                "status":"ok",
                "userTier":"internal",
                "total":119545,
                "startIndex":1,
                "pageSize":10,
                "currentPage":1,
                "pages":11955,
                "orderBy":"newest",
                "results":[{
                  "id":"1",
                  "sectionId":"sport",
                  "sectionName":"Sport",
                  "webPublicationDate":"2012-12-18T14:05:20Z",
                  "webTitle":"England clock up first Test series win in India since 1984",
                  "webUrl":"http://www.theguardian.com/sport/2012/dec/18/guardian-weekly-sport-diary-trott-wiggins",
                  "apiUrl":"http://content.guardianapis.com/sport/2012/dec/18/guardian-weekly-sport-diary-trott-wiggins",
                  "fields":{
                    "trailText":"Draw in Nagpur caps cricket victory; Wiggins has personality; Chelsea lose in Japan; meet 'Michelle' Tyson",
                    "headline":"England clock up first Test series win in India since 1984",
                    "standfirst":"Draw in Nagpur caps cricket victory; Wiggins has personality; Chelsea lose in Japan; meet 'Michelle' Tyson",
                    "thumbnail":"http://static.guim.co.uk/sys-images/Guardian/Pix/GWeekly/2012/12/17/1355756269098/SPORT-CRICKET-INDIA-003.jpg",
                    "commentable":"true",
                    "byline":"Barney Ronay",
                    "liveBloggingNow":"false"
                  }
                },{
                  "id":"2",
                  "sectionId":"sport",
                  "sectionName":"Sport",
                  "webPublicationDate":"2012-12-18T13:46:10Z",
                  "webTitle":"The Spin | The art of Alastair Cook's captaincy | Andy Bull",
                  "webUrl":"http://www.theguardian.com/sport/2012/dec/18/the-spin-alastair-cook-captaincy",
                  "apiUrl":"http://content.guardianapis.com/sport/2012/dec/18/the-spin-alastair-cook-captaincy",
                  "fields":{
                    "trailText":"cricket",
                    "headline":"The art of Alastair Cook's captaincy",
                    "standfirst":"Some players were inspired by their captain's example against spin.",
                    "thumbnail":"http://static.guim.co.uk/sys-images/Sport/Pix/pictures/2012/12/18/1355837622222/Englands-Alastair-Cook-003.jpg",
                    "commentable":"true",
                    "byline":"Andy Bull",
                    "liveBloggingNow":"false"
                  }
                }]
              }
            }
        """
        return (self.status, response)
