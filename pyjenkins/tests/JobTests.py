import mox
from unittest import TestCase

from pyjenkins import Http
from pyjenkins.Job import Job
from pyjenkins.Http import IHttp
from pyjenkins.Configuration import IConfiguration, IConfigurationFactory

class JobTests(TestCase):

    def test_name_ReturnNamePassedOnConstruction(self):

        job= Job(None, 'a name')
        self.assertEqual('a name', job.name())

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

    def test_configuration_HttpRequestReturnsOK_ReturnSomeXml(self):

        mocks= mox.Mox();
        http= mocks.CreateMock(IHttp)
        configurationFactory = mocks.CreateMock(IConfigurationFactory)
        configuration = mocks.CreateMock(IConfiguration)

        http.request("job/jobName/config.xml").AndReturn(('some xml', Http.OK))
        configurationFactory.create('some xml').AndReturn(configuration)
        mocks.ReplayAll()

        job= Job(http, "jobName")
        job.configurationFactory = configurationFactory
        
        result= job.configuration()

        self.assertEqual(configuration, result)

    def test_configuration_HttpRequestReturnsNotFound_ReturnNone(self):

        mocks= mox.Mox();
        http= mocks.CreateMock(IHttp)

        http.request("job/jobName/config.xml").AndReturn(("error text", Http.NOT_FOUND))
        mocks.ReplayAll()

        job= Job(http, "jobName")
        result= job.configuration()

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

    def test_setConfiguration_HttpRequestReturnsOK_ReturnTrue(self):

        mocks= mox.Mox();
        http= mocks.CreateMock(IHttp)
        configuration = mocks.CreateMock(IConfiguration)

        configuration.rawXml().AndReturn("raw xml")
        http.request("job/jobName/config.xml", postData="raw xml") \
           .AndReturn(("blah blah", Http.OK))
        mocks.ReplayAll()

        job= Job(http, "jobName")
        result= job.setConfiguration(configuration)

        self.assertEqual(True, result)

    def test_setConfiguration_HttpRequestReturnsNotOK_ReturnFalse(self):

        mocks= mox.Mox();
        http= mocks.CreateMock(IHttp)
        configuration = mocks.CreateMock(IConfiguration)

        configuration.rawXml().AndReturn("raw xml")
        http.request("job/jobName/config.xml", postData="raw xml") \
           .AndReturn(("error text", Http.NOT_FOUND))
        mocks.ReplayAll()

        job= Job(http, "jobName")
        result= job.setConfiguration(configuration)

        self.assertEqual(False, result)
