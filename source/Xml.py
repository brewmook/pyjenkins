class IXmlFactory:

    def create(self, rawXmlString):
        pass

class IXml:

    def toString(self):
        '''
        Return raw xml contents
        '''

    def setFirstNodeText(self, xpath, text):
        '''
        Finds the first node with the specified xpath and sets its contents to text.

        Returns True if a node was found, False otherwise.
        '''

class Xml:

    def __init__(self, rawXmlString):

        self.xml= rawXmlString

    def toString(self):

        return self.xml

    def setFirstNodeText(self, xpath, text):

        pass

class XmlFactory:

    def create(self, rawXmlString):
        return Xml(rawXmlString)
