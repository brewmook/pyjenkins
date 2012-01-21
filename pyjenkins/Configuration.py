from pyjenkins.backend.Xml import Xml
from pyjenkins.interfaces import IConfiguration, IConfigurationFactory

# Constants
SUBVERSION_REPOSITORY_XPATH = './/hudson.scm.SubversionSCM_-ModuleLocation/remote'
CHILD_PROJECTS_XPATH = './/hudson.tasks.BuildTrigger/childProjects'
COPY_ARTIFACTS_JOB_NAME_XPATH = './/hudson.plugins.copyartifact.CopyArtifact/projectName'

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
