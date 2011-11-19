from xml.etree import ElementTree

class IXmlFactory:

    def create(self, rawXmlString):
        pass

class IXml:

    def toString(self):
        '''
        Return raw xml contents
        '''

    def getFirstNodeText(self, xpath):
        '''
        Finds the first node with the specified xpath and returns its contents as text.

        Returns the contents if a node was found, None otherwise.
        '''
        
    def setFirstNodeText(self, xpath, text):
        '''
        Finds the first node with the specified xpath and sets its contents to text.

        Returns True if a node was found, False otherwise.
        '''

class Xml:

    def __init__(self, rawXmlString):

        root = ElementTree.fromstring(rawXmlString)
        self.tree = ElementTree.ElementTree(root)

    def toString(self):

        return ElementTree.tostring(self.tree.getroot())

    def getFirstNodeText(self, xpath):

        result= None
        element = self.tree.find(xpath)

        if element != None:
            result= element.text

        return result

    def setFirstNodeText(self, xpath, text):

        result= False
        element = self.tree.find(xpath)

        if element != None:
            element.text = text
            result= True

        return result

class XmlFactory:

    def create(self, rawXmlString):
        return Xml(rawXmlString)
