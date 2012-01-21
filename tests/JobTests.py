from unittest import TestCase

from pyjenkins.Job import Job, JobStatus

class JobTests(TestCase):

    def test_constructor_NameAttributeMatchesThatPassedIn(self):

        job= Job('a name', 'whatever')
        self.assertEqual('a name', job.name)

    def test_constructor_StatusAttributeMatchesThatPassedIn(self):

        job= Job('spam', JobStatus.FAILING)
        self.assertEqual(JobStatus.FAILING, job.status)
