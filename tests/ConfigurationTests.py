import mox
from unittest import TestCase

from Configuration import Configuration
from Xml import IXml

class ConfigurationTests(TestCase):

    def test_rawXml_NoChangesMade_ReturnOriginalXml(self):

        mocks= mox.Mox()
        xml= mocks.CreateMock(IXml)

        xml.toString().AndReturn('the raw xml')
        mocks.ReplayAll()

        configuration= Configuration(xml)
        
        result= configuration.rawXml()

        self.assertEqual('the raw xml', result)

    def test_setSubversionRepository_SubversionRepositoryExists_ReturnTrue(self):

        mocks= mox.Mox()
        xml= mocks.CreateMock(IXml)

        xml.setFirstNodeText('//hudson.scm.SubversionSCM_-ModuleLocation/remote',
                             'http://host/path/to/repo') \
            .AndReturn(True)
        mocks.ReplayAll()

        configuration= Configuration(xml)
        result= configuration.setSubversionRepository('http://host/path/to/repo')

        self.assertEqual(True, result)

    def test_setSubversionRepository_SubversionRepositoryExists_ReturnFalse(self):

        mocks= mox.Mox()
        xml= mocks.CreateMock(IXml)

        xml.setFirstNodeText('//hudson.scm.SubversionSCM_-ModuleLocation/remote',
                             'http://host/path/to/repo') \
            .AndReturn(False)
        mocks.ReplayAll()

        configuration= Configuration(xml)
        result= configuration.setSubversionRepository('http://host/path/to/repo')

        self.assertEqual(False, result)

    def test_subversionRepository_CorrectXPathUsed_ReturnResultFromXml(self):

        mocks= mox.Mox()
        xml= mocks.CreateMock(IXml)

        xml.getFirstNodeText('//hudson.scm.SubversionSCM_-ModuleLocation/remote') \
            .AndReturn('http://host/path/to/repository')
        mocks.ReplayAll()

        configuration= Configuration(xml)
        result= configuration.subversionRepository()

        self.assertEqual('http://host/path/to/repository', result)

    def test_setChildProjects_AlreadyExists_ReturnTrue(self):

        mocks= mox.Mox()
        xml= mocks.CreateMock(IXml)

        xml.setFirstNodeText('/project/publishers/hudson.tasks.BuildTrigger/childProjects',
                             'tests job') \
            .AndReturn(True)
        mocks.ReplayAll()

        configuration= Configuration(xml)
        result= configuration.setChildProjects('tests job')

        self.assertEqual(True, result)

    def test_setChildProjects_XPathKeyNotFound_ReturnFalse(self):

        mocks= mox.Mox()
        xml= mocks.CreateMock(IXml)

        xml.setFirstNodeText('/project/publishers/hudson.tasks.BuildTrigger/childProjects',
                             'tests job') \
            .AndReturn(False)
        mocks.ReplayAll()

        configuration= Configuration(xml)
        result= configuration.setChildProjects('tests job')

        self.assertEqual(False, result)
