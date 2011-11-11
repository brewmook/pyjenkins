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

class Configuration(IConfiguration):

    def __init__(self, aXml):
        pass

    def rawXml(self):
        pass

class ConfigurationFactory(IConfigurationFactory):

    def create(self, rawXml):

        return Configuration(Xml(rawXml))
