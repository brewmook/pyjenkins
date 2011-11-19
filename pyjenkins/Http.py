from UrlBuilder import UrlBuilderFactory
from Request import Urllib2RequestFactory

# Response constants
OK = 200
NOT_FOUND = 404

class IHttp:

    def request(self, path, arguments={}, postData=None):
        '''
        Request the given path.
        
        Anything in arguments will be added as url query arguments.
        
        By default GET is used, but if postData is supplied, POST will be
        used, and postData sent as the payload.
        
        Return tuple of (contents, returnCode).
        '''
        pass

class Http(IHttp):
    '''
    Helpful links:
    http://www.voidspace.org.uk/python/articles/authentication.shtml
    '''

    def __init__(self, host, username, password,
                 urlBuilderFactory = UrlBuilderFactory(),
                 requestFactory = Urllib2RequestFactory()):
        self.host= host
        self.username= username
        self.password= password
        self.requestFactory= requestFactory
        self.urlBuilderFactory= urlBuilderFactory

    def request(self, path, arguments={}, postData=None):

        builder= self.urlBuilderFactory.create()
        url= builder.build(self.host, path, arguments)

        req= self.requestFactory.create(url)
        req.setBasicAuthorisation(self.username, self.password)

        return req.open(postData)
