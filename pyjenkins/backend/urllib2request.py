import urllib2
import base64

from pyjenkins.backend.enums import HttpStatus
from pyjenkins.backend.interfaces import IRequest, IRequestFactory


class Urllib2Request(IRequest):

    def __init__(self, url):

        self.request = urllib2.Request(url)

    def setBasicAuthorisation(self, username, password):

        base64string = base64.encodestring('%s:%s' % (username,
                                                      password))
        authorisation = 'Basic ' + base64string.replace('\n', '')

        self.request.add_header('Authorization', authorisation)

    def request(self, postData=None):

        try:
            response = urllib2.urlopen(self.request, data=postData)
            result = (response.read(), HttpStatus.OK)
        except urllib2.HTTPError as error:
            content = error.fp.read()
            result = (content, error.code)

        return result


class Urllib2RequestFactory(IRequestFactory):

    def create(self, url):
        return Urllib2Request(url)
