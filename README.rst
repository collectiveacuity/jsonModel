.. image:: https://img.shields.io/pypi/v/jsonmodel.svg
    :target: https://pypi.python.org/pypi/jsonmodel
.. image:: https://img.shields.io/pypi/dm/jsonmodel.svg
    :target: https://pypi.python.org/pypi/jsonmodel
.. image:: https://img.shields.io/pypi/l/jsonmodel.svg
    :target: https://pypi.python.org/pypi/jsonmodel

=========
jsonModel
=========
*A Collection of Methods for Validating JSON Structured Data*

:Downloads: http://pypi.python.org/pypi/jsonModel
:Source: https://github.com/collectiveacuity/jsonModel

Top-Level Classes
-----------------
* **jsonModel**: a schema-enforceable class for json data validation

Features
--------
- Validates native json datatypes
- Validates byte data as base64 encoded strings
- Alternative to json schema module
- Schema declaration is self-valid
- Built-in validation of model declaration
- Flat structure to object property attribute declarations
- Ability to assign default values to inputs
- Validates individual components in a model
- Ingests arbitrary keyword data and outputs model valid dictionary

============
Installation
============
From PyPi::

    $ pip install jsonmodel

From GitHub::

    $ git clone https://github.com/collectiveacuity/jsonModel
    $ cd jsonModel
    $ python setup.py install

Getting Started
---------------
This module is designed to facilitate the process of implementing data validation against a declared json data model. jsonModel offers a more intuitive declaration process than other schema enforcement modules currently available by relying upon the architecture of json itself to validate datatypes, requirements and defaults. For many data models, full validation can be achieved from an example declaration::

    "schema": {
        "userID": "gY3Cv81QwL0Fs",
        "datetime": 1456000345.543713,
        "active": true,
        "address": {
            "city": "New Orleans",
            "region": "LA",
            "postal_code": "",
            "country": "United States"
        }
    }


*[In this model, the input must contain values for all four top level keys and each value must correspond to the datatype in the model. So, the input must have a userID field with a string, a datetime field with a number, an active key with a boolean and the address field must be a dictionary which itself contains city, region and country values. Since it is empty, postal_code is optional. If a value is provided for postal_code however, it must be a string.]*

In addition to intuitive self-valid schema declarations, jsonModel also offers a rich way to further refine the conditionality of any property in the model through an accompanying components map whose key names correspond to the path to the schema property which requires additional validation::

    "components": {
        ".userID": {
            "min_length": 13,
            "max_length": 13,
            "must_not_contain": [ "[^\\w]", "_" ]
        },
        ".address.city": {
            "discrete_values": [ "New Orleans", "New York", "Los Angeles", "Miami" ],
            "required_field": false
        }
    }


*[In this model, the process of checking the inputs will also check the paths designated in the components dictionary to make sure that values do not violate any of the additional attributes of the property declared in the components. Whenever they may conflict with the attributes declared in the schema example, the conditions in the components map supersedes. So, in this case, the requirement that an address contain a city key-value has been turned off. But if a city is provided, it must match one of the four city values provided. Likewise, any value provided in userID must be no more than nor less than 13 characters long and can only be composed of alphanumerical characters.]*

This module also validates the architecture of the model declarations themselves to facilitate the model design process and ensure that no models break the rules of the module. Error reports are provided to identity the scope of conditionals applicable to any given property in addition to the module documentation.

To declare the model::

    {
        "schema": {
            "property": "value"
        },
        "components": {},
        "title": "my cool data model",
        "description": "model for performance analytics records of my sweet app",
        "metadata": { "version": "1.1.1" },
        "url": "https://collectiveacuity.com/api/mycoolresource?jsonmodel=true",
        "max_size": 1024,
    }

*[all fields except schema are optional]*

To import the model::

    import json

    sampleModel = json.loads(open('sample-model.json').read())


To initialize the class object::

    from jsonmodel.validators import jsonModel

    validModel = jsonModel(sampleModel)


To validate input against model declaration::

    validModel.validate(input)


To validate input against an individual component::

    path_to_root = '.property'
    validModel.validate(input, path_to_root)


To handle invalid inputs::

    try:
        validModel.validate(invalid_input)
    except InputValidationError as err:
        assert err.error['error_code'] > 4000


Ingest Kwargs
-------------
This module also supports the ingestion of keyword arguments. The process of ingestion recursively walks the valid model searching for key-value pairs which match the keyword arguments of the input. For each match it finds, it constructs a key-value pair in the dictionary using the following rules (in order):

1. Value in kwargs if field passes all its component validation tests
2. Default value declared for the key in the model
3. Empty value appropriate to datatype of key in the model

As a result, ingestion will produce an output which contains all the keys declared in the model. If there is a **default value** declared for each key in the model, it is also guaranteed to return a dictionary that will pass a model validation test. Extra keyword arguments are ignored unless extra fields is *True* in the model declaration.

To ingest kwargs::

    output_dict = validModel.ingest(**kwargs)


Reference Documentation
-----------------------
For more details about how to use jsonModel, refer to the
`Reference Documentation on GitHub
<https://github.com/collectiveacuity/jsonModel/blob/master/REFERENCE.rst>`_