import mox
from unittest import TestCase

from pyjenkins import httpstatus
from pyjenkins.Jenkins import Jenkins
from pyjenkins.interfaces import IHttp, IJob, IJobFactory, IJobFilter, IJsonParser

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
        filter= mocks.CreateMock(IJobFilter)

        http.request('api/json', {'tree': 'jobs[name,color]'}).AndReturn(('whatever', httpstatus.NOT_FOUND))
        json.parse('whatever').AndReturn({'pies':3})
        filter.includeJob(mox.IgnoreArg(), mox.IgnoreArg()).AndReturn(True)

        mocks.ReplayAll()

        jenkins = Jenkins(http)
        jenkins.json= json

        result= jenkins.listJobs(filter)

        self.assertEqual(None, result)

    def test_listJobs_JsonResultHasNoJobsElement_ReturnNone(self):

        mocks= mox.Mox()
        http= mocks.CreateMock(IHttp)
        json= mocks.CreateMock(IJsonParser)
        filter= mocks.CreateMock(IJobFilter)

        http.request('api/json', {'tree': 'jobs[name,color]'}).AndReturn(('json response', httpstatus.OK))
        json.parse('json response').AndReturn({'pies':3})
        filter.includeJob(mox.IgnoreArg(), mox.IgnoreArg()).AndReturn(True)

        mocks.ReplayAll()

        jenkins = Jenkins(http)
        jenkins.json= json

        result= jenkins.listJobs(filter)

        self.assertEqual(None, result)

    def test_listJobs_JsonResultContainsEmptyJobsList_ReturnEmptyList(self):

        mocks= mox.Mox()
        http= mocks.CreateMock(IHttp)
        json= mocks.CreateMock(IJsonParser)
        filter= mocks.CreateMock(IJobFilter)

        http.request('api/json', {'tree': 'jobs[name,color]'}).AndReturn(('json response', httpstatus.OK))
        json.parse('json response').AndReturn({'jobs':[]})
        filter.includeJob(mox.IgnoreArg(), mox.IgnoreArg()).AndReturn(True)

        mocks.ReplayAll()

        jenkins = Jenkins(http)
        jenkins.json= json

        result= jenkins.listJobs(filter)

        self.assertEqual([], result)

    def test_listJobs_JobsListHasSomeJobsFilterAllowsAllJobs_ReturnJobNamesInList(self):

        mocks= mox.Mox()
        http= mocks.CreateMock(IHttp)
        json= mocks.CreateMock(IJsonParser)
        filter= mocks.CreateMock(IJobFilter)

        http.request('api/json', {'tree': 'jobs[name,color]'}).AndReturn(('json response', httpstatus.OK))
        json.parse('json response').AndReturn({'jobs':[{'name':'winston', 'color':'red'},
                                                       {'name':'geoff', 'color':'blue'}
                                                       ]})
        filter.includeJob(mox.IgnoreArg(), mox.IgnoreArg()).AndReturn(True)
        filter.includeJob(mox.IgnoreArg(), mox.IgnoreArg()).AndReturn(True)
        mocks.ReplayAll()

        jenkins = Jenkins(http)
        jenkins.json= json

        result= jenkins.listJobs(filter)

        self.assertEqual(['winston', 'geoff'], result)

    def test_listJobs_JobsListHasSomeJobsFilterBarsAllJobs_ReturnEmptyList(self):

        mocks= mox.Mox()
        http= mocks.CreateMock(IHttp)
        json= mocks.CreateMock(IJsonParser)
        filter= mocks.CreateMock(IJobFilter)

        http.request('api/json', {'tree': 'jobs[name,color]'}).AndReturn(('json response', httpstatus.OK))
        json.parse('json response').AndReturn({'jobs':[{'name':'winston', 'color':'red'},
                                                       {'name':'geoff', 'color':'blue'}
                                                      ]})
        filter.includeJob(mox.IgnoreArg(), mox.IgnoreArg()).AndReturn(False)
        filter.includeJob(mox.IgnoreArg(), mox.IgnoreArg()).AndReturn(False)
        mocks.ReplayAll()

        jenkins = Jenkins(http)
        jenkins.json= json

        result= jenkins.listJobs(filter)

        self.assertEqual([], result)

    def test_listJobs_JobsListHasSomeJobsFilterAllowsGeoff_ReturnGeoff(self):

        mocks= mox.Mox()
        http= mocks.CreateMock(IHttp)
        json= mocks.CreateMock(IJsonParser)
        filter= mocks.CreateMock(IJobFilter)

        http.request('api/json', {'tree': 'jobs[name,color]'}).AndReturn(('json response', httpstatus.OK))
        json.parse('json response').AndReturn({'jobs':[{'name':'winston', 'color':'red'},
                                                       {'name':'geoff', 'color':'blue'}
                                                      ]})
        filter.includeJob('geoff', mox.IgnoreArg()).InAnyOrder().AndReturn(True)
        filter.includeJob(mox.IgnoreArg(), mox.IgnoreArg()).InAnyOrder().AndReturn(False)
        mocks.ReplayAll()

        jenkins = Jenkins(http)
        jenkins.json= json

        result= jenkins.listJobs(filter)

        self.assertEqual(['geoff'], result)

    def test_listJobs_JobsListHasSomeJobsFilterAllowsRed_ReturnWinston(self):

        mocks= mox.Mox()
        http= mocks.CreateMock(IHttp)
        json= mocks.CreateMock(IJsonParser)
        filter= mocks.CreateMock(IJobFilter)

        http.request('api/json', {'tree': 'jobs[name,color]'}).AndReturn(('json response', httpstatus.OK))
        json.parse('json response').AndReturn({'jobs':[{'name':'winston', 'color':'red'},
                                                       {'name':'geoff', 'color':'blue'}
                                                      ]})
        filter.includeJob(mox.IgnoreArg(), 'red').InAnyOrder().AndReturn(True)
        filter.includeJob(mox.IgnoreArg(), mox.IgnoreArg()).InAnyOrder().AndReturn(False)
        mocks.ReplayAll()

        jenkins = Jenkins(http)
        jenkins.json= json

        result= jenkins.listJobs(filter)

        self.assertEqual(['winston'], result)

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
