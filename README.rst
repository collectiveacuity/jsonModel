.. image:: https://img.shields.io/pypi/v/jsonmodel.svg
    :target: https://pypi.python.org/pypi/jsonmodel
.. image:: https://img.shields.io/pypi/l/jsonmodel.svg
    :target: https://pypi.python.org/pypi/jsonmodel

=========
jsonModel
=========
*A Collection of Methods for Validating JSON Structured Data*

:Downloads: http://pypi.python.org/pypi/jsonModel
:Source: https://github.com/collectiveacuity/jsonModel
:Documentation: https://collectiveacuity.github.io/jsonModel/

============
Introduction
============
Json Model is designed to facilitate the process of implementing data validation against a declared json data model. The jsonModel class offers a more intuitive declaration process than other schema enforcement modules currently available by relying upon the architecture of json itself to validate datatypes, requirements and defaults.

============
Installation
============
From PyPi::

    $ pip install jsonmodel

From GitHub::

    $ git clone https://github.com/collectiveacuity/jsonmodel
    $ cd jsonmodel
    $ python setup.py install


Getting Started
---------------
This module uses self-valid schema declarations as a method to describe data requirements. As a result, for many data models, full validation can be achieved from an example declaration using the schema key::


    {
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
    }

*[In this model, the input must contain values for all four top level keys and each value must correspond to the datatype in the model. So, the input must have a userID field with a string, a datetime field with a number, an active key with a boolean and the address field must be a dictionary which itself contains city, region and country values. Since it is empty, postal_code is optional. If a value is provided for postal_code however, it must be a string.]*

In addition to intuitive self-valid schema declarations, jsonModel also offers a rich way to further refine the conditionality of any property in the model through an accompanying components map whose key names correspond to the path to the schema property which requires additional validation::

    {
      "schema": { ... },
      "components": {
        "userID": {
          "min_length": 13,
          "max_length": 13,
          "must_not_contain": [ "[^\\w]", "_" ]
        },
        "address.city": {
          "discrete_values": [ "New Orleans", "New York", "Los Angeles", "Miami" ],
          "required_field": false
        }
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

To import the schema::

    import json

    sample_schema = json.loads(open('sample-schema.json').read())


To initialize the class object::

    from jsonmodel.validators import jsonModel

    valid_model = jsonModel(sample_schema)


To validate input against model declaration::

    valid_model.validate(input)


To validate input against an individual component::

    path_to_root = 'dot.path[2].field'
    valid_model.validate(input, path_to_root)


To handle invalid inputs::

    try:
        valid_model.validate(invalid_input)
    except InputValidationError as err:
        assert err.error['error_code'] > 4000


To generate a colloquial explanation of error::

    try:
        valid_model.validate(invalid_input)
    except InputValidationError as err:
         print(err.explain())
         
To customize error message::

    input_title = 'Property field in input'
    valid_model.validate(input, path_to_root, input_title)


To filter valid input based upon query criteria::

    query_criteria = { 'dot.path[2].field': 'exact value' }
    assert valid_model.query(query_criteria, valid_input)
    
    query_criteria = { 'dot.path[2].field': { 'excluded_values': [ 'exact value' ] } }
    assert not valid_model.query(query_criteria, valid_input)


To produce html documentation of model criteria::

    from jsonmodel.extensions import tabulate
    tabulate(valid_model)
    html_table = valid_model.tabulate()


Further Reading
---------------
For more details about how to use jsonModel, refer to the
`Reference Documentation on GitHub
<https://collectiveacuity.github.io/jsonModel>`_
