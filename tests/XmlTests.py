import mox
from unittest import TestCase

from Xml import Xml

class XmlTests(TestCase):

    def test_toString_NoChangesMade_ReturnOriginalXml(self):

        xml= Xml('raw xml')
        
        result= xml.toString()

        self.assertEqual('raw xml', result)

    def test_toString_setFirstNodeTextReturnsTrue_ReturnModifiedXml(self):

        xml= Xml('<element><other>text</other></element>')

        xml.setFirstNodeText('//other', 'pies')

        result= xml.toString()

        self.assertEqual('<element><other>pies</other></element>', result)

    def test_toString_setFirstNodeTextReturnsFalse_ReturnOriginalXml(self):

        xml= Xml('<element><other>text</other></element>')

        xml.setFirstNodeText('//notfound', 'whatever')

        result= xml.toString()

        self.assertEqual('<element><other>text</other></element>', result)

    def test_toString_XmlHeaderAndSetFirstNodeTextReturnsTrue_XmlHeaderRemoved(self):

        xml= Xml("<?xml version='1.0' encoding='UTF-8'?>\n<element><other>text</other></element>")

        xml.setFirstNodeText('//other', 'pies')

        result= xml.toString()

        self.assertEqual('<element><other>pies</other></element>', result)

    def test_setFirstNodeText_XPathNodeDoesNotExist_ReturnFalse(self):

        xml= Xml('<element><other>text</other></element>')

        result= xml.setFirstNodeText('//pies', 'whatever')

        self.assertEqual(False, result)

    def test_setFirstNodeText_XPathNodeExists_ReturnTrue(self):

        xml= Xml('<element><other>text</other></element>')

        result= xml.setFirstNodeText('//other', 'whatever')

        self.assertEqual(True, result)

    def test_getFirstNodeText_XPathNodeExists_ReturnNodeContents(self):

        xml= Xml('<stuff><things>words words</things></stuff>')

        result= xml.getFirstNodeText('//things')

        self.assertEqual('words words', result)

    def test_getFirstNodeText_XPathNodeDoesNotExist_ReturnNone(self):

        xml= Xml('<stuff><things>words words</things></stuff>')

        result= xml.getFirstNodeText('//friday')

        self.assertEqual(None, result)
