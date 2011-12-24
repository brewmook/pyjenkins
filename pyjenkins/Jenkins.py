from pyjenkins import httpstatus
from pyjenkins.Job import JobFactory
from pyjenkins.JsonParser import JsonParser
from pyjenkins.interfaces import IJenkins

class Jenkins(IJenkins):

    def __init__(self, http):
        self.http= http
        self.jobFactory = JobFactory(http)
        self.json = JsonParser()

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
