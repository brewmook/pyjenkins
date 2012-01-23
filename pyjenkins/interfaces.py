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

class IJenkins(object):

    def listJobs(self):
        """
        @return: list of Jobs
        @rtype: [pyjenkins.job.Job]
        """
