import urllib2
import base64

class IRequestFactory(object):

    def create(self, url):
        """
        @type url: str
        @rtype: pyjenkins.Request.IRequest
        """

class IRequest(object):

    def setBasicAuthorisation(self, username, password):
        """
        @type username: str
        @type password: str
        """

    def open(self, postData=None):
        """
        @param postData: data to be sent via POST method. Default is to send via GET.
        @type  postData: str
        @return: Tuple representing content and http status code
        @rtype: (str, int)
        """

# ----------------------------------------------------------------------
# urllib2 implementation
# ----------------------------------------------------------------------

from pyjenkins import httpstatus

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
            result= (response.read(), httpstatus.OK)
        except urllib2.HTTPError as error:
            content= error.fp.read()
            result= (content, error.code)

        return result

class Urllib2RequestFactory(IRequestFactory):

    def create(self, url):
        return Urllib2Request(url)
