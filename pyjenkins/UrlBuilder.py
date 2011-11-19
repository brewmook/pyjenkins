import urllib

class IUrlBuilderFactory(object):

    def create(self):
        """
        @rtype: pyjenkins.UrlBuilder.IUrlBuilder
        """

class IUrlBuilder(object):

    def build(self, host, path, arguments=None):
        """
        @param host: E.g. 'http://pies.com'
        @type  host: str
        @param path: The path part of the url, e.g. 'cgi-bin/something.py'
        @type  path: str
        @param arguments: key-value pairs will be added to the url as query arguments
        @type  arguments: dict
        @return: A well-formed url created from the constituent parts
        @rtype: str
        """

class UrlBuilder(IUrlBuilder):

    def __init__(self):
        pass

    def build(self, host, path, arguments=None):

        url= '%s/%s' % (host, urllib.quote(path))

        if arguments:
            url= '?'.join([url, urllib.urlencode(arguments)])
            
        return url

class UrlBuilderFactory(IUrlBuilderFactory):

    def create(self):
        return UrlBuilder()
