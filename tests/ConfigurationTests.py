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
