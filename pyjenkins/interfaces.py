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
