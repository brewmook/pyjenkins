import sys
import os
import mox
from unittest import TestCase

import Http

from Job import Job
from Http import IHttp

class JobTests(TestCase):

    def test_exists_HttpRequestReturnsOK_ReturnTrue(self):

        mocks= mox.Mox();
        http= mocks.CreateMock(IHttp)
        http.request("job/jobName/config.xml").AndReturn(("blah", Http.OK))
        mocks.ReplayAll()

        job= Job(http, "jobName")
        result= job.exists()

        self.assertEqual(True, result)

    def test_exists_HttpRequestReturnsNotFound_ReturnFalse(self):

        mocks= mox.Mox();
        http= mocks.CreateMock(IHttp)
        http.request("job/jobName/config.xml").AndReturn(("blah", Http.NOT_FOUND))
        mocks.ReplayAll()

        job= Job(http, "jobName")
        result= job.exists()

        self.assertEqual(False, result)

    def test_configurationXml_HttpRequestReturnsOK_ReturnSomeXml(self):

        mocks= mox.Mox();
        http= mocks.CreateMock(IHttp)
        http.request("job/jobName/config.xml").AndReturn(("some xml", Http.OK))
        mocks.ReplayAll()

        job= Job(http, "jobName")
        result= job.configurationXml()

        self.assertEqual("some xml", result)

    def test_configurationXml_HttpRequestReturnsNotFound_ReturnNone(self):

        mocks= mox.Mox();
        http= mocks.CreateMock(IHttp)
        http.request("job/jobName/config.xml").AndReturn(("error text", Http.NOT_FOUND))
        mocks.ReplayAll()

        job= Job(http, "jobName")
        result= job.configurationXml()

        self.assertEqual(None, result)

    def test_createCopy_HttpRequestReturnsOK_ReturnTrue(self):

        mocks= mox.Mox();
        http= mocks.CreateMock(IHttp)
        http.request("createItem",
                     arguments= {'name':'jobName',
                                 'mode':'copy',
                                 'from':'otherJob'},
                     postData= "") \
           .AndReturn(("blah blah", Http.OK))
        mocks.ReplayAll()

        job= Job(http, "jobName")
        result= job.createCopy("otherJob")

        self.assertEqual(True, result)

    def test_createCopy_HttpRequestReturnsNotOK_ReturnFalse(self):

        mocks= mox.Mox();
        http= mocks.CreateMock(IHttp)
        http.request("createItem",
                     arguments= {'name':'jobName',
                                 'mode':'copy',
                                 'from':'otherJob'},
                     postData= "") \
           .AndReturn(("blah blah", Http.NOT_FOUND))
        mocks.ReplayAll()

        job= Job(http, "jobName")
        result= job.createCopy("otherJob")

        self.assertEqual(False, result)

    def test_setConfigurationXml_HttpRequestReturnsOK_ReturnTrue(self):

        mocks= mox.Mox();
        http= mocks.CreateMock(IHttp)
        http.request("job/jobName/config.xml", postData="xml data") \
           .AndReturn(("blah blah", Http.OK))
        mocks.ReplayAll()

        job= Job(http, "jobName")
        result= job.setConfigurationXml("xml data")

        self.assertEqual(True, result)

    def test_setConfigurationXml_HttpRequestReturnsNotOK_ReturnFalse(self):

        mocks= mox.Mox();
        http= mocks.CreateMock(IHttp)
        http.request("job/jobName/config.xml", postData="xml data") \
           .AndReturn(("error text", Http.NOT_FOUND))
        mocks.ReplayAll()

        job= Job(http, "jobName")
        result= job.setConfigurationXml("xml data")

        self.assertEqual(False, result)
