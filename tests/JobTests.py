import sys
import os
import mox
from unittest import TestCase

import Http

from Job import Job
from Http import IHttp
from Xml import IXml, IXmlFactory

class JobTests(TestCase):

    def test_exists_HttpRequestReturnsOK_ReturnTrue(self):

        mocks= mox.Mox();
        http= mocks.CreateMock(IHttp)
        xmlFactory = mocks.CreateMock(IXmlFactory)

        http.request("job/jobName/config.xml").AndReturn(("blah", Http.OK))
        mocks.ReplayAll()

        job= Job(http, "jobName", xmlFactory)
        result= job.exists()

        self.assertEqual(True, result)

    def test_exists_HttpRequestReturnsNotFound_ReturnFalse(self):

        mocks= mox.Mox();
        http= mocks.CreateMock(IHttp)
        xmlFactory = mocks.CreateMock(IXmlFactory)

        http.request("job/jobName/config.xml").AndReturn(("blah", Http.NOT_FOUND))
        mocks.ReplayAll()

        job= Job(http, "jobName", xmlFactory)
        result= job.exists()

        self.assertEqual(False, result)

    def test_configurationXml_HttpRequestReturnsOK_ReturnSomeXml(self):

        mocks= mox.Mox();
        http= mocks.CreateMock(IHttp)
        xmlFactory = mocks.CreateMock(IXmlFactory)
        xml = mocks.CreateMock(IXml)

        http.request("job/jobName/config.xml").AndReturn(('some xml', Http.OK))
        xmlFactory.create('some xml').AndReturn(xml)
        mocks.ReplayAll()

        job= Job(http, "jobName", xmlFactory)
        result= job.configurationXml()

        self.assertEqual(xml, result)

    def test_configurationXml_HttpRequestReturnsNotFound_ReturnNone(self):

        mocks= mox.Mox();
        http= mocks.CreateMock(IHttp)
        xmlFactory = mocks.CreateMock(IXmlFactory)

        http.request("job/jobName/config.xml").AndReturn(("error text", Http.NOT_FOUND))
        mocks.ReplayAll()

        job= Job(http, "jobName", xmlFactory)
        result= job.configurationXml()

        self.assertEqual(None, result)

    def test_createCopy_HttpRequestReturnsOK_ReturnTrue(self):

        mocks= mox.Mox();
        http= mocks.CreateMock(IHttp)
        xmlFactory = mocks.CreateMock(IXmlFactory)

        http.request("createItem",
                     arguments= {'name':'jobName',
                                 'mode':'copy',
                                 'from':'otherJob'},
                     postData= "") \
           .AndReturn(("blah blah", Http.OK))
        mocks.ReplayAll()

        job= Job(http, "jobName", xmlFactory)
        result= job.createCopy("otherJob")

        self.assertEqual(True, result)

    def test_createCopy_HttpRequestReturnsNotOK_ReturnFalse(self):

        mocks= mox.Mox();
        http= mocks.CreateMock(IHttp)
        xmlFactory = mocks.CreateMock(IXmlFactory)

        http.request("createItem",
                     arguments= {'name':'jobName',
                                 'mode':'copy',
                                 'from':'otherJob'},
                     postData= "") \
           .AndReturn(("blah blah", Http.NOT_FOUND))
        mocks.ReplayAll()

        job= Job(http, "jobName", xmlFactory)
        result= job.createCopy("otherJob")

        self.assertEqual(False, result)

    def test_setConfigurationXml_HttpRequestReturnsOK_ReturnTrue(self):

        mocks= mox.Mox();
        http= mocks.CreateMock(IHttp)
        xmlFactory = mocks.CreateMock(IXmlFactory)
        xml = mocks.CreateMock(IXml)

        xml.toString().AndReturn("raw xml")
        http.request("job/jobName/config.xml", postData="raw xml") \
           .AndReturn(("blah blah", Http.OK))
        mocks.ReplayAll()

        job= Job(http, "jobName", xmlFactory)
        result= job.setConfigurationXml(xml)

        self.assertEqual(True, result)

    def test_setConfigurationXml_HttpRequestReturnsNotOK_ReturnFalse(self):

        mocks= mox.Mox();
        http= mocks.CreateMock(IHttp)
        xmlFactory = mocks.CreateMock(IXmlFactory)
        xml = mocks.CreateMock(IXml)

        xml.toString().AndReturn("raw xml")
        http.request("job/jobName/config.xml", postData="raw xml") \
           .AndReturn(("error text", Http.NOT_FOUND))
        mocks.ReplayAll()

        job= Job(http, "jobName", xmlFactory)
        result= job.setConfigurationXml(xml)

        self.assertEqual(False, result)
