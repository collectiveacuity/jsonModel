=============================
jsonModel Reference Materials
=============================
*Documentation for model declaration and error handling for jsonModel validation.*

Schema Default Behavior
-----------------------
The default behavior of a schema declaration includes validation of structure, datatype and requirements. Any of these defaults can be turned off in the specification of a property in the components map. However, for many purposes, the defaults will suffice to declare model property validation, eliminating the need for further specification in a components map.

**Schema Example**::

    "schema": {
        "userID": "gY3Cv81QwL0Fs",
        "datetime": 1456000345.543713,
        "active": true,
        "address": {
            "city": "New Orleans",
            "region": "LA",
            "postal_code": "",
            "country": "United States"
        },
        "comments": [ "strings" ]
    }

Default Settings
^^^^^^^^^^^^^^^^
- **Structure**: The validation process will assume that a dictionary (including the top-level dictionary) defines its maximum scope of key names and that lists can contain any number of items. Lists cannot contain mixed datatypes and the structure of the first item in a list defines the allowable properties of each item in the list. So, the example model expects to find only the userID, datetime, active, address and comments fields and it will accept any number of strings in the comments list.
- **Datatype**: The validation process will assume that the datatype of each value in the input matches the datatype in the model. So, the example model expects to see a string for userID, a number for datetime, a boolean for active, etc...
- **Requirements**: The validation process will assume a key with a non-empty value is a required input. On top of this, a list with a single item it is also considered optional so that there is a placeholder with which to declare the format of the contents of the list. So, all fields in the example are required except postal_code and comments. The empty value for each datatype can be expressed with {}, [], 0, 0.0, false or "" and indicates that it is optional.

Components Map
--------------
The default validation process can be modified, and other (less common) conditionals can be added through the components map of the model. Whereas the schema map provides a transparent data architecture that is self-valid, the components map can be used to specify the conditions of acceptable data for any number of fields in the schema. The component map is an optional flat dictionary where each key in the component map designates a particular path in the schema using the '.' and [0] nomenclature of nesting and array identification.

**Components Example**::

    "components": {
        ".": {
            "extra_fields": true
        },
        ".userID": {
            "min_length": 13,
            "max_length": 13,
            "must_not_contain": [ "[^\\w]", "_" ]
        },
        ".address.city": {
            "discrete_values": [ "New Orleans", "New York", "Los Angeles", "Miami" ],
            "required_field": false
        },
        ".comments[0]": {
            "max_length": 120
        }
    }
Path Definitions
^^^^^^^^^^^^^^^^
To validate additional conditionals placed on a property in the schema, the validation process looks through the schema for the value associated with a key or item specified in the key name of the components map. In this example, a key named "userID" is expected to be found in the top level map of the schema, .address.city refers to the "city" key inside the "address" map inside the schema map and .comments[0] refers to the first item inside the comments list.  Since the comments list is itself optional, this component is only validated if there is an item to validate. Otherwise, it is ignored. "." is the key name for the top-level map itself and the "extra_fields" conditional changes the default to allow the top-level map to accept undeclared keys.

List of Field Conditionals (and default values)
-----------------------------------------------
- "**value_datatype**": null, # **IMMUTABLE** / DEFINED IN SCHEMA / error_code: 4001
- "**required_field**": false, # a true boolean requires this key-value in the input / error_code: 4002
- "**extra_fields**": false, # a true boolean allows map to contain undeclared keys / error_code: 4003 / [**maps only**]
- "**default_value**": null, # a value for an optional property when no value is given
- "**byte_data**": false, # a true boolean expects to see base64 byte data in the string field [strings only]
- "**min_length**": 0, # the minimum number of characters in a string [strings only]
- "**max_length**": 0, # the maximum number of characters in a string [strings only]
- "**must_not_contain**": [], # a list of regular expressions which should not be found in a string [strings only]
- "**must_contain**": [], # a list of regular expressions which must be found in a string [strings only]
- "**min_value**": 0, # the minimum value of a number [numbers only]
- "**max_value**": 0, # the maximum value of a number [numbers only]
- "**min_size**": 0, # the minimum number of items in a list [lists only]
- "**max_size**": 0, # the maximum number of items in a list [lists only]
- "**unique_set**": false, # a true boolean treats a list as a set of unique primitives with no duplication [lists of strings and numbers only]
- "**match_first**": false, # a true boolean checks to see that each item of a list matches the construct of the first item [lists only]
- "**discrete_values**": [], # a list of values allowed, this attribute supersedes other qualifying attributes in the component list [numbers and strings only]
- "**identical_to**": "", # the key name in the components map whose value the value of this component must match
- "**lambda_function**": "", # a single argument function which should be run to validate the value of this component, lambda_function must return true (valid) or false (invalid)
- "**validation_url**": "", # an uri which can be called to validate the value of this component with its input in the body of the request, uri response must return true (valid) or false (invalid)
- "**example_values**": [], # a list of values which satisfy all the validation requirements [ numbers and strings only ]
- "**field_description**": "" # a description of the nature of the component used in documentation

Error Handling
--------------
Errors created from improper model specification will raise a ModelValidationError with a message that is designed to help determine the source of the model declaration error. To ensure that model initialization occurs properly, no error encoding is included to handle these exceptions. However, it is expected that validation of inputs will through errors. Otherwise, what's the point?! So, in addition to a text report, a dictionary has been included with the InputValidationError exception to facilitate error handling.

**Error Method Example**::

    self.error = {
        'input_criteria': self.keyMap['.'],
        'failed_test': 'value_datatype',
        'input_path': '.',
        'error_value': input_dict.__class__,
        'error_code': 4001
    }
Order of Exceptions
^^^^^^^^^^^^^^^^^^^
The validation process will raise an error as soon as it encounters one, so there is no guarantee that the error that is reported is the only error in the input. However the steps of the validation process are designed to tackle the largest scope first before they drill down. Here is the order of error exception:

#. Required keys in a dictionary
#. Extra keys in a dictionary
#. Individual fields in the dictionary

- #. Datatype of value
- #. Non-empty value
- #. Other value qualifiers

To help the process of error handling and client-server negotiation, the input_criteria is included in the error dictionary as a map of all the conditional qualifiers which are associated with a particular field in the input.









