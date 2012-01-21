import mox
from unittest import TestCase

from pyjenkins.backend.enums import HttpStatus
from pyjenkins.Jenkins import Jenkins
from pyjenkins.backend.interfaces import IHttp, IJsonParser
from pyjenkins.Job import Job, JobStatus

class JenkinsTests(TestCase):

    def test_listJobs_HttpRequestNotOk_ReturnNone(self):

        mocks= mox.Mox()
        http= mocks.CreateMock(IHttp)
        json= mocks.CreateMock(IJsonParser)

        http.request('api/json', {'tree': 'jobs[name,color]'}).AndReturn(('whatever', HttpStatus.NOT_FOUND))
        json.parse('whatever').AndReturn({'pies':3})

        mocks.ReplayAll()

        jenkins = Jenkins(http, json)

        result= jenkins.listJobs()

        self.assertEqual(None, result)

    def test_listJobs_JsonResultHasNoJobsElement_ReturnNone(self):

        mocks= mox.Mox()
        http= mocks.CreateMock(IHttp)
        json= mocks.CreateMock(IJsonParser)

        http.request('api/json', {'tree': 'jobs[name,color]'}).AndReturn(('json response', HttpStatus.OK))
        json.parse('json response').AndReturn({'pies':3})

        mocks.ReplayAll()

        jenkins = Jenkins(http, json)

        result= jenkins.listJobs()

        self.assertEqual(None, result)

    def test_listJobs_JsonResultContainsEmptyJobsList_ReturnEmptyList(self):

        mocks= mox.Mox()
        http= mocks.CreateMock(IHttp)
        json= mocks.CreateMock(IJsonParser)

        http.request('api/json', {'tree': 'jobs[name,color]'}).AndReturn(('json response', HttpStatus.OK))
        json.parse('json response').AndReturn({'jobs':[]})

        mocks.ReplayAll()

        jenkins = Jenkins(http, json)

        result= jenkins.listJobs()

        self.assertEqual([], result)

    def test_listJobs_JsonResultContainsSomeJobs_ReturnListOfJobs(self):

        mocks= mox.Mox()
        http= mocks.CreateMock(IHttp)
        json= mocks.CreateMock(IJsonParser)

        http.request('api/json', {'tree': 'jobs[name,color]'}).AndReturn(('json response', HttpStatus.OK))
        json.parse('json response').AndReturn({'jobs':[{'name':'graham', 'color':'red'},
                                                       {'name':'john', 'color':'blue'},
                                                       {'name':'eric', 'color':'grey'}
                                                       ]})
        mocks.ReplayAll()

        jenkins = Jenkins(http, json)

        result= jenkins.listJobs()
        expectedResult= [Job('graham', JobStatus.FAILING),
                         Job('john', JobStatus.OK),
                         Job('eric', JobStatus.UNKNOWN)]

        self.assertEqual(expectedResult, result)