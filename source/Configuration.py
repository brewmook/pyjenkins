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
        Return True on success, False otherwise.
        '''

# Constants
SUBVERSION_REPOSITORY_XPATH = '//hudson.scm.SubversionSCM_-ModuleLocation/remote'

class Configuration(IConfiguration):

    def __init__(self, aXml):
        self.xml= aXml

    def rawXml(self):
        return self.xml.toString()

    def subversionRepository(self):
        return self.xml.getFirstNodeText(SUBVERSION_REPOSITORY_XPATH)

    def setSubversionRepository(self, url):
        return self.xml.setFirstNodeText(SUBVERSION_REPOSITORY_XPATH, url)

class ConfigurationFactory(IConfigurationFactory):

    def create(self, rawXml):

        return Configuration(Xml(rawXml))
