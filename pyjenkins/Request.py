import urllib, urllib2
import base64
import Http

class IRequestFactory:

    def create(self, url):
        pass

class IRequest:

    def setBasicAuthorisation(self, username, password):
        pass

    def open(self, postData=None):
        '''
        Return tuple of (page content, http status code)

        Default is to use GET, but if postData is supplied, use POST.
        '''
        pass

# ----------------------------------------------------------------------
# urllib2 implementation
# ----------------------------------------------------------------------

class Urllib2Request(IRequest):

    def __init__(self, url):

        self.request= urllib2.Request(url)

    def setBasicAuthorisation(self, username, password):
        
        base64string = base64.encodestring('%s:%s' % (username,
                                                      password))
        authorisation= 'Basic ' + base64string.replace('\n','')

        self.request.add_header('Authorization', authorisation)

    def open(self, postData=None):

        try:
            response = urllib2.urlopen(self.request, data=postData)
            result= (response.read(), Http.OK)
        except urllib2.HTTPError as error:
            content= error.fp.read()
            result= (content, error.code)

        return result

class Urllib2RequestFactory(IRequestFactory):

    def create(self, url):
        return Urllib2Request(url)
