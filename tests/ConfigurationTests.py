import mox
from unittest import TestCase

from pyjenkins.configuration import Configuration
from pyjenkins.backend.interfaces import IXml


class ConfigurationTests(TestCase):

    def test_rawXml_NoChangesMade_ReturnOriginalXml(self):

        mocks = mox.Mox()
        xml = mocks.CreateMock(IXml)

        xml.toString().AndReturn('the raw xml')
        mocks.ReplayAll()

        configuration = Configuration(xml)

        result = configuration.rawXml()

        self.assertEqual('the raw xml', result)

    def test_setSubversionRepository_XmlExpectsAppropriateKey_ReturnWhateverXmlReturns(self):

        mocks = mox.Mox()
        xml = mocks.CreateMock(IXml)

        xml.setFirstNodeText('.//hudson.scm.SubversionSCM_-ModuleLocation/remote',
                             'http://host/path/to/repo') \
            .AndReturn('mangos')
        mocks.ReplayAll()

        configuration = Configuration(xml)
        result = configuration.setSubversionRepository('http://host/path/to/repo')

        self.assertEqual('mangos', result)

    def test_subversionRepository_XmlExpectsAppropriateKey_ReturnWhateverXmlReturns(self):

        mocks = mox.Mox()
        xml = mocks.CreateMock(IXml)

        xml.getFirstNodeText('.//hudson.scm.SubversionSCM_-ModuleLocation/remote') \
            .AndReturn('http://host/path/to/repository')
        mocks.ReplayAll()

        configuration = Configuration(xml)
        result = configuration.subversionRepository()

        self.assertEqual('http://host/path/to/repository', result)

    def test_setChildProjects_XmlExpectsAppropriateKey_ReturnWhateverXmlReturns(self):

        mocks = mox.Mox()
        xml = mocks.CreateMock(IXml)

        xml.setFirstNodeText('.//hudson.tasks.BuildTrigger/childProjects',
                             'tests job') \
            .AndReturn('kiwis')
        mocks.ReplayAll()

        configuration = Configuration(xml)
        result = configuration.setChildProjects('tests job')

        self.assertEqual('kiwis', result)

    def test_setCopyArtifactsJobName_XmlExpectsAppropriateKey_ReturnWhateverXmlReturns(self):

        mocks = mox.Mox()
        xml = mocks.CreateMock(IXml)

        xml.setFirstNodeText('.//hudson.plugins.copyartifact.CopyArtifact/projectName',
                             'build job') \
            .AndReturn('bananas')
        mocks.ReplayAll()

        configuration = Configuration(xml)
        result = configuration.setCopyArtifactsJobName('build job')

        self.assertEqual('bananas', result)
