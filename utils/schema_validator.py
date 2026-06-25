import json
from jsonschema import validate, ValidationError

def validate_json_schema(json_data, schema_file):
    """
    Validate JSON data against a JSON schema.

    :param json_data: The JSON data to validate (as a dictionary).
    :param schema_file: Path to the JSON schema file.
    :return: True if valid, raises ValidationError if invalid.
    """
    with open(schema_file, 'r') as file:
        schema = json.load(file)

    try:
        validate(instance=json_data, schema=schema)
        return True
    except ValidationError as e:
        raise ValidationError(f"JSON data is invalid: {e.message}")