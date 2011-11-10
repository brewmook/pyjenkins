import Http

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

    def __init__(self, http, jobName):
        self.http = http
        self.name = jobName

    def exists(self):
        result= True
        url= self._configUrl()
        (text, returnCode) = self.http.getUrl(url)
        if returnCode != Http.OK:
            result= False
        return result

    def configurationXml(self):
        url= self._configUrl()
        (result, returnCode) = self.http.getUrl(url)
        if returnCode != Http.OK:
            result= None
        return result

    def setConfigurationXml(self, configurationXml):
        result= True
        url= self._configUrl()

        (content, returnCode) = self.http.post(url, configurationXml)
        if returnCode != Http.OK:
            result= False
            
        return result

    def createCopy(self, otherJobName):
        result= True
        arguments= {'name' : self.name,
                    'mode' : 'copy',
                    'from' : otherJobName}
        
        (content, returnCode) = self.http.post('createItem', "", arguments)
        if returnCode != Http.OK:
            result= False
            
        return result

    def _configUrl(self):
        return '/'.join(['job', self.name, 'config.xml'])
