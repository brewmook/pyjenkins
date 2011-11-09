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
        http.getUrl("job/jobName").AndReturn(("blah", Http.OK))
        mocks.ReplayAll()

        job= Job(http, "jobName")
        result= job.exists()

        self.assertEqual(True, result)

    def test_exists_HttpGetUrlReturnsNotFound_ReturnFalse(self):

        mocks= mox.Mox();
        http= mocks.CreateMock(IHttp)
        http.getUrl("job/jobName").AndReturn(("blah", Http.NOT_FOUND))
        mocks.ReplayAll()

        job= Job(http, "jobName")
        result= job.exists()

        self.assertEqual(False, result)

    def test_configurationXml_HttpGetUrlReturnsOK_ReturnSomeXml(self):

        mocks= mox.Mox();
        http= mocks.CreateMock(IHttp)
        http.getUrl("job/jobName/config.xml").AndReturn(("some xml", Http.OK))
        mocks.ReplayAll()

        job= Job(http, "jobName")
        result= job.configurationXml()

        self.assertEqual("some xml", result)

    def test_configurationXml_HttpGetUrlReturnsNotFound_ReturnEmptyString(self):

        mocks= mox.Mox();
        http= mocks.CreateMock(IHttp)
        http.getUrl("job/jobName/config.xml").AndReturn(("error text", Http.NOT_FOUND))
        mocks.ReplayAll()

        job= Job(http, "jobName")
        result= job.configurationXml()

        self.assertEqual("", result)

    def test_createCopy_HttpPostReturnsOK_ReturnTrue(self):

        mocks= mox.Mox();
        http= mocks.CreateMock(IHttp)
        http.post("createItem", "", {'name':'jobName',
                                     'mode':'copy',
                                     'from':'otherJob'}) \
           .AndReturn(("blah blah", Http.OK))
        mocks.ReplayAll()

        job= Job(http, "jobName")
        result= job.createCopy("otherJob")

        self.assertEqual(True, result)

    def test_createCopy_HttpPostReturnsNotOK_ReturnFalse(self):

        mocks= mox.Mox();
        http= mocks.CreateMock(IHttp)
        http.post("createItem", "", {'name':'jobName',
                                     'mode':'copy',
                                     'from':'otherJob'}) \
           .AndReturn(("blah blah", Http.NOT_FOUND))
        mocks.ReplayAll()

        job= Job(http, "jobName")
        result= job.createCopy("otherJob")

        self.assertEqual(False, result)

    def test_setConfigurationXml_HttpPostReturnsOK_ReturnTrue(self):

        mocks= mox.Mox();
        http= mocks.CreateMock(IHttp)
        http.post("job/jobName/config.xml","xml data") \
           .AndReturn(("blah blah", Http.OK))
        mocks.ReplayAll()

        job= Job(http, "jobName")
        result= job.setConfigurationXml("xml data")

        self.assertEqual(True, result)

    def test_setConfigurationXml_HttpPostReturnsNotOK_ReturnFalse(self):

        mocks= mox.Mox();
        http= mocks.CreateMock(IHttp)
        http.post("job/jobName/config.xml","xml data") \
           .AndReturn(("error text", Http.NOT_FOUND))
        mocks.ReplayAll()

        job= Job(http, "jobName")
        result= job.setConfigurationXml("xml data")

        self.assertEqual(False, result)
