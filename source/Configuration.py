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

    def setSubversionRepository(self, url):
        '''
        Replace the current subversion repository.
        Return True on success, False otherwise.
        '''

class Configuration(IConfiguration):

    def __init__(self, aXml):
        self.xml= aXml

    def rawXml(self):
        return self.xml.toString()

    def setSubversionRepository(self, url):
        xpath= '//hudson.scm.SubversionSCM_-ModuleLocation/remote'
        return self.xml.setFirstNodeText(xpath, url)

class ConfigurationFactory(IConfigurationFactory):

    def create(self, rawXml):

        return Configuration(Xml(rawXml))
