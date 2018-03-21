# jsonModel Class

The jsonModel class is the main class of the module. A jsonModel object must be initialized with a json-valid dictionary with the schema you wish to valid. When the object is initialized, it validates the architecture of the model declaration itself to facilitate the model design process and ensure that no models break the rules of the module. Once a valid model is constructed, input can then be fed to the class method 'validate' to determine whether the input is valid. Error reports are provided to identify the scope of conditionals applicable to any given property in addition to the module documentation.

## Declare Schema
Save in sample-schema.json::

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

## Import Schema
To import the schema::

    import json

    sample_schema = json.loads(open('sample-schema.json').read())


## Initialize Model
To initialize the class object::

    from jsonmodel.validators import jsonModel

    valid_model = jsonModel(sample_schema)

## Validate Input
To validate input against model declaration::

    valid_model.validate(input)


To validate input against an individual component::

    path_to_root = '.property'
    valid_model.validate(input, path_to_root)

## Handle Errors
To handle invalid inputs::

    try:
        valid_model.validate(invalid_input)
    except InputValidationError as err:
        assert err.error['error_code'] > 4000
     
To customize error message:

    input_title = 'Property field in input'
    valid_model.validate(input, path_to_root, input_title)

    
Ingest Kwargs
-------------
This module also supports the ingestion of keyword arguments. The process of ingestion recursively walks the valid model searching for key-value pairs which match the keyword arguments of the input. For each match it finds, it constructs a key-value pair in the dictionary using the following rules (in order):

1. Value in kwargs if field passes all its component validation tests
2. Default value declared for the key in the model
3. Empty value appropriate to datatype of key in the model

As a result, ingestion will produce an output which contains all the keys declared in the model. If there is a **default value** declared for each key in the model, it is also guaranteed to return a dictionary that will pass a model validation test. Extra keyword arguments are ignored unless extra fields is *True* in the model declaration.

To ingest kwargs::

    output_dict = valid_model.ingest(**kwargs)
    
To produce a default record:

    default_dict = valid_model.ingest()


Query Records
-------------
The jsonModel class also supports record querying on model validated data. When the model is initialized, it constructs a set of operators that can be used to query records which contain data validated by the model. The set of valid operators and qualifiers which can be used to query records on each field depend upon its datatype. The query criteria for each field is the subset of the criteria that can be declared for that field in the components section of the model which can evaluate to 'true' against a value stored for that field in a record.

The built in query method supports any number of fields declared in the model as well as the maximum subset of query relevant criteria for each field based upon its datatype. But the model can also be initialized with a customized dictionary of rules for field datatypes based upon what is supported by a specific query engine.  In this way, the query method can be used as a bridge across multiple different database query languages (with a jsonModel valid record access object customized for applicable databases) or as a post-request filter for records stored in a way that does not support robust query criteria.

To declare query rules::

    {
        ".string_fields": {
            "must_contain": []
        }
    }

To initialize model with custom query rules::

    query_rules = json.loads(open('query-rules.json').read())

    valid_model = jsonModel(sample_model, query_rules)


To declare query criteria::

    {
        'dot.path[2].field': {
            'must_contain': [ 'v.+' ]
        }
    }

To validate query criteria::

    valid_model.query(sample_query)


To evaluate a record using the criteria::

    valid_input = valid_model.validate(input)

    eval_outcome = valid_model.query(sample_query, valid_input)
    assert isinstance(eval_outcome, bool)


