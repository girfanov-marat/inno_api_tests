import json

from jsonpath_ng import parse


def json_extractor(json_string, expression):
    data = []
    json_data = json.loads(json_string)
    jsonpath_expression = parse(expression)
    matches = jsonpath_expression.find(json_data)
    for match in matches:
        data.append(match.value)
    return data
