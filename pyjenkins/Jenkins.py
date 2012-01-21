from pyjenkins.interfaces import IJenkins
from pyjenkins.backend.enums import HttpStatus
from pyjenkins.backend.JsonParser import JsonParser
from pyjenkins.Job import Job, JobStatus

class Jenkins(IJenkins):

    def __init__(self, http, json=JsonParser()):
        """
        @type http: pyjenkins.interfaces.IHttp
        @type json: pyjenkins.interfaces.IJsonParser
        """
        self.http= http
        self.json= json
        self.statusMap = {'red':JobStatus.FAILING,
                          'blue':JobStatus.OK,
                          'grey':JobStatus.UNKNOWN }

    def listJobs(self):
        """
        @return: list of Jobs
        @rtype: [pyjenkins.Job]
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