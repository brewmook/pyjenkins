import sys
import os
import mox
from unittest import TestCase

import Http

from Job import Job
from Http import IHttp

class JobTests(TestCase):

    def test_exists_HttpGetUrlReturnsOK_ReturnTrue(self):

        mocks= mox.Mox();
        http= mocks.CreateMock(IHttp)
        http.getUrl("host/jobName").AndReturn(("blah", Http.OK))
        mocks.ReplayAll()

        job= Job(http, "host", "jobName")
        result= job.exists()

        self.assertEqual(True, result)

    def test_exists_HttpGetUrlReturnsError_ReturnFalse(self):

        mocks= mox.Mox();
        http= mocks.CreateMock(IHttp)
        http.getUrl("host/jobName").AndReturn(("blah", Http.NOT_FOUND))
        mocks.ReplayAll()

        job= Job(http, "host", "jobName")
        result= job.exists()

        self.assertEqual(False, result)

    def test_configurationXml_HttpGetUrlReturnsSomeXml_ReturnSomeXml(self):

        mocks= mox.Mox();
        http= mocks.CreateMock(IHttp)
        http.getUrl("host/jobName/config.xml").AndReturn(("some xml", Http.OK))
        mocks.ReplayAll()

        job= Job(http, "host", "jobName")
        result= job.configurationXml()

        self.assertEqual("some xml", result)

    def test_configurationXml_HttpGetUrlReturnsError_ReturnEmptyString(self):

        mocks= mox.Mox();
        http= mocks.CreateMock(IHttp)
        http.getUrl("host/jobName/config.xml").AndReturn(("error text", Http.NOT_FOUND))
        mocks.ReplayAll()

        job= Job(http, "host", "jobName")
        result= job.configurationXml()

        self.assertEqual("", result)

