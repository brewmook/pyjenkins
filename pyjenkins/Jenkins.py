from pyjenkins import httpstatus
from pyjenkins.interfaces import IJenkins
from pyjenkins.backend.JsonParser import JsonParser

class Jenkins(IJenkins):

    def __init__(self, http, json=JsonParser()):
        """
        @type http: pyjenkins.interfaces.IHttp
        @type json: pyjenkins.interfaces.IJsonParser
        """
        self.http= http
        self.json= json

    def listJobs(self, jobFilter):
        """
        @type jobFilter: pyjenkins.interfaces.IJobFilter
        @return: list of job names
        @rtype: [str]
        """
        result= None
        jobs= self._getJsonJobs({'tree':'jobs[name,color]'})

        if jobs is not None:
            result= [job['name'] for job in jobs if jobFilter.includeJob(job['name'],job['color'])]

        return result

    def _getJsonJobs(self, parameters):
        result= None
        (json, status) = self.http.request('api/json', parameters)

        if status == httpstatus.OK:
            data= self.json.parse(json)
            if 'jobs' in data:
                result= data['jobs']

        return result