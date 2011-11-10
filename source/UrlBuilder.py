import urllib

class IUrlBuilder:

    def build(self, protocol, host, path, arguments={}):
        '''
        Create a well-formed url from the constituent parts.
        '''

class UrlBuilder:

    def __init__(self):
        pass

    def build(self, protocol, host, path, arguments={}):

        url= '%s://%s/%s' % (protocol, host, urllib.quote(path))

        if arguments:
            url= '?'.join([url, urllib.urlencode(arguments)])
            
        return url
