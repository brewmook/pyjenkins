from pyjenkins.interfaces import IJobFilter

class FailingJobs(IJobFilter):

    def includeJob(self, job, color):
        """
        @type job: str
        @type color: str
        """
        result= False
        if (color == "red"):
            result= True
        return result
