import urllib, urllib2
import base64

from UrlBuilder import UrlBuilder

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

    def __init__(self, host, username, password):
        self.host= host
        self.username= username
        self.password= password

    def request(self, path, arguments={}, postData=None):

        builder= UrlBuilder()

        url= builder.build('http', self.host, path, arguments)

        print url

        if postData:
            req = urllib2.Request(url, postData)
        else:
            req = urllib2.Request(url)

        req.add_header('Authorization', self._authorization())
        
        try:
            response = urllib2.urlopen(req)
            result = (response.read(), OK)
        except urllib2.HTTPError as error:
            content= error.fp.read()
            result = (content, error.code)

        return result

    def _authorization(self):

        base64string = base64.encodestring('%s:%s' % (self.username,
                                                      self.password))
        return 'Basic ' + base64string.replace('\n','')
