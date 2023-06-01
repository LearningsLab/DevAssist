# Data parsing Service will help in parsing the data taken from any source and then convert it into a format that can be used by the model.

import json

class DataParsingService:
    @staticmethod
    def string_to_json(data):
        try:
            json_data = json.loads(data)
            return json_data
        except json.JSONDecodeError:
            print("Error: Invalid JSON data")
            return None
    
    @staticmethod
    def json_to_string(data):
        try:
            text_data = json.dumps(data)
            return text_data
        except TypeError:
            print("Error: Invalid JSON object")
            return None

