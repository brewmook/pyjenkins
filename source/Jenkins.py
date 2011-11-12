import Http
import Job
import Json

class Jenkins:

    def __init__(self, http):
        self.http= http
        self.jobFactory = Job.JobFactory(http)
        self.json = Json.Json()

    def copyJob(self, sourceJobName, targetJobName):
        '''
        Returns target job on success, or None on failure.
        '''
        sourceJob= self.jobFactory.create(sourceJobName)
        result= None

        if sourceJob.exists():

            targetJob= self.jobFactory.create(targetJobName)

            if not targetJob.exists() \
               and targetJob.createCopy(sourceJobName):
                result= targetJob
            
        return result
    
    def listJobs(self):
        '''
        Returns a list of job names.
        '''

        result= None
        (json, status) = self.http.request('api/json', {'depth':0})

        if status == Http.OK:
            data= self.json.parse(json)
            if 'jobs' in data:
                result= [job['name'] for job in data['jobs']]

        return result
