# Response constants
OK = 200
NOT_FOUND = 404

class IHttp:

    def getUrl(self, url):
        '''Return tuple of (contents, returnCode) for the given url'''
        pass

    def post(self, url, postData):
        '''
        Sends a POST request with postData as the payload to url.
        Return tuple of (contents, returnCode).
        '''
        pass
