from unittest import TestCase

from pyjenkins.jobfilters import FailingJobs

class FailingJobsTests(TestCase):

    def test_includeJob_StatusFailing_ReturnTrue(self):

        filter= FailingJobs()
        result= filter.includeJob('spam', 'red')
        self.assertEqual(True, result)

    def test_includeJob_StatusOk_ReturnFalse(self):

        filter= FailingJobs()
        result= filter.includeJob('spam', 'blue')
        self.assertEqual(False, result)

    def test_includeJob_StatusUnknown_ReturnFalse(self):

        filter= FailingJobs()
        result= filter.includeJob('spam', 'grey')
        self.assertEqual(False, result)
