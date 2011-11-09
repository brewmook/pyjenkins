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

    def __init__(self, http, host, jobName):
        self.http = http
        self.host = host
        self.name = jobName

    def exists(self):
        result= True
        (text, returnCode) = self._getUrl()
        if returnCode != Http.OK:
            result= False
        return result

    def configurationXml(self):
        (result, returnCode) = self._getUrl(['config.xml'])
        if returnCode != Http.OK:
            result= ''
        return result

    def setConfigurationXml(self, configurationXml):
        result= True
        url= '/'.join([self.host, 'job', self.name, 'config.xml'])

        (content, returnCode) = self.http.post(url, configurationXml)
        if returnCode != Http.OK:
            result= False
            
        return result

    def createCopy(self, otherJobName):
        result= True
        arguments= '&'.join(['name='+self.name,
                             'mode=copy',
                             'from='+otherJobName])
        url= '/'.join([self.host,
                       'createItem?'+arguments])
        
        (content, returnCode) = self.http.post(url, "")
        if returnCode != Http.OK:
            result= False
            
        return result

    def _getUrl(self, extraPathElements = []):
        url= '/'.join([self.host, self.name] + extraPathElements)
        return self.http.getUrl(url)
