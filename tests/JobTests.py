from unittest import TestCase

from pyjenkins.job import Job, JobStatus

class JobTests(TestCase):

    def test_constructor_NameAttributeMatchesThatPassedIn(self):

        job= Job('a name', 'whatever')
        self.assertEqual('a name', job.name)

    def test_constructor_StatusAttributeMatchesThatPassedIn(self):

        job= Job('spam', JobStatus.FAILING)
        self.assertEqual(JobStatus.FAILING, job.status)

    def test_equalityop_TwoEquivalentObjects_ReturnTrue(self):

        jobOne= Job('spam', JobStatus.FAILING)
        jobTwo= Job('spam', JobStatus.FAILING)

        self.assertTrue(jobOne == jobTwo)

    def test_equalityop_NamesDiffer_ReturnFalse(self):

        jobOne= Job('spam', JobStatus.FAILING)
        jobTwo= Job('eggs', JobStatus.FAILING)

        self.assertFalse(jobOne == jobTwo)

    def test_equalityop_StatusDiffer_ReturnFalse(self):

        jobOne= Job('eggs', JobStatus.FAILING)
        jobTwo= Job('eggs', JobStatus.UNKNOWN)

        self.assertFalse(jobOne == jobTwo)

    def test_repr_ReturnsSensibleResult(self):

        job= Job('spam', JobStatus.OK)
        self.assertEquals("Job(name='spam',status='OK')", job.__repr__())
