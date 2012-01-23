from pyjenkins.interfaces import IJenkins
from pyjenkins.backend.enums import HttpStatus
from pyjenkins.backend.jsonparser import JsonParser
from pyjenkins.job import Job, JobStatus

class Jenkins(IJenkins):

    def __init__(self, http, json=JsonParser()):
        """
        @type http: pyjenkins.interfaces.IHttp
        @type json: pyjenkins.interfaces.IJsonParser
        """
        self.http= http
        self.json= json
        self.statusMap = {'red':        JobStatus.FAILING,
                          'red_anime':  JobStatus.FAILING,
                          'blue':       JobStatus.OK,
                          'blue_anime': JobStatus.OK,
                          'grey':       JobStatus.UNKNOWN,
                          'grey_anime': JobStatus.UNKNOWN,
                          'disabled':   JobStatus.UNKNOWN
                          }

    def listJobs(self):
        """
        @return: list of Jobs
        @rtype: [pyjenkins.job.Job]
        """
        result= None
        jobs= self._getJsonJobs({'tree':'jobs[name,color]'})

        if jobs is not None:
            result= [Job(job['name'], self.statusMap[job['color']]) for job in jobs]

        return result

    def _getJsonJobs(self, parameters):
        result= None
        (json, status) = self.http.request('api/json', parameters)

        if status == HttpStatus.OK:
            data= self.json.parse(json)
            if 'jobs' in data:
                result= data['jobs']

        return result
