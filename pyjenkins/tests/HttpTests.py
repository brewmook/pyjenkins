import mox
from unittest import TestCase

from pyjenkins.Http import Http

from pyjenkins.UrlBuilder import IUrlBuilder, IUrlBuilderFactory
from pyjenkins.Request import IRequest, IRequestFactory

class HttpTests(TestCase):

    def test_request_WellBehavedFactories_ReturnRequestOpenResult(self):

        expectedResult = ("text", 123)
        arguments = { 'something' : 'whatever' }
        postData = 'blah blah'

        mocks= mox.Mox();
        urlBuilder= mocks.CreateMock(IUrlBuilder)
        urlBuilderFactory= mocks.CreateMock(IUrlBuilderFactory)
        request= mocks.CreateMock(IRequest)
        requestFactory= mocks.CreateMock(IRequestFactory)

        urlBuilderFactory.create().AndReturn(urlBuilder)
        urlBuilder.build('host', 'path', arguments).AndReturn('full url')

        requestFactory.create('full url').AndReturn(request)
        request.setBasicAuthorisation(mox.IgnoreArg(), mox.IgnoreArg()).InAnyOrder()
        request.open(postData).InAnyOrder().AndReturn(expectedResult)

        mocks.ReplayAll()

        http= Http('host', 'blah', 'blah', urlBuilderFactory, requestFactory)
        result= http.request('path', arguments, postData)

        self.assertEqual(expectedResult, result)

    def test_request_WellBehavedFactories_EnsureAuthenticationIsSet(self):

        expectedResult = ("text", 123)
        arguments = { 'something' : 'whatever' }
        postData = 'blah blah'

        mocks= mox.Mox();
        urlBuilder= mocks.CreateMock(IUrlBuilder)
        urlBuilderFactory= mocks.CreateMock(IUrlBuilderFactory)
        request= mocks.CreateMock(IRequest)
        requestFactory= mocks.CreateMock(IRequestFactory)

        urlBuilderFactory.create().AndReturn(urlBuilder)
        urlBuilder.build('host', 'path', arguments).AndReturn('full url')

        requestFactory.create('full url').AndReturn(request)
        request.setBasicAuthorisation('username', 'password')
        request.open(postData).AndReturn(expectedResult)

        mocks.ReplayAll()

        http= Http('host', 'username', 'password', urlBuilderFactory, requestFactory)
        http.request('path', arguments, postData)

        mox.Verify(request)
