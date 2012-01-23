from unittest import TestCase

from pyjenkins.server import Server

class ServerTests(TestCase):

    def test_constructor_HostAttributeMatchesThatPassedIn(self):

        server = Server('a host', 'whatever', 'whatever')
        self.assertEqual('a host', server.host)

    def test_constructor_UsernameAttributeMatchesThatPassedIn(self):

        server = Server('whatever', 'a username', 'whatever')
        self.assertEqual('a username', server.username)

    def test_constructor_PasswordAttributeMatchesThatPassedIn(self):

        server = Server('whatever', 'whatever', 'a password')
        self.assertEqual('a password', server.password)

    def test_equalityop_TwoEquivalentObjects_ReturnTrue(self):

        serverOne = Server('host', 'username', 'password')
        serverTwo = Server('host', 'username', 'password')

        self.assertTrue(serverOne == serverTwo)

    def test_equalityop_HostsDiffer_ReturnFalse(self):

        serverOne = Server('host A', 'username', 'password')
        serverTwo = Server('host B', 'username', 'password')

        self.assertFalse(serverOne == serverTwo)

    def test_equalityop_UsernamesDiffer_ReturnFalse(self):

        serverOne = Server('host', 'username A', 'password')
        serverTwo = Server('host', 'username B', 'password')

        self.assertFalse(serverOne == serverTwo)

    def test_equalityop_PasswordsDiffer_ReturnFalse(self):

        serverOne = Server('host', 'username', 'password A')
        serverTwo = Server('host', 'username', 'password B')

        self.assertFalse(serverOne == serverTwo)

    def test_repr_ReturnsSensibleResult(self):

        server = Server('bacon', 'eggs', 'spam')
        self.assertEquals("Server(host='bacon',username='eggs',password='spam')", server.__repr__())
