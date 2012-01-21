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

class IJsonParser(object):

    def parse(self, jsonString):
        """
        Convert the json string into a traversable dictionary.
        @type jsonString: str
        @rtype: dict
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

class IRequestFactory(object):

    def create(self, url):
        """
        @type url: str
        @rtype: pyjenkins.interfaces.IRequest
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

class IUrlBuilderFactory(object):

    def create(self):
        """
        @rtype: pyjenkins.interfaces.IUrlBuilder
        """

class IXml(object):

    def toString(self):
        """
        @return: raw xml string
        @rtype: str
        """

    def getFirstNodeText(self, xpath):
        """
        Finds the first node with the specified xpath and returns its contents as text.
        @param xpath: xpath location of
        @type  xpath: str
        @return: The contents as a string if a node was found, None otherwise.
        @rtype: str
        """

    def setFirstNodeText(self, xpath, text):
        """
        Finds the first node with the specified xpath and sets its contents to text.

        Returns True if a node was found, False otherwise.
        """

class IXmlFactory(object):

    def create(self, rawXmlString):
        """
        @type rawXmlString: str
        @rtype: pyjenkins.interfaces.IXml
        """
