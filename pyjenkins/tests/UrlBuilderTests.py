from unittest import TestCase

from UrlBuilder import UrlBuilder

class UrlBuilderTests(TestCase):

    def test_build_NoArguments_ReturnCorrectlyJoinedUrl(self):

        builder= UrlBuilder()
        result= builder.build('host', 'path')

        self.assertEqual('host/path', result)

    def test_build_WithArguments_ReturnCorrectlyJoinedUrl(self):

        arguments= {'blah':'whatever',
                    'xyz':'abc'}

        builder= UrlBuilder()
        result= builder.build('host', 'path', arguments)

        self.assertEqual('host/path?blah=whatever&xyz=abc', result)

    def test_build_SpacesInPath_ReturnSpacesEscaped(self):

        builder= UrlBuilder()
        result= builder.build('host', 'path with spaces')

        self.assertEqual('host/path%20with%20spaces', result)
