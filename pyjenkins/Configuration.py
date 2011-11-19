from pyjenkins.Xml import Xml

class IConfigurationFactory(object):

    def create(self, rawXml):
        """
        @type rawXml: str
        @rtype: pyjenkins.IConfiguration.IConfiguration
        """

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

# Constants
SUBVERSION_REPOSITORY_XPATH = '//hudson.scm.SubversionSCM_-ModuleLocation/remote'
CHILD_PROJECTS_XPATH = '//hudson.tasks.BuildTrigger/childProjects'
COPY_ARTIFACTS_JOB_NAME_XPATH = '//hudson.plugins.copyartifact.CopyArtifact/projectName'

class Configuration(IConfiguration):

    def __init__(self, aXml):
        self.xml= aXml

    def rawXml(self):
        return self.xml.toString()

    def subversionRepository(self):
        return self.xml.getFirstNodeText(SUBVERSION_REPOSITORY_XPATH)

    def setSubversionRepository(self, url):
        return self.xml.setFirstNodeText(SUBVERSION_REPOSITORY_XPATH, url)

    def setChildProjects(self, jobName):
        return self.xml.setFirstNodeText(CHILD_PROJECTS_XPATH, jobName)

    def setCopyArtifactsJobName(self, jobName):
        return self.xml.setFirstNodeText(COPY_ARTIFACTS_JOB_NAME_XPATH, jobName)

class ConfigurationFactory(IConfigurationFactory):

    def create(self, rawXml):

        return Configuration(Xml(rawXml))
