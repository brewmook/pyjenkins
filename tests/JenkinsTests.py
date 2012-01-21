import mox
from unittest import TestCase

from pyjenkins.backend.enums import HttpStatus
from pyjenkins.Jenkins import Jenkins
from pyjenkins.interfaces import IJobFilter
from pyjenkins.backend.interfaces import IHttp, IJsonParser

class JenkinsTests(TestCase):

    def test_listJobs_HttpRequestNotOk_ReturnNone(self):

        mocks= mox.Mox()
        http= mocks.CreateMock(IHttp)
        json= mocks.CreateMock(IJsonParser)
        filter= mocks.CreateMock(IJobFilter)

        http.request('api/json', {'tree': 'jobs[name,color]'}).AndReturn(('whatever', HttpStatus.NOT_FOUND))
        json.parse('whatever').AndReturn({'pies':3})
        filter.includeJob(mox.IgnoreArg(), mox.IgnoreArg()).AndReturn(True)

        mocks.ReplayAll()

        jenkins = Jenkins(http, json)

        result= jenkins.listJobs(filter)

        self.assertEqual(None, result)

    def test_listJobs_JsonResultHasNoJobsElement_ReturnNone(self):

        mocks= mox.Mox()
        http= mocks.CreateMock(IHttp)
        json= mocks.CreateMock(IJsonParser)
        filter= mocks.CreateMock(IJobFilter)

        http.request('api/json', {'tree': 'jobs[name,color]'}).AndReturn(('json response', HttpStatus.OK))
        json.parse('json response').AndReturn({'pies':3})
        filter.includeJob(mox.IgnoreArg(), mox.IgnoreArg()).AndReturn(True)

        mocks.ReplayAll()

        jenkins = Jenkins(http, json)

        result= jenkins.listJobs(filter)

        self.assertEqual(None, result)

    def test_listJobs_JsonResultContainsEmptyJobsList_ReturnEmptyList(self):

        mocks= mox.Mox()
        http= mocks.CreateMock(IHttp)
        json= mocks.CreateMock(IJsonParser)
        filter= mocks.CreateMock(IJobFilter)

        http.request('api/json', {'tree': 'jobs[name,color]'}).AndReturn(('json response', HttpStatus.OK))
        json.parse('json response').AndReturn({'jobs':[]})
        filter.includeJob(mox.IgnoreArg(), mox.IgnoreArg()).AndReturn(True)

        mocks.ReplayAll()

        jenkins = Jenkins(http, json)

        result= jenkins.listJobs(filter)

        self.assertEqual([], result)

    def test_listJobs_JobsListHasSomeJobsFilterAllowsAllJobs_ReturnJobNamesInList(self):

        mocks= mox.Mox()
        http= mocks.CreateMock(IHttp)
        json= mocks.CreateMock(IJsonParser)
        filter= mocks.CreateMock(IJobFilter)

        http.request('api/json', {'tree': 'jobs[name,color]'}).AndReturn(('json response', HttpStatus.OK))
        json.parse('json response').AndReturn({'jobs':[{'name':'winston', 'color':'red'},
                                                       {'name':'geoff', 'color':'blue'}
                                                       ]})
        filter.includeJob(mox.IgnoreArg(), mox.IgnoreArg()).AndReturn(True)
        filter.includeJob(mox.IgnoreArg(), mox.IgnoreArg()).AndReturn(True)
        mocks.ReplayAll()

        jenkins = Jenkins(http, json)

        result= jenkins.listJobs(filter)

        self.assertEqual(['winston', 'geoff'], result)

    def test_listJobs_JobsListHasSomeJobsFilterBarsAllJobs_ReturnEmptyList(self):

        mocks= mox.Mox()
        http= mocks.CreateMock(IHttp)
        json= mocks.CreateMock(IJsonParser)
        filter= mocks.CreateMock(IJobFilter)

        http.request('api/json', {'tree': 'jobs[name,color]'}).AndReturn(('json response', HttpStatus.OK))
        json.parse('json response').AndReturn({'jobs':[{'name':'winston', 'color':'red'},
                                                       {'name':'geoff', 'color':'blue'}
                                                      ]})
        filter.includeJob(mox.IgnoreArg(), mox.IgnoreArg()).AndReturn(False)
        filter.includeJob(mox.IgnoreArg(), mox.IgnoreArg()).AndReturn(False)
        mocks.ReplayAll()

        jenkins = Jenkins(http, json)

        result= jenkins.listJobs(filter)

        self.assertEqual([], result)

    def test_listJobs_JobsListHasSomeJobsFilterAllowsGeoff_ReturnGeoff(self):

        mocks= mox.Mox()
        http= mocks.CreateMock(IHttp)
        json= mocks.CreateMock(IJsonParser)
        filter= mocks.CreateMock(IJobFilter)

        http.request('api/json', {'tree': 'jobs[name,color]'}).AndReturn(('json response', HttpStatus.OK))
        json.parse('json response').AndReturn({'jobs':[{'name':'winston', 'color':'red'},
                                                       {'name':'geoff', 'color':'blue'}
                                                      ]})
        filter.includeJob('geoff', mox.IgnoreArg()).InAnyOrder().AndReturn(True)
        filter.includeJob(mox.IgnoreArg(), mox.IgnoreArg()).InAnyOrder().AndReturn(False)
        mocks.ReplayAll()

        jenkins = Jenkins(http, json)

        result= jenkins.listJobs(filter)

        self.assertEqual(['geoff'], result)

    def test_listJobs_JobsListHasSomeJobsFilterAllowsRed_ReturnWinston(self):

        mocks= mox.Mox()
        http= mocks.CreateMock(IHttp)
        json= mocks.CreateMock(IJsonParser)
        filter= mocks.CreateMock(IJobFilter)

        http.request('api/json', {'tree': 'jobs[name,color]'}).AndReturn(('json response', HttpStatus.OK))
        json.parse('json response').AndReturn({'jobs':[{'name':'winston', 'color':'red'},
                                                       {'name':'geoff', 'color':'blue'}
                                                      ]})
        filter.includeJob(mox.IgnoreArg(), 'red').InAnyOrder().AndReturn(True)
        filter.includeJob(mox.IgnoreArg(), mox.IgnoreArg()).InAnyOrder().AndReturn(False)
        mocks.ReplayAll()

        jenkins = Jenkins(http, json)

        result= jenkins.listJobs(filter)

        self.assertEqual(['winston'], result)
