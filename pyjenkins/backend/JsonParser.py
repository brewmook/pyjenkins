import json
from interfaces import IJsonParser

class JsonParser(IJsonParser):

    def parse(self, jsonString):

        return json.loads(jsonString)
    
