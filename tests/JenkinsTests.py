import mox
from unittest import TestCase

from pyjenkins.backend.enums import HttpStatus
from pyjenkins.backend.interfaces import IHttp, IJsonParser
from pyjenkins.jenkins import Jenkins
from pyjenkins.job import Job, JobStatus

class JenkinsTests(TestCase):

    def test__list_jobs__HttpRequestNotOk_ReturnNone(self):

        mocks= mox.Mox()
        http= mocks.CreateMock(IHttp)
        json= mocks.CreateMock(IJsonParser)

        http.request('api/json', {'tree': 'jobs[name,color]'}).AndReturn(('whatever', HttpStatus.NOT_FOUND))
        json.parse('whatever').AndReturn({'pies':3})

        mocks.ReplayAll()

        jenkins = Jenkins(http, json)

        result= jenkins.list_jobs()

        self.assertEqual(None, result)

    def test__list_jobs__JsonResultHasNoJobsElement_ReturnNone(self):

        mocks= mox.Mox()
        http= mocks.CreateMock(IHttp)
        json= mocks.CreateMock(IJsonParser)

        http.request('api/json', {'tree': 'jobs[name,color]'}).AndReturn(('json response', HttpStatus.OK))
        json.parse('json response').AndReturn({'pies':3})

        mocks.ReplayAll()

        jenkins = Jenkins(http, json)

        result= jenkins.list_jobs()

        self.assertEqual(None, result)

    def test__list_jobs__JsonResultContainsEmptyJobsList_ReturnEmptyList(self):

        mocks= mox.Mox()
        http= mocks.CreateMock(IHttp)
        json= mocks.CreateMock(IJsonParser)

        http.request('api/json', {'tree': 'jobs[name,color]'}).AndReturn(('json response', HttpStatus.OK))
        json.parse('json response').AndReturn({'jobs':[]})

        mocks.ReplayAll()

        jenkins = Jenkins(http, json)

        result= jenkins.list_jobs()

        self.assertEqual([], result)

    def test__list_jobs__JsonResultContainsSomeJobs_ReturnListOfJobs(self):

        mocks= mox.Mox()
        http= mocks.CreateMock(IHttp)
        json= mocks.CreateMock(IJsonParser)

        http.request('api/json', {'tree': 'jobs[name,color]'}).AndReturn(('json response', HttpStatus.OK))
        json.parse('json response').AndReturn({'jobs':[{'name':'graham', 'color':'red'},
                                                       {'name':'john', 'color':'blue'},
                                                       {'name':'eric', 'color':'grey'},
                                                       {'name':'terry', 'color':'disabled'},
                                                       ]})
        mocks.ReplayAll()

        jenkins = Jenkins(http, json)

        result= jenkins.list_jobs()
        expectedResult= [Job('graham', JobStatus.FAILING),
                         Job('john', JobStatus.OK),
                         Job('eric', JobStatus.UNKNOWN),
                         Job('terry', JobStatus.DISABLED)]

        self.assertEqual(expectedResult, result)
