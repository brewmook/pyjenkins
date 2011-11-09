import httplib, urllib

# Response constants
OK = 200
NOT_FOUND = 404

class IHttp:

    def getUrl(self, url):
        '''Return tuple of (contents, returnCode) for the given url'''
        pass

    def post(self, url, postData, arguments={}):
        '''
        Sends a POST request with postData as the payload to url.
        Return tuple of (contents, returnCode).
        '''
        pass

class Http(IHttp):
    '''
    Method implementations loosely based on examples at
    http://docs.python.org/release/2.6.7/library/httplib.html
    '''

    def __init__(self, host):
        self.host= host

    def getUrl(self, url):

        conn = httplib.HTTPConnection(self.host)
        conn.request("GET", "/"+url)
        response= conn.getresponse()

        status= response.status
        content= response.read()

        conn.close()

        return (content, status)

    def post(self, url, postData, arguments={}):

        params = urllib.urlencode(arguments)
        headers = {"Content-type": "application/x-www-form-urlencoded",
                   "Accept": "text/plain"}

        conn = httplib.HTTPConnection(self.host)
        conn.request("POST", "/"+url, params, headers)
        conn.send(postData)

        response= conn.getresponse()
        status= response.status
        content= response.read()

        conn.close()

        return (content, status)
