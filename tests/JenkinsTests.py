import mox
from unittest import TestCase

from pyjenkins import httpstatus
from pyjenkins.Jenkins import Jenkins
from pyjenkins.interfaces import IHttp, IJob, IJobFactory, IJsonParser

class JenkinsTests(TestCase):

    def test_copyJob_SourceExistsAndTargetDoesNotExistCopySuccess_ReturnTargetJob(self):

        mocks= mox.Mox()
        http= mocks.CreateMock(IHttp)
        jobFactory= mocks.CreateMock(IJobFactory)
        sourceJob= mocks.CreateMock(IJob)
        targetJob= mocks.CreateMock(IJob)
        
        jobFactory.create('source').AndReturn(sourceJob)
        jobFactory.create('target').AndReturn(targetJob)
        sourceJob.exists().AndReturn(True)
        targetJob.exists().AndReturn(False)
        targetJob.createCopy('source').AndReturn(True)

        mocks.ReplayAll()

        jenkins = Jenkins(http)
        jenkins.jobFactory= jobFactory

        result= jenkins.copyJob('source', 'target')

        self.assertEqual(targetJob, result)

    def test_copyJob_SourceJobDoesNotExist_ReturnNone(self):

        mocks= mox.Mox()
        http= mocks.CreateMock(IHttp)
        jobFactory= mocks.CreateMock(IJobFactory)
        sourceJob= mocks.CreateMock(IJob)
        
        jobFactory.create('source').AndReturn(sourceJob)
        sourceJob.exists().AndReturn(False)

        mocks.ReplayAll()

        jenkins = Jenkins(http)
        jenkins.jobFactory= jobFactory

        result= jenkins.copyJob('source', 'target')

        self.assertEqual(None, result)

    def test_copyJob_TargetAlreadyExists_ReturnNone(self):

        mocks= mox.Mox()
        http= mocks.CreateMock(IHttp)
        jobFactory= mocks.CreateMock(IJobFactory)
        sourceJob= mocks.CreateMock(IJob)
        targetJob= mocks.CreateMock(IJob)
        
        jobFactory.create('source').AndReturn(sourceJob)
        jobFactory.create('target').AndReturn(targetJob)
        sourceJob.exists().AndReturn(True)
        targetJob.exists().AndReturn(True)

        mocks.ReplayAll()

        jenkins = Jenkins(http)
        jenkins.jobFactory= jobFactory

        result= jenkins.copyJob('source', 'target')

        self.assertEqual(None, result)

    def test_copyJob_CopyFails_ReturnNone(self):

        mocks= mox.Mox()
        http= mocks.CreateMock(IHttp)
        jobFactory= mocks.CreateMock(IJobFactory)
        sourceJob= mocks.CreateMock(IJob)
        targetJob= mocks.CreateMock(IJob)
        
        jobFactory.create('source').AndReturn(sourceJob)
        jobFactory.create('target').AndReturn(targetJob)
        sourceJob.exists().AndReturn(True)
        targetJob.exists().AndReturn(False)
        targetJob.createCopy('source').AndReturn(False)

        mocks.ReplayAll()

        jenkins = Jenkins(http)
        jenkins.jobFactory= jobFactory

        result= jenkins.copyJob('source', 'target')

        self.assertEqual(None, result)

    def test_listJobs_HttpRequestNotOk_ReturnNone(self):

        mocks= mox.Mox()
        http= mocks.CreateMock(IHttp)
        json= mocks.CreateMock(IJsonParser)

        http.request('api/json', {'depth': 0}).AndReturn(('whatever', httpstatus.NOT_FOUND))

        mocks.ReplayAll()

        jenkins = Jenkins(http)
        jenkins.json= json
        
        result= jenkins.listJobs()

        self.assertEqual(None, result)

    def test_listJobs_JsonResultHasNoJobsElement_ReturnNone(self):

        mocks= mox.Mox()
        http= mocks.CreateMock(IHttp)
        json= mocks.CreateMock(IJsonParser)

        http.request('api/json', {'depth': 0}).AndReturn(('json response', httpstatus.OK))
        json.parse('json response').AndReturn({'pies':3})

        mocks.ReplayAll()

        jenkins = Jenkins(http)
        jenkins.json= json
        
        result= jenkins.listJobs()

        self.assertEqual(None, result)

    def test_listJobs_JsonResultContainsEmptyJobsList_ReturnEmptyList(self):

        mocks= mox.Mox()
        http= mocks.CreateMock(IHttp)
        json= mocks.CreateMock(IJsonParser)

        http.request('api/json', {'depth': 0}).AndReturn(('json response', httpstatus.OK))
        json.parse('json response').AndReturn({'jobs':[]})

        mocks.ReplayAll()

        jenkins = Jenkins(http)
        jenkins.json= json
        
        result= jenkins.listJobs()

        self.assertEqual([], result)

    def test_listJobs_JobsListHasSomeJobs_ReturnJobNamesInList(self):

        mocks= mox.Mox()
        http= mocks.CreateMock(IHttp)
        json= mocks.CreateMock(IJsonParser)

        http.request('api/json', {'depth': 0}).AndReturn(('json response', httpstatus.OK))
        json.parse('json response').AndReturn({'jobs':[{'name':'winston'},
                                                       {'name':'geoff'}
                                                       ]})
        mocks.ReplayAll()

        jenkins = Jenkins(http)
        jenkins.json= json
        
        result= jenkins.listJobs()

        self.assertEqual(['winston', 'geoff'], result)

    def test_listFailingJobs_JsonResultContainsEmptyJobsList_ReturnEmptyList(self):

        mocks= mox.Mox()
        http= mocks.CreateMock(IHttp)
        json= mocks.CreateMock(IJsonParser)

        http.request('api/json', {'tree': 'jobs[name,color]'}).AndReturn(('json response', httpstatus.OK))
        json.parse('json response').AndReturn({'jobs':[]})

        mocks.ReplayAll()

        jenkins = Jenkins(http)
        jenkins.json= json

        result= jenkins.listFailingJobs()

        self.assertEqual([], result)

    def test_listFailingJobs_JobsListHasOneJobWithColorRed_ReturnJobNameInList(self):

        mocks= mox.Mox()
        http= mocks.CreateMock(IHttp)
        json= mocks.CreateMock(IJsonParser)

        http.request('api/json', {'tree': 'jobs[name,color]'}).AndReturn(('json response', httpstatus.OK))
        json.parse('json response').AndReturn({'jobs':[{'name':'eric', 'color':'red'}]})
        mocks.ReplayAll()

        jenkins = Jenkins(http)
        jenkins.json= json

        result= jenkins.listFailingJobs()

        self.assertEqual(['eric'], result)

    def test_listFailingJobs_JobsListHasTwoJobsButOnlyOneWithColorRed_ReturnRedJobNameInList(self):

        mocks= mox.Mox()
        http= mocks.CreateMock(IHttp)
        json= mocks.CreateMock(IJsonParser)

        http.request('api/json', {'tree': 'jobs[name,color]'}).AndReturn(('json response', httpstatus.OK))
        json.parse('json response').AndReturn({'jobs':[{'name':'eric', 'color':'red'},
                                                       {'name':'sir lancelot', 'color':'blue'}]})
        mocks.ReplayAll()

        jenkins = Jenkins(http)
        jenkins.json= json

        result= jenkins.listFailingJobs()

        self.assertEqual(['eric'], result)

    def test_listFailingJobs_TriangulationJobsListHasSeveralJobsWithSomeRed_ReturnRedJobNameInList(self):

        mocks= mox.Mox()
        http= mocks.CreateMock(IHttp)
        json= mocks.CreateMock(IJsonParser)

        http.request('api/json', {'tree': 'jobs[name,color]'}).AndReturn(('json response', httpstatus.OK))
        json.parse('json response').AndReturn({'jobs':[{'name':'sir lancelot', 'color':'blue'},
                                                       {'name':'john', 'color':'red'},
                                                       {'name':'sir galahad', 'color':'blue. no. yell...'},
                                                       {'name':'graham', 'color':'red'}
                                                      ]})
        mocks.ReplayAll()

        jenkins = Jenkins(http)
        jenkins.json= json

        result= jenkins.listFailingJobs()

        self.assertEqual(['john', 'graham'], result)

    def test_listFailingJobs_HttpRequestNotOk_ReturnNone(self):

        mocks= mox.Mox()
        http= mocks.CreateMock(IHttp)
        json= mocks.CreateMock(IJsonParser)

        http.request('api/json', {'tree': 'jobs[name,color]'}).AndReturn(('whatever', httpstatus.NOT_FOUND))

        mocks.ReplayAll()

        jenkins = Jenkins(http)
        jenkins.json= json

        result= jenkins.listFailingJobs()

        self.assertEqual(None, result)

    def test_listFailingJobs_JsonResultHasNoJobsElement_ReturnNone(self):

        mocks= mox.Mox()
        http= mocks.CreateMock(IHttp)
        json= mocks.CreateMock(IJsonParser)

        http.request('api/json', {'tree': 'jobs[name,color]'}).AndReturn(('json response', httpstatus.OK))
        json.parse('json response').AndReturn({'spam':3})

        mocks.ReplayAll()

        jenkins = Jenkins(http)
        jenkins.json= json

        result= jenkins.listFailingJobs()

        self.assertEqual(None, result)

    def test_getJob_JobExists_ReturnJob(self):

        mocks= mox.Mox()
        http= mocks.CreateMock(IHttp)
        jobFactory= mocks.CreateMock(IJobFactory)
        job= mocks.CreateMock(IJob)

        jobFactory.create('source').AndReturn(job)
        job.exists().AndReturn(True)

        mocks.ReplayAll()

        jenkins= Jenkins(http)
        jenkins.jobFactory= jobFactory

        result= jenkins.getJob('source')
        
        self.assertEqual(job, result)

    def test_getJob_JobDoesNotExist_ReturnNone(self):

        mocks= mox.Mox()
        http= mocks.CreateMock(IHttp)
        jobFactory= mocks.CreateMock(IJobFactory)
        job= mocks.CreateMock(IJob)

        jobFactory.create('source').AndReturn(job)
        job.exists().AndReturn(False)

        mocks.ReplayAll()

        jenkins= Jenkins(http)
        jenkins.jobFactory= jobFactory

        result= jenkins.getJob('source')
        
        self.assertEqual(None, result)