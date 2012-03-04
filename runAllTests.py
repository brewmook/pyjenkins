#!/usr/bin/python

import unittest
import sys

from tests.ConfigurationTests import ConfigurationTests  # @UnusedImport
from tests.JenkinsTests import JenkinsTests  # @UnusedImport
from tests.JobTests import JobTests  # @UnusedImport
from tests.ServerTests import ServerTests  # @UnusedImport

from tests.backend.HttpTests import HttpTests  # @UnusedImport
from tests.backend.UrlBuilderTests import UrlBuilderTests  # @UnusedImport
from tests.backend.XmlTests import XmlTests  # @UnusedImport

if __name__ == '__main__':
    unittest.main(testRunner=unittest.TextTestRunner(stream=sys.stdout, verbosity=2))
