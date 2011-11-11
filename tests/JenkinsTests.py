import mox
from unittest import TestCase

from Jenkins import Jenkins

from Http import IHttp
from Job import IJob, IJobFactory

class JenkinsTests(TestCase):

    def test_copyJob_SourceExistsAndTargetDoesNotExistCopySuccess_ReturnTargetJob(self):

        mocks= mox.Mox();
        http= mocks.CreateMock(IHttp)
        jobFactory= mocks.CreateMock(IJobFactory)
        sourceJob= mocks.CreateMock(IJob)
        targetJob= mocks.CreateMock(IJob)
        
        jobFactory.create('source').AndReturn(sourceJob)
        jobFactory.create('target').AndReturn(targetJob)
        sourceJob.exists().AndReturn(True)
        targetJob.exists().AndReturn(False)
        targetJob.createCopy('source').AndReturn(True)

        mocks.ReplayAll()

        jenkins = Jenkins(http)
        jenkins.jobFactory= jobFactory

        result= jenkins.copyJob('source', 'target')

        self.assertEqual(targetJob, result)

    def test_copyJob_SourceJobDoesNotExist_ReturnNone(self):

        mocks= mox.Mox();
        http= mocks.CreateMock(IHttp)
        jobFactory= mocks.CreateMock(IJobFactory)
        sourceJob= mocks.CreateMock(IJob)
        
        jobFactory.create('source').AndReturn(sourceJob)
        sourceJob.exists().AndReturn(False)

        mocks.ReplayAll()

        jenkins = Jenkins(http)
        jenkins.jobFactory= jobFactory

        result= jenkins.copyJob('source', 'target')

        self.assertEqual(None, result)

    def test_copyJob_TargetAlreadyExists_ReturnNone(self):

        mocks= mox.Mox();
        http= mocks.CreateMock(IHttp)
        jobFactory= mocks.CreateMock(IJobFactory)
        sourceJob= mocks.CreateMock(IJob)
        targetJob= mocks.CreateMock(IJob)
        
        jobFactory.create('source').AndReturn(sourceJob)
        jobFactory.create('target').AndReturn(targetJob)
        sourceJob.exists().AndReturn(True)
        targetJob.exists().AndReturn(True)

        mocks.ReplayAll()

        jenkins = Jenkins(http)
        jenkins.jobFactory= jobFactory

        result= jenkins.copyJob('source', 'target')

        self.assertEqual(None, result)

    def test_copyJob_CopyFails_ReturnNone(self):

        mocks= mox.Mox();
        http= mocks.CreateMock(IHttp)
        jobFactory= mocks.CreateMock(IJobFactory)
        sourceJob= mocks.CreateMock(IJob)
        targetJob= mocks.CreateMock(IJob)
        
        jobFactory.create('source').AndReturn(sourceJob)
        jobFactory.create('target').AndReturn(targetJob)
        sourceJob.exists().AndReturn(True)
        targetJob.exists().AndReturn(False)
        targetJob.createCopy('source').AndReturn(False)

        mocks.ReplayAll()

        jenkins = Jenkins(http)
        jenkins.jobFactory= jobFactory

        result= jenkins.copyJob('source', 'target')

        self.assertEqual(None, result)
