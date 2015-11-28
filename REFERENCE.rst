=============================
jsonModel Reference Materials
=============================
*Documentation for the list of conditional attributes that can be added to properties of a jsonModel schema.*

Schema Default Behavior
-----------------------
The default behavior of a schema declaration includes validation of structure, datatype
and requirements. Any of these defaults can be turned off in the specification of a
property in the components map. However, for many purposes, the defaults will suffice
to declare model property validation, eliminating the need for further specification in
a components map.

**Schema Example**::

    "schema": {
        "userID": "gY3Cv81QwL0Fs",
        "datetime": 1456000345.543713,
        "active": true,
        "address": {
            "city": "New Orleans",
            "region": "LA",
            "postal_code": "",
            "country: "United States"
        },
        "comments": [ "" ]
    }

Default Settings
^^^^^^^^^^^^^^^^
- **Structure**: The validation process will assume that keys with a declared value exist in each dictionary and that dictionaries or lists with other properties declared inside of them exist in the input. So, the example model expects to see an address field in the top level dictionary which is itself a dictionary with at least city, region and country key-value pairs inside of it. But, on the other hand, there is no requirement that a list of comments exists.
- **Datatype**: The validation process will assume that the datatype of each value in the input matches the datatype in the model. So, the example model expects to see a string for userID, a double-point precision for datetime, a boolean for active, etc...
- **Requirements**: The validation process will assume a key with a non-empty value is a required input. So, all fields in the example are required except postal_code and comments. The empty value for each datatype can be expressed with {}, [], 0, 0.0, false or "" and indicates that it is optional.

Components Map
--------------
The default validation process can be modified, and other (less common) conditionals
can be added through the components map of the model. Whereas the schema map provides
a transparent data architecture that is self-valid, the components map can be used to
specify the conditions of acceptable data for any number of fields in the schema.
The component map is an optional flat dictionary where each key in the component map
designates a particular path in the schema using the '.' and [1] nomenclature of
nesting and array identification.

**Components Example**::

    "components": {
        "userID" {
            "min_length": 13,
            "max_length": 13,
            "must_not_contain": [ "[^a-zA-Z0-9]" ]
        }
        "address.city": {
            "discrete_values": [ "New Orleans", "New York", "Los Angeles", "Miami" ],
            "required_field": false
        },
        "comments[0]": {
            "max_length": 120
        }
    }
Path Definitions
^^^^^^^^^^^^^^^^
To validate additional conditionals placed on a property in the schema, the validation
process looks through the schema for the value associated with a key or item specified
in the key name of the components map. In this example, userID is expected to be found
in the top level dictionary of the schema, address.city refers to the city key inside
the address dictionary inside the schema and comments[0] refers to the first item inside
the comments list. Since the comments list is itself optional, this component is only
validated if there is an item to validate. Otherwise, it is ignored.

List of Field Conditionals
--------------------------
- "**required_field**": false, # a true boolean requires this key-value in the input
- "**value_datatypes**": [], # a list of datatypes which are acceptable types for the value, acceptable items of this list are: [], {}, "", false, 0, 0.0 in the list
- "**byte_data**": false, # a true boolean expects to see base64 byte data in the string field [strings only]
- "**default_value**": None, # a value for an optional property when no value is given
- "**min_length**": 0, # the minimum number of characters in a string [strings only]
- "**max_length**": 0, # the maximum number of characters in a string [strings only]
- "**min_value**": 0, # the minimum value of a number [integers and doubles only]
- "**max_value**": 0, # the maximum value of a number [integers and doubles only]
- "**min_size**": 0, # the minimum number of items in a list [lists only]
- "**max_size**": 0, # the maximum number of items in a list [lists only]
- "**unique_set**": false, # a true boolean treats a list as a set of unique primitives with no duplication [lists of strings and numbers only]
- "**match_first**": false, # a true boolean checks to see that each item of a list matches the construct of the first item [lists only]
- "**must_not_contain**": [], # a list of regular expressions which should not be found in a string [strings only]
- "**must_contain**": [], # a list of regular expressions which must be found in a string [strings only]
- "**discrete_values**": [], # a list of values allowed, this attribute supersedes other qualifying attributes in the component list [integers, doubles and strings only]
- "**identical_to**": "", # the key name in the components map whose value the value of this component must match
- "**lambda_function**": "", # a single argument function which should be run to validate the value of this component, lambda_function must return true (valid) or false (invalid)
- "**validation_url**": "", # an uri which can be called to validate the value of this component with its input in the body of the request, uri response must return true (valid) or false (invalid)
- "**example_values**": [], # a list of values which satisfy all the validation requirements
- "**field_description**": "" # a description of the nature of the component used in documentation









