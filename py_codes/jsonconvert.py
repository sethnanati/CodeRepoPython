import json

with open('/Users/adeyemiadenuga/Downloads/calendar.txt') as reader:
    json_data = reader.read()
    json_object = json.loads(json_data)
    json_formatted_str = json.dumps(json_object, indent=2)
    print(json_formatted_str)