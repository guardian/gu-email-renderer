from urllib2 import urlparse
import urllib


class ApiStubFetcher:

    status = """
        {'status': '200', 'content-length': '10614', 'x-content-api-build': '1998', 'proxy-connection': 'keep-alive',
         'vary': 'Accept,Accept-Encoding', 'x-lift-version': '2.4', 'x-gu-jas': 'ea12a9802fea0a87cff65d3d23752cec!600461558@qtp-1761506447-286',
         'keep-alive': '60', 'expires': 'Tue, 18 Dec 2012 15:19:33 GMT', 'server': 'Mashery Proxy', 'date': 'Tue, 18 Dec 2012 15:18:33 GMT',
         '-content-encoding': 'gzip', 'cache-control': 'max-age=20', 'x-gu-httpd': 'ea12a9802fea0a87cff65d3d23752cec', 'x-mashery-responder': 'prod-p-worker-eu-west-1a-14.mashery.com',
         'content-type': 'application/json; charset=utf-8',
         'content-location': 'http://content.guardianapis.com/search?page-size=10&format=json&section=culture&api-key=***REMOVED***&tag=type%2Farticle&show-fields=trailText%2Cheadline%2CliveBloggingNow%2Cstandfirst%2Ccommentable%2Cthumbnail%2Cbyline'}
        """



    def get(self, url):
        (_, _, path, _, query, _) = urlparse.urlparse(url)
        if path == '/search':
            return self.search_results()
        if path == '/sport':
            return self.sport_results()
        elif 'show-editors-picks' in query:
            return self.editors_picks_results()


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
                    "webUrl":"http://www.guardian.co.uk/sport/video/2013/jan/09/relay-runners-start-brawl-video",
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
                  "webUrl":"http://www.guardian.co.uk/world/2012/dec/17/white-house-obama-gun-control-newtown",
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
                  "webUrl":"http://www.guardian.co.uk/uk/2012/dec/18/antarctic-territory-queen-cabinet",
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
                  "webUrl":"http://www.guardian.co.uk/world/2012/dec/18/anti-polio-workers-shot-pakistan",
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
                  "webUrl":"http://www.guardian.co.uk/world/2012/dec/17/white-house-obama-gun-control-newtown",
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
                  "webUrl":"http://www.guardian.co.uk/sport/2012/dec/18/guardian-weekly-sport-diary-trott-wiggins",
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
                  "webUrl":"http://www.guardian.co.uk/sport/2012/dec/18/the-spin-alastair-cook-captaincy",
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
