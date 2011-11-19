from pyjenkins import httpstatus
from pyjenkins.Job import JobFactory
from pyjenkins.Json import Json

class IJenkins(object):
    
    def copyJob(self, sourceJobName, targetJobName):
        """
        @return: target job on success, or None on failure.
        @rtype:  pyjenkins.Job.IJob
        """

    def listJobs(self):
        """
        @return: list of job names
        @rtype: [str]
        """

    def getJob(self, jobName):
        """
        @return: job instance if it exists, or None otherwise.
        @rtype:  pyjenkins.Job.IJob
        """

class Jenkins(IJenkins):

    def __init__(self, http):
        self.http= http
        self.jobFactory = JobFactory(http)
        self.json = Json()

    def copyJob(self, sourceJobName, targetJobName):
        sourceJob= self.jobFactory.create(sourceJobName)
        result= None

        if sourceJob.exists():

            targetJob= self.jobFactory.create(targetJobName)

            if not targetJob.exists() \
               and targetJob.createCopy(sourceJobName):
                result= targetJob
            
        return result
    
    def listJobs(self):
        result= None
        (json, status) = self.http.request('api/json', {'depth':0})

        if status == httpstatus.OK:
            data= self.json.parse(json)
            if 'jobs' in data:
                result= [job['name'] for job in data['jobs']]

        return result

    def getJob(self, jobName):
        
        job= self.jobFactory.create(jobName)
        if not job.exists():
            job= None
        return job
