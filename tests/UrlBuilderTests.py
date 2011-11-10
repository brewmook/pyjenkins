from unittest import TestCase

from UrlBuilder import UrlBuilder

class UrlBuilderTests(TestCase):

    def test_build_NoArguments_ReturnCorrectlyJoinedUrl(self):

        builder= UrlBuilder()
        result= builder.build('http', 'host', 'path')

        self.assertEqual('http://host/path', result)

    def test_build_WithArguments_ReturnCorrectlyJoinedUrl(self):

        arguments= {'blah':'whatever',
                    'xyz':'abc'}

        builder= UrlBuilder()
        result= builder.build('http', 'host', 'path', arguments)

        self.assertEqual('http://host/path?blah=whatever&xyz=abc', result)

    def test_build_SpacesInPath_ReturnSpacesEscaped(self):

        builder= UrlBuilder()
        result= builder.build('http', 'host', 'path with spaces')

        self.assertEqual('http://host/path%20with%20spaces', result)
