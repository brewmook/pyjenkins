import Http
import Configuration

class IJob:

    def name(self):
        '''Return the name of the job.'''

    def exists(self):
        '''Return True if the job exists, False otherwise'''
        pass

    def configuration(self):
        '''Return an IConfiguration instance for this job.'''
        pass

    def setConfiguration(self, aConfiguration):
        '''Change the remote configuration. Return True on success, False otherwise'''
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
        self._name = jobName
        self.configurationFactory = Configuration.ConfigurationFactory()

    def name(self):
        return self._name

    def exists(self):
        result= True
        url= self._configUrl()
        (text, returnCode) = self.http.request(url)

        if returnCode != Http.OK:
            result= False

        return result

    def configuration(self):
        result= None
        url= self._configUrl()
        (contents, returnCode) = self.http.request(url)

        if returnCode == Http.OK:
            result= self.configurationFactory.create(contents)

        return result

    def setConfiguration(self, aConfiguration):
        result= True
        url= self._configUrl()
        (content, returnCode) = self.http.request(url, postData=aConfiguration.rawXml())

        if returnCode != Http.OK:
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
        if returnCode != Http.OK:
            result= False
            
        return result

    def _configUrl(self):
        return '/'.join(['job', self._name, 'config.xml'])

class IJobFactory:
    
    def create(self, http):
        pass

class JobFactory(IJobFactory):

    def __init__(self, http):
        self.http= http

    def create(self, name):
        return Job(self.http, name)
