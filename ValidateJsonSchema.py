import json
import jsonschema
from jsonschema import validate


def should_match_schema(schema, test):
    schemaJson = json.loads(schema)
    test_json = json.loads(test)
    validate(test_json, schemaJson, format_checker = jsonschema.FormatChecker())
