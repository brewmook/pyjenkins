# Response constants
OK = 200
NOT_FOUND = 404

class IHttp:

    def request(self, url, arguments={}, postData=None):
        '''
        Request the given url.
        
        Anything in arguments will be added as url query arguments.
        
        By default GET is used, but if postData is supplied, POST will be
        used, and postData sent as the payload.
        
        Return tuple of (contents, returnCode).
        '''
        pass
