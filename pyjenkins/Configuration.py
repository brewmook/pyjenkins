from Xml import Xml

class IConfigurationFactory:

    def create(self, rawXml):
        '''
        Create a IConfiguration instance from the raw xml provided.
        '''

class IConfiguration:

    def rawXml(self):
        '''
        Return Jenkins-format configuration xml string.
        '''

    def subversionRepository(self):
        '''
        Return the current Subversion repository url or None if it\'s not there.
        '''

    def setSubversionRepository(self, url):
        '''
        Replace the current subversion repository.
        Return True on success, False if the setting is not already in the xml.
        '''

    def setChildProjects(self, jobName):
        '''
        Replace the name of the job(s) to build after this job.
        Return True on success, False if the setting is not already in the xml.
        '''

    def setCopyArtifactsJobName(self, jobName):
        '''
        Replace the name of the job(s) to copy artifacts from.
        Return True on success, False if the setting is not already in the xml.
        '''

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
