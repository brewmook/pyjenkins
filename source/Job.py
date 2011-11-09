import Http

class IJob:

    def exists(self):
        '''Return True if the job exists, False otherwise'''
        pass

    def configurationXml(self):
        '''Return the configuration XML for this job as plain text.'''
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

    def _getUrl(self, extraPathElements = []):
        url= '/'.join([self.host, self.name] + extraPathElements)
        return self.http.getUrl(url)
