class IConfiguration(object):

    def rawXml(self):
        """
        @return: Jenkins-format configuration xml string.
        @rtype: str
        """

    def subversionRepository(self):
        """
        @return: The current Subversion repository url or None if it\'s not there.
        @rtype: str
        """

    def setSubversionRepository(self, url):
        """
        Replace the current subversion repository url.
        @type url: str
        @return: True on success, False if the setting is not already in the xml.
        @rtype: bool
        """

    def setChildProjects(self, jobName):
        """
        Replace the name of the job(s) to build after this job.
        @type jobName: str
        @return True on success, False if the setting is not already in the xml.
        @rtype: bool
        """

    def setCopyArtifactsJobName(self, jobName):
        """
        Replace the name of the job(s) to copy artifacts from.
        @type jobName: str
        @return True on success, False if the setting is not already in the xml.
        @rtype: bool
        """

class IConfigurationFactory(object):

    def create(self, rawXml):
        """
        @type rawXml: str
        @rtype: pyjenkins.interfaces.IConfiguration
        """

class IEvent(object):
    """
    Inspired by code by Peter Thatcher found at
    http://www.valuedlessons.com/2008/04/events-in-python.html
    """

    def register(self, handler):
        """
        @arg handler: Callable
        """

    def fire(self, *args, **kargs):
        """
        Calls all registered handlers with given arguments.
        """

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

class IJenkins(object):

    def copyJob(self, sourceJobName, targetJobName):
        """
        @return: target job on success, or None on failure.
        @rtype:  pyjenkins.interfaces.IJob
        """

    def listJobs(self):
        """
        @return: list of job names
        @rtype: [str]
        """

    def listFailingJobs(self):
        """
        @return: list of failing job names
        @rtype: [str]
        """

    def getJob(self, jobName):
        """
        @return: job instance if it exists, or None otherwise.
        @rtype:  pyjenkins.interfaces.IJob
        """

class IJob(object):

    def name(self):
        """
        @rtype: str
        """

    def exists(self):
        """
        @return: True if the job exists, False otherwise.
        @rtype: bool
        """

    def configuration(self):
        """
        Fetch the configuration from the server. No cacheing.
        @rtype: pyjenkins.interfaces.IConfiguration
        """

    def setConfiguration(self, configuration):
        """
        Send the configuration to the remote server. No cacheing.
        @type configuration: pyjenkins.interfaces.IConfiguration
        @return: True if the server accepted the configuration, False otherwise.
        @rtype: bool
        """

    def createCopy(self, otherJobName):
        """
        Create a job on the host with self.name, copying settings from otherJobName.
        @type otherJobName: str
        @return: True if the job was created, False otherwise.
        @rtype: bool
        """

class IJobFactory(object):

    def create(self, name):
        """
        @type name: str
        @rtype: pyjenkins.interfaces.IJob
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
