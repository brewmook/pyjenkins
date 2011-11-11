import Job

class Jenkins:

    def __init__(self, http):
        self.jobFactory = Job.JobFactory(http)

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
    
