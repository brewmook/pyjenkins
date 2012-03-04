from pyjenkins.backend.interfaces import IHttp
from pyjenkins.backend.urlbuilder import UrlBuilderFactory
from pyjenkins.backend.urllib2request import Urllib2RequestFactory


class Http(IHttp):
    """
    Helpful links:
    http://www.voidspace.org.uk/python/articles/authentication.shtml
    """

    def __init__(self,
                 server,
                 urlBuilderFactory=UrlBuilderFactory(),
                 requestFactory=Urllib2RequestFactory()):
        """
        @param host: e.g. http://www.wherever.com
        @type server: pyjenkins.server.Server
        @type urlBuilderFactory: pyjenkins.urlbuilder.IUrlBuilderFactory
        @type requestFactory: pyjenkins.interfaces.IRequestFactory
        """
        self.server = server
        self.requestFactory = requestFactory
        self.urlBuilderFactory = urlBuilderFactory

    def request(self, path, arguments=None, postData=None):

        builder = self.urlBuilderFactory.create()
        url = builder.build(self.server.host, path, arguments)

        req = self.requestFactory.create(url)
        if self.server.username is not '':
            req.setBasicAuthorisation(self.server.username, self.server.password)

        return req.open(postData)
