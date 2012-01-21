import urllib
from pyjenkins.interfaces import IUrlBuilder, IUrlBuilderFactory

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
