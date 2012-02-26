from pyjenkins.interfaces import IJenkinsFactory
from pyjenkins.backend.enums import HttpStatus
from pyjenkins.backend.http import Http
from pyjenkins.backend.jsonparser import JsonParser
from pyjenkins.job import Job, JobStatus

class Jenkins(object):

    def __init__(self, http, json=JsonParser()):
        """
        @type http: pyjenkins.interfaces.IHttp
        @type json: pyjenkins.interfaces.IJsonParser
        """
        self.http= http
        self.json= json
        self.statusMap = {'aborted':        JobStatus.UNKNOWN,
                          'aborted_anime':  JobStatus.UNKNOWN,
                          'blue':           JobStatus.OK,
                          'blue_anime':     JobStatus.OK,
                          'disabled':       JobStatus.DISABLED,
                          'disabled_anime': JobStatus.DISABLED,
                          'grey':           JobStatus.UNKNOWN,
                          'grey_anime':     JobStatus.UNKNOWN,
                          'notbuilt':       JobStatus.UNKNOWN,
                          'notbuilt_anime': JobStatus.UNKNOWN,
                          'red':            JobStatus.FAILING,
                          'red_anime':      JobStatus.FAILING,
                          'yellow':         JobStatus.FAILING,
                          'yellow_anime':   JobStatus.FAILING,
                          }

    def list_jobs(self):
        """
        @return: list of Jobs
        @rtype: [pyjenkins.job.Job]
        """
        result= None
        jobs= self._get_json_jobs({'tree':'jobs[name,color]'})

        if jobs is not None:
            result= [Job(job['name'], self.statusMap[job['color']]) for job in jobs]

        return result

    def disable_job(self, job_name):
        """
        @type job_name: str
        @return: True on success, False if something went wrong.
        @rtype: bool
        """
        (json, status) = self.http.request('job/%s/disable' % job_name)
        return status == HttpStatus.OK

    def enable_job(self, job_name):
        """
        @type job_name: str
        @return: True on success, False if something went wrong.
        @rtype: bool
        """
        (json, status) = self.http.request('job/%s/enable' % job_name)
        return status == HttpStatus.OK

    def _get_json_jobs(self, parameters):
        result= None
        (json, status) = self.http.request('api/json', parameters)

        if status == HttpStatus.OK:
            data= self.json.parse(json)
            if 'jobs' in data:
                result= data['jobs']

        return result

class JenkinsFactory(IJenkinsFactory):

    def create(self, server):
        """
        @type server: pyjenkins.server.Server
        @rtype: pyjenkins.jenkins.Jenkins
        """
        return Jenkins(Http(server))
