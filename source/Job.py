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
        url= self._jobUrl()
        (text, returnCode) = self.http.getUrl(url)
        if returnCode != Http.OK:
            result= False
        return result

    def configurationXml(self):
        url= self._jobUrl(['config.xml'])
        (result, returnCode) = self.http.getUrl(url)
        if returnCode != Http.OK:
            result= ''
        return result

    def setConfigurationXml(self, configurationXml):
        result= True
        url= self._jobUrl(['config.xml'])

        (content, returnCode) = self.http.post(url, configurationXml)
        if returnCode != Http.OK:
            result= False
            
        return result

    def createCopy(self, otherJobName):
        result= True
        arguments= {'name' : self.name,
                    'mode' : 'copy',
                    'from' : otherJobName}
        url= '/'.join([self.host, 'createItem'])
        
        (content, returnCode) = self.http.post(url, "", arguments)
        if returnCode != Http.OK:
            result= False
            
        return result

    def _jobUrl(self, extraPathElements = []):
        return '/'.join([self.host, 'job', self.name] + extraPathElements)
