#!/usr/bin/python

import unittest
import sys
import os

from tests.ConfigurationTests import ConfigurationTests
from tests.EventTests import EventTests
from tests.JenkinsTests import JenkinsTests
from tests.JobTests import JobTests

from tests.backend.HttpTests import HttpTests
from tests.backend.UrlBuilderTests import UrlBuilderTests
from tests.backend.XmlTests import XmlTests

if __name__ == '__main__':
    unittest.main(testRunner= unittest.TextTestRunner(stream= sys.stdout, verbosity=2))
