class IJsonParser(object):

    def parse(self, jsonString):
        """
        Convert the json string into a traversable dictionary.
        @type jsonString: str
        @rtype: dict
        """

import json

class JsonParser(IJsonParser):

    def parse(self, jsonString):

        return json.loads(jsonString)
    
