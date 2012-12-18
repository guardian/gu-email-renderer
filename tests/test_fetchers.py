from urllib2 import urlparse
import urllib


class UrlCheckingFetcher:
    def __init__(self, expected_path, **expected_args):
        self.expected_path = expected_path
        self.expected_args = self._quote_params(expected_args)

    def assert_expected_url_equals(self, actual_url):
        (scheme, netloc, path, params, query, fragment) = urlparse.urlparse(actual_url)
        actual_args = dict([arg.split('=') for arg in query.split('&')])

        assert len(actual_args) == len(self.expected_args), 'actual: %d, expected: %d'\
        % (len(actual_args), len(self.expected_args))
        for key in actual_args:
            actual_arg = actual_args[key]
            expected_arg = self.expected_args[key]
            assert actual_arg == expected_arg, 'actual: %s, expected: %s' % (actual_arg, expected_arg)

        assert self.expected_path == path

    def get(self, url):
        print 'Url is: %s' % url
        self.assert_expected_url_equals(url)
        return (None, '{"response": {"results": []}}')

    def _quote_params(self, query_params):
        quoted_params = {}
        for key in query_params.keys():
            new_key = key.replace('_', '-')
            new_value = urllib.quote_plus(query_params[key])
            quoted_params[new_key] = new_value
        return quoted_params



class ApiStubFetcher:

    def get(self, url):
        (_, _, path, _, query, _) = urlparse.urlparse(url)
        if path == '/search':
            return self.search_results()
        if path == '/' and 'show-editors-picks' in query:
            return self.editors_picks_results()

    def search_results(self):

        status = """
        {'status': '200', 'content-length': '10614', 'x-content-api-build': '1998', 'proxy-connection': 'keep-alive',
         'vary': 'Accept,Accept-Encoding', 'x-lift-version': '2.4', 'x-gu-jas': 'ea12a9802fea0a87cff65d3d23752cec!600461558@qtp-1761506447-286',
         'keep-alive': '60', 'expires': 'Tue, 18 Dec 2012 15:19:33 GMT', 'server': 'Mashery Proxy', 'date': 'Tue, 18 Dec 2012 15:18:33 GMT',
         '-content-encoding': 'gzip', 'cache-control': 'max-age=20', 'x-gu-httpd': 'ea12a9802fea0a87cff65d3d23752cec', 'x-mashery-responder': 'prod-p-worker-eu-west-1a-14.mashery.com',
         'content-type': 'application/json; charset=utf-8',
         'content-location': 'http://content.guardianapis.com/search?page-size=10&format=json&section=culture&api-key=***REMOVED***&tag=type%2Farticle&show-fields=trailText%2Cheadline%2CliveBloggingNow%2Cstandfirst%2Ccommentable%2Cthumbnail%2Cbyline'}
        """

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
        return (status, response)

