from pyjenkins.UrlBuilder import UrlBuilderFactory
from pyjenkins.Request import Urllib2RequestFactory

class IHttp(object):

    def request(self, path, arguments=None, postData=None):
        """
        @param path: The path part of the url, e.g. 'cgi-bin/something.py'
        @type path:  str
        @param arguments: key-value pairs will be added to the url as query arguments.
        @type arguments: dict
        @param postData: data to be sent via POST method. Default is to send via GET.
        @type  postData: str
        @return: Tuple representing content and http status code
        @rtype: (str, int)
        """
        pass

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
        @type requestFactory: pyjenkins.Request.IRequestFactory
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
