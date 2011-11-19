class IJson(object):

    def parse(self, jsonString):
        '''
        Convert the json string into a dictionary
        '''

import json

class Json(IJson):

    def parse(self, jsonString):

        return json.loads(jsonString)
    
