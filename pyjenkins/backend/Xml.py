from xml.etree import ElementTree

from pyjenkins.interfaces import IXml, IXmlFactory

class Xml(IXml):

    def __init__(self, rawXmlString):

        root = ElementTree.fromstring(rawXmlString)
        self.tree = ElementTree.ElementTree(root)

    def toString(self):

        return ElementTree.tostring(self.tree.getroot())

    def getFirstNodeText(self, xpath):

        result= None
        element = self.tree.find(xpath)

        if element is not None:
            result= element.text

        return result

    def setFirstNodeText(self, xpath, text):

        result= False
        element = self.tree.find(xpath)

        if element is not None:
            element.text = text
            result= True

        return result

class XmlFactory(IXmlFactory):

    def create(self, rawXmlString):
        return Xml(rawXmlString)
