import mox
from unittest import TestCase

from pyjenkins.server import Server
from pyjenkins.backend.http import Http
from pyjenkins.backend.interfaces import IRequest, IRequestFactory, IUrlBuilder, IUrlBuilderFactory


class HttpTests(TestCase):

    def test_request_WellBehavedFactories_ReturnRequestOpenResult(self):

        expectedResult = ("text", 123)
        arguments = {'something': 'whatever'}
        postData = 'blah blah'
        server = Server('host', 'blah', 'blah')

        mocks = mox.Mox()
        urlBuilder = mocks.CreateMock(IUrlBuilder)
        urlBuilderFactory = mocks.CreateMock(IUrlBuilderFactory)
        request = mocks.CreateMock(IRequest)
        requestFactory = mocks.CreateMock(IRequestFactory)

        urlBuilderFactory.create().AndReturn(urlBuilder)
        urlBuilder.build('host', 'path', arguments).AndReturn('full url')

        requestFactory.create('full url').AndReturn(request)
        request.setBasicAuthorisation(mox.IgnoreArg(), mox.IgnoreArg()).InAnyOrder()
        request.open(postData).InAnyOrder().AndReturn(expectedResult)

        mocks.ReplayAll()

        http = Http(server, urlBuilderFactory, requestFactory)
        result = http.request('path', arguments, postData)

        self.assertEqual(expectedResult, result)

    def test_request_WellBehavedFactories_EnsureAuthenticationIsSet(self):

        expectedResult = ("text", 123)
        arguments = {'something': 'whatever'}
        postData = 'blah blah'
        server = Server('host', 'username', 'password')

        mocks = mox.Mox()
        urlBuilder = mocks.CreateMock(IUrlBuilder)
        urlBuilderFactory = mocks.CreateMock(IUrlBuilderFactory)
        request = mocks.CreateMock(IRequest)
        requestFactory = mocks.CreateMock(IRequestFactory)

        urlBuilderFactory.create().AndReturn(urlBuilder)
        urlBuilder.build('host', 'path', arguments).AndReturn('full url')

        requestFactory.create('full url').AndReturn(request)
        request.setBasicAuthorisation('username', 'password')
        request.open(postData).AndReturn(expectedResult)

        mocks.ReplayAll()

        http = Http(server, urlBuilderFactory, requestFactory)
        http.request('path', arguments, postData)

        mox.Verify(request)

    def test_request_NoUsername_AuthenticationNotSet(self):

        expectedResult = ("text", 123)
        arguments = {'something': 'whatever'}
        postData = 'blah blah'
        server = Server('host', '', 'password anyway')

        mocks = mox.Mox()
        urlBuilder = mocks.CreateMock(IUrlBuilder)
        urlBuilderFactory = mocks.CreateMock(IUrlBuilderFactory)
        request = mocks.CreateMock(IRequest)
        requestFactory = mocks.CreateMock(IRequestFactory)

        urlBuilderFactory.create().AndReturn(urlBuilder)
        urlBuilder.build('host', 'path', arguments).AndReturn('full url')

        requestFactory.create('full url').AndReturn(request)
        request.open(postData).AndReturn(expectedResult)

        mocks.ReplayAll()

        http = Http(server, urlBuilderFactory, requestFactory)
        http.request('path', arguments, postData)

        mox.Verify(request)
