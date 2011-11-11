import Http
import Xml

class IJob:

    def exists(self):
        '''Return True if the job exists, False otherwise'''
        pass

    def configurationXml(self):
        '''Return the configuration XML for this job as plain text.'''
        pass

    def setConfigurationXml(self, configurationXml):
        '''Change the xml configuration. Return True on success, False otherwise'''
        pass

    def createCopy(self, otherJobName):
        '''
        Create a job on the host with self.name, copying settings from otherJobName.
        Return True if the job was created, False otherwise.
        '''
        pass


class Job(IJob):

    def __init__(self, http, jobName,
                 xmlFactory = Xml.XmlFactory()):
        self.http = http
        self.name = jobName
        self.xmlFactory = xmlFactory

    def exists(self):
        result= True
        url= self._configUrl()
        (text, returnCode) = self.http.request(url)

        if returnCode != Http.OK:
            result= False

        return result

    def configurationXml(self):
        result= None
        url= self._configUrl()
        (contents, returnCode) = self.http.request(url)

        if returnCode == Http.OK:
            result= self.xmlFactory.create(contents)

        return result

    def setConfigurationXml(self, xml):
        result= True
        url= self._configUrl()
        (content, returnCode) = self.http.request(url, postData=xml.toString())

        if returnCode != Http.OK:
            result= False
            
        return result

    def createCopy(self, otherJobName):
        result= True
        arguments= {'name' : self.name,
                    'mode' : 'copy',
                    'from' : otherJobName}
        (content, returnCode) = self.http.request('createItem',
                                                  postData="",
                                                  arguments=arguments)
        if returnCode != Http.OK:
            result= False
            
        return result

    def _configUrl(self):
        return '/'.join(['job', self.name, 'config.xml'])
