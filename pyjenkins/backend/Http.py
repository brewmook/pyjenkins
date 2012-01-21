from pyjenkins.backend.UrlBuilder import UrlBuilderFactory
from pyjenkins.backend.Urllib2Request import Urllib2RequestFactory

from pyjenkins.interfaces import IHttp

class Http(IHttp):
    """
    Helpful links:
    http://www.voidspace.org.uk/python/articles/authentication.shtml
    """

    def __init__(self, host, username, password,
                 urlBuilderFactory = UrlBuilderFactory(),
                 requestFactory = Urllib2RequestFactory()):
        """
        @param host: e.g. http://www.wherever.com
        @type host: str
        @type username: str
        @type password: str
        @type urlBuilderFactory: pyjenkins.UrlBuilder.IUrlBuilderFactory
        @type requestFactory: pyjenkins.interfaces.IRequestFactory
        """
        self.host= host
        self.username= username
        self.password= password
        self.requestFactory= requestFactory
        self.urlBuilderFactory= urlBuilderFactory

    def request(self, path, arguments=None, postData=None):

        builder= self.urlBuilderFactory.create()
        url= builder.build(self.host, path, arguments)

        req= self.requestFactory.create(url)
        req.setBasicAuthorisation(self.username, self.password)

        return req.open(postData)
