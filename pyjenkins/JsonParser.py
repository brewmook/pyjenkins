import json
from pyjenkins.interfaces import IJsonParser

class JsonParser(IJsonParser):

    def parse(self, jsonString):

        return json.loads(jsonString)
    
