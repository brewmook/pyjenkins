import urllib

class IUrlBuilderFactory:

    def create():
        pass

class IUrlBuilder:

    def build(self, host, path, arguments={}):
        '''
        Create a well-formed url from the constituent parts.
        '''
        pass

class UrlBuilder:

    def __init__(self):
        pass

    def build(self, host, path, arguments={}):

        url= '%s/%s' % (host, urllib.quote(path))

        if arguments:
            url= '?'.join([url, urllib.urlencode(arguments)])
            
        return url

class UrlBuilderFactory(IUrlBuilderFactory):

    def create():
        return UrlBuilder()
