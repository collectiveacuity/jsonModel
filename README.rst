=========
jsonModel
=========
*A Collection of Methods for Validating JSON Structured Data*

:Documentation: http://jsonModel.readthedocs.org/
:Downloads: http://pypi.python.org/pypi/jsonModel
:Source: https://github.com/collectiveacuity/jsonModel

Top-Level Classes
-----------------
* **jsonModel**: a schema-enforced class for json data validation

Features
--------
- Alternative to json schema
- Schema declaration is self-valid
- Built-in validation of model declaration
- Flat structure to declarations of property attributes
- Accommodates additional functions for property validation

Installation
^^^^^^^^^^^^
From PyPi::

    $ pip install jsonModel

From GitHub::

    $ pip install git+https://github.com/collectiveacuity/jsonModel


Getting Started
^^^^^^^^^^^^^^^
This module is designed to facilitate the process of implementing data validation against a declared json data model. jsonModel offers a more intuitive declaration process than other schema enforcement modules currently available by relying upon the architecture of json itself to validate datatypes, requirements and defaults. For many data models, full validation can be achieved from an example declaration::

    "schema": {
        "userID": "gY3Cv81QwL0Fs",
        "datetime": 1456000345.543713,
        "active": true,
        "address": {
            "city": "New Orleans",
            "region": "LA",
            "postal_code": "",
            "country: "United States"
        }
    }


*[Validation of input against this model declaration requires values for all four top level keys and that each key value must be the corresponding datatype in the model. For the address field, the value for all keys except postal_code are required string inputs. If a value is provided for postal_code, it must be a string.]*

In addition to intuitive self-valid schema declarations, jsonModel also offers a rich way to further refine the conditionality of any property in the model through a components map of keys whose name corresponds to the path to the schema property::

    "components": {
        "userID" {
            "min_length": 13,
            "max_length": 13,
            "must_not_contain": [ "[^a-zA-Z0-9]" ]
        }
        "address.city": {
            "discrete_values": [ "New Orleans", "New York", "Los Angeles", "Miami" ],
            "required_field": false
        }
    }


*[Validation of any input against this model also checks the paths designated in the components dictionary to make sure that values do not violate any of the declared additional attributes of the property. Whenever they may conflict with the attributes declared in the schema example, the conditions in the components map supersedes. So, in this case, the requirement that an address contain a city has been turned off. But if a city is provided, it must match one of the four city values provided. Likewise, any value provided in userID must be 13 characters long and can only be composed of alphanumerical characters.]*

This module also validates the architecture of the model declarations themselves to facilitate the model design process and ensure that no models break the rules of the module. Error reports are provided to identity the scope of conditionals applicable to any given property in addition to the module documentation.

To declare the model (components is optional)::

    {
        "schema": {
            "property": "value"
        },
        "components": {}
    }

To initialize the class object::

    from jsonModel import jsonModel
    import json

    sampleModel = json.loads(open('sample-model.json').read())
    validModel = jsonModel(sampleModel)


To validate input against model declaration::

    validModel.validate(input)


For more details about how to use jsonModel, refer to the
`Reference Documentation on Github
<https://github.com/collectiveacuity/jsonModel/REFERENCE.rst>`_