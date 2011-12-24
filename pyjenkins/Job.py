from pyjenkins import httpstatus
from pyjenkins.Configuration import ConfigurationFactory
from pyjenkins.interfaces import IJob, IJobFactory

class Job(IJob):

    def __init__(self, http, jobName):
        self.http = http
        self._name = jobName
        self.configurationFactory = ConfigurationFactory()

    def name(self):
        return self._name

    def exists(self):
        result= True
        url= self._configUrl()
        (text, returnCode) = self.http.request(url)

        if returnCode != httpstatus.OK:
            result= False

        return result

    def configuration(self):
        result= None
        url= self._configUrl()
        (contents, returnCode) = self.http.request(url)

        if returnCode == httpstatus.OK:
            result= self.configurationFactory.create(contents)

        return result

    def setConfiguration(self, aConfiguration):
        result= True
        url= self._configUrl()
        (content, returnCode) = self.http.request(url, postData=aConfiguration.rawXml())

        if returnCode != httpstatus.OK:
            result= False
            
        return result

    def createCopy(self, otherJobName):
        result= True
        arguments= {'name' : self._name,
                    'mode' : 'copy',
                    'from' : otherJobName}
        (content, returnCode) = self.http.request('createItem',
                                                  postData="",
                                                  arguments=arguments)
        if returnCode != httpstatus.OK:
            result= False
            
        return result

    def _configUrl(self):
        return '/'.join(['job', self._name, 'config.xml'])


class JobFactory(IJobFactory):

    def __init__(self, http):
        self.http= http

    def create(self, name):
        return Job(self.http, name)
