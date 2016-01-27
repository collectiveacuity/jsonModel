__author__ = 'rcj1492'
__created__ = '2016.01'

modelRules = {
    "schema": {
        "string_fields": "",
        "similar_string": "",
        "number_fields": 0.0,
        "similar_number": 0,
        "boolean_fields": False,
        "similar_boolean": False,
        "map_fields": {},
        "similar_map": {},
        "list_fields": [],
        "similar_list": []
    },
    "components": {
        ".string_fields": {
            "required_field": False,
            "default_value": "",
            "byte_data": False,
            "min_length": 0,
            "max_length": 0,
            "must_not_contain": [],
            "must_contain": [],
            "contains_either": [],
            "discrete_values": [],
            "identical_to": ".similar_string",
            "lambda_function": "",
            "validation_url": "",
            "example_values": [],
            "field_description": ""
        },
        ".number_fields": {
            "required_field": False,
            "default_value": 0.0,
            "min_value": 0.0,
            "max_value": 0.0,
            "integer_only": False,
            "discrete_values": [],
            "identical_to": ".similar_number",
            "lambda_function": "",
            "validation_url": "",
            "example_values": [],
            "field_description": ""
        },
        ".boolean_fields": {
            "required_field": False,
            "default_value": False,
            "identical_to": ".similar_boolean",
            "lambda_function": "",
            "validation_url": "",
            "field_description": ""
        },
        ".map_fields": {
            "required_field": False,
            "extra_fields": False,
            "identical_to": ".similar_map",
            "lambda_function": "",
            "validation_url": "",
            "field_description": ""
        },
        ".list_fields": {
            "required_field": False,
            "min_size": 0,
            "max_size": 0,
            "unique_values": False,
            "identical_to": ".similar_list",
            "lambda_function": "",
            "validation_url": "",
            "field_description": ""
        }
    },
    "title": "",
    "url": "",
    "max_size": 0
}