import mox
from unittest import TestCase

from pyjenkins.backend.enums import HttpStatus
from pyjenkins.backend.interfaces import IHttp, IJsonParser
from pyjenkins.jenkins import Jenkins
from pyjenkins.job import Job, JobStatus

class JenkinsTests(TestCase):

    def setUp(self):

        self.mocks = mox.Mox()
        self.http= self.mocks.CreateMock(IHttp)
        self.json= self.mocks.CreateMock(IJsonParser)

    # Test list_jobs()

    def test__list_jobs__HttpRequestNotOk_ReturnNone(self):

        self.http.request('api/json', {'tree': 'jobs[name,color]'}).AndReturn(('whatever', HttpStatus.NOT_FOUND))
        self.json.parse('whatever').AndReturn({'pies':3})
        self.mocks.ReplayAll()

        jenkins = Jenkins(self.http, self.json)
        result = jenkins.list_jobs()

        self.assertEqual(None, result)

    def test__list_jobs__JsonResultHasNoJobsElement_ReturnNone(self):

        self.http.request('api/json', {'tree': 'jobs[name,color]'}).AndReturn(('json response', HttpStatus.OK))
        self.json.parse('json response').AndReturn({'pies':3})
        self.mocks.ReplayAll()

        jenkins = Jenkins(self.http, self.json)
        result = jenkins.list_jobs()

        self.assertEqual(None, result)

    def test__list_jobs__JsonResultContainsEmptyJobsList_ReturnEmptyList(self):

        self.http.request('api/json', {'tree': 'jobs[name,color]'}).AndReturn(('json response', HttpStatus.OK))
        self.json.parse('json response').AndReturn({'jobs':[]})
        self.mocks.ReplayAll()

        jenkins = Jenkins(self.http, self.json)
        result = jenkins.list_jobs()

        self.assertEqual([], result)

    def test__list_jobs__JsonResultContainsSomeJobs_ReturnListOfJobs(self):

        json_parsed = {'jobs':[{'name':'graham', 'color':'red'},
                               {'name':'john', 'color':'blue'},
                               {'name':'eric', 'color':'grey'},
                               {'name':'terry', 'color':'disabled'},
                               ]}
        self.http.request('api/json', {'tree': 'jobs[name,color]'}).AndReturn(('json response', HttpStatus.OK))
        self.json.parse('json response').AndReturn(json_parsed)
        self.mocks.ReplayAll()

        jenkins = Jenkins(self.http, self.json)
        result = jenkins.list_jobs()
        expectedResult = [Job('graham', JobStatus.FAILING),
                          Job('john', JobStatus.OK),
                          Job('eric', JobStatus.UNKNOWN),
                          Job('terry', JobStatus.DISABLED)]

        self.assertEqual(expectedResult, result)

    # Test disable_job()

    def test__disable_job__HttpRequestNotOk_ReturnFalse(self):

        self.http.request('job/some job/disable', postData='').AndReturn(('whatever', HttpStatus.NOT_FOUND))
        self.mocks.ReplayAll()

        jenkins = Jenkins(self.http, self.json)
        result = jenkins.disable_job('some job')

        self.assertEqual(False, result)

    def test__disable_job__HttpRequestOk_ReturnTrue(self):

        self.http.request('job/other job/disable', postData='').AndReturn(('whatever', HttpStatus.OK))
        self.mocks.ReplayAll()

        jenkins = Jenkins(self.http, self.json)
        result = jenkins.disable_job('other job')

        self.assertEqual(True, result)

    # Test enable_job()

    def test__enable_job__HttpRequestNotOk_ReturnFalse(self):

        self.http.request('job/some job/enable', postData='').AndReturn(('whatever', HttpStatus.NOT_FOUND))
        self.mocks.ReplayAll()

        jenkins = Jenkins(self.http, self.json)
        result = jenkins.enable_job('some job')

        self.assertEqual(False, result)

    def test__enable_job__HttpRequestOk_ReturnTrue(self):

        self.http.request('job/other job/enable', postData='').AndReturn(('whatever', HttpStatus.OK))
        self.mocks.ReplayAll()

        jenkins = Jenkins(self.http, self.json)
        result = jenkins.enable_job('other job')

        self.assertEqual(True, result)
