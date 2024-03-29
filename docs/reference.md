
# Reference Materials
*Documentation for model declaration and error handling for jsonModel validation*

## Schema Default Behavior
The default behavior of a schema declaration includes validation of structure, datatype and requirements. Any of these defaults can be turned off in the specification of a field in the components map. However, for many purposes, the defaults will suffice to declare model field validation, eliminating the need for further specification in a components map.

**Schema Example**::

    "schema": {
        "userID": "gY3Cv81QwL0Fs",
        "datetime": 1456000345.543713,
        "active": true,
        "emoticon": "aGFwcHk=",
        "rating": 8,
        "reference": null,
        "address": {
            "city": "New Orleans",
            "region": "LA",
            "postal_code": "",
            "country": "United States",
            "country_code": 0
        },
        "comments": [ "@GerardMaras Rock the shrimp bouillabaisse!" ]
    }

### Default Settings
- **Structure**: The validation process will assume that a dictionary (including the top-level dictionary) defines its maximum scope of key names and that lists can contain any number of items. Lists cannot contain mixed datatypes and the first item in a list defines the allowable properties of each item in the list. For this reason, all lists declared in the model must also contain an item. So, the example model expects to find only the userID, datetime, active, emoticon, rating, address and comments fields and it will accept any number of strings in the comments list.
- **Datatype**: The validation process will assume that the datatype of each value in the input matches the datatype in the model. So, the example model expects to see a string for userID, a number for datetime, a boolean for active, etc... Special datatypes like bytes, integers and sets which json does not directly support must be handled by qualifiers in the components map.
- **Requirements**: The validation process will assume a key with a non-empty value is a required input. Since lists must declare an item, all lists are assumed to be required fields in the model. So, all fields in the example are required except postal_code and country_code. The empty value for each datatype can be expressed with {}, 0, 0.0, false or "" and indicates that it is optional.

### Meta-Model Restrictions
A model validation error will occur if a key name in the schema contains an item designator pattern such as [2] or [35]. The module uses these patterns to validate inputs which contain lists of arbitrary size. As a result, there are limitations to the meta-model recursion of the module. It is not possible to use lists in model declarations which you wish to use as schemas in other model declarations.

## Components Map
The default validation process can be modified, and other (less common) conditional qualifier can be added through the components map of the model. Whereas the schema map provides a transparent data architecture that is self-valid, the components map can be used to specify the conditions of acceptable data for any number of fields in the schema. The component map is an optional flat dictionary where each key in the component map designates a particular path in the schema using the dot-path ('.' and [0]) nomenclature of nesting and array identification.

**Components Example**::

    "components": {
        ".": {
            "extra_fields": false,
            "min_size": 10,
            "max_size": 300
        },
        ".active": {
            "equal_to": false
        },
        ".userID": {
            "min_length": 13,
            "max_length": 13,
            "min_value": "1111111111111",
            "max_value": "yyyyyyyyyyyyy",
            "must_not_contain": [ "[^\\w]", "_" ],
            "field_description": "13 digit unique base 64 url safe key"
        },
        ".datetime": {
            "greater_than": 1.1,
            "less_than": 2000000000.0,
            "field_position": 1
        },
        ".emoticon": {
            "required_field": false,
            "byte_data": true,
            "example_values": [ "aGFwcHk=" ],
            "excluded_values": [ "c2Fk" ],
            "field_metadata": { "endpoint": "http://collectiveacuity.com/icons/" }
        },
        ".reference": {
            "required_field": false
        },
        ".rating": {
            "required_field": false,
            "min_value": 1,
            "max_value": 10,
            "default_value": 5,
            "excluded_values": [ 7, 9 ],
            "integer_data": true
        },
        ".address.city": {
            "discrete_values": [ "New Orleans", "New York", "Los Angeles", "Miami" ],
            "required_field": false,
            "default_value": "New York"
        },
        ".address.region":{
            "greater_than": "AB",
            "less_than": "Yyyyyyyyyyyyyyyyyyyyyyyy",
            "contains_either": [ "[A-Z]{2}", "[A-Z][a-z]+" ],
            "field_title": "State or Province"
        },
        ".address.country_code":{
            "discrete_values": [ 36, 124, 554, 826, 840 ],
            "integer_data": true
        },
        ".comments": {
            "required_field": false,
            "min_size": 1,
            "max_size": 3,
            "unique_values": true
        }
        ".comments[0]": {
            "max_length": 140,
            "must_contain": [ "[a-zA-Z]{2,}" ],
            "example_values": [ "couldn't find the place", "hidden gem!!!!" ]
        }
    }

### Path Definitions
To validate additional conditional qualifier placed on a field in the schema, the validation process looks through the schema for the value associated with a key or item specified in the key name of the components map. In this example, the key named ".userID" maps to the "userID" key to be found in the top level map of the schema, ".address.city" refers to the "city" key inside the "address" map inside the schema map and ".comments[0]" refers to the first item inside the comments list.  Since the comments list is itself made optional by the declaration "required_field": false in the ".comments" key, this component is only validated if there is an item to validate. Otherwise, it is ignored. "." is the key name for the top-level map itself and the "extra_fields" criterion changes the default to allow the top-level map to accept undeclared keys.  
__NOTE:__ The "." at the beginning of a dot-path is optional. So, a key named "userID" is the same as ".userID".

## List of Field Conditionals
<table>
<thead>
<tr><th>Criteria Key     </th><th>Criteria Value            </th><th>Error Code  </th><th>String  </th><th>Number  </th><th>Boolean  </th><th>Map  </th><th>List  </th><th>Status   </th><th>Description                                                                                                                                                             </th></tr>
</thead>
<tbody>
<tr><td>value_datatype   </td><td>String                    </td><td>n/a         </td><td>        </td><td>        </td><td>         </td><td>     </td><td>      </td><td>available</td><td>the datatype of a value or item defined in the schema                                                                                                                   </td></tr>
<tr><td>required_field   </td><td>Boolean                   </td><td>4002        </td><td>Y       </td><td>Y       </td><td>Y        </td><td>Y    </td><td>Y     </td><td>available</td><td>a true boolean requires this key-value in the input                                                                                                                     </td></tr>
<tr><td>extra_fields     </td><td>Boolean                   </td><td>4003        </td><td>        </td><td>        </td><td>         </td><td>Y    </td><td>      </td><td>available</td><td>a true boolean allows map to contain undeclared keys                                                                                                                    </td></tr>
<tr><td>key_datatype     </td><td>String                    </td><td>n/a         </td><td>        </td><td>        </td><td>         </td><td>     </td><td>      </td><td>available</td><td>the datatype of a key name must be a string                                                                                                                             </td></tr>
<tr><td>maximum_scope    </td><td>List                      </td><td>n/a         </td><td>        </td><td>        </td><td>         </td><td>     </td><td>      </td><td>available</td><td>the maximum extent of keys allowed in a dictionary generated by extra_fields default                                                                                    </td></tr>
<tr><td>declared_value   </td><td>Any                       </td><td>n/a         </td><td>        </td><td>        </td><td>         </td><td>     </td><td>      </td><td>available</td><td>the value or item defined in the schema [strings                                                                                                                        </td></tr>
<tr><td>default_value    </td><td>Any                       </td><td>n/a         </td><td>Y       </td><td>Y       </td><td>Y        </td><td>     </td><td>Y     </td><td>available</td><td>a value for an optional field when field is missing in input                                                                                                            </td></tr>
<tr><td>byte_data        </td><td>Boolean                   </td><td>4011        </td><td>Y       </td><td>        </td><td>         </td><td>     </td><td>      </td><td>available</td><td>a true boolean expects to see base64 byte data in the string field                                                                                                      </td></tr>
<tr><td>min_length       </td><td>Integer                   </td><td>4012        </td><td>Y       </td><td>        </td><td>         </td><td>     </td><td>      </td><td>available</td><td>the minimum number of characters in a string                                                                                                                            </td></tr>
<tr><td>max_length       </td><td>Integer                   </td><td>4013        </td><td>Y       </td><td>        </td><td>         </td><td>     </td><td>      </td><td>available</td><td>the maximum number of characters in a string                                                                                                                            </td></tr>
<tr><td>must_not_contain </td><td>List of Strings           </td><td>4014        </td><td>Y       </td><td>        </td><td>         </td><td>     </td><td>      </td><td>available</td><td>a list of regular expressions which should not be found in a string                                                                                                     </td></tr>
<tr><td>must_contain     </td><td>List of Strings           </td><td>4015        </td><td>Y       </td><td>        </td><td>         </td><td>     </td><td>      </td><td>available</td><td>a list of regular expressions which must be found in a string                                                                                                           </td></tr>
<tr><td>contains_either  </td><td>List of Strings           </td><td>4016        </td><td>Y       </td><td>        </td><td>         </td><td>     </td><td>      </td><td>available</td><td>a list of regular expressions which string must match at least one                                                                                                      </td></tr>
<tr><td>integer_data     </td><td>Boolean                   </td><td>4021        </td><td>        </td><td>Y       </td><td>         </td><td>     </td><td>      </td><td>available</td><td>a true boolean requires number to be an integer                                                                                                                         </td></tr>
<tr><td>min_value        </td><td>Number or String          </td><td>4022        </td><td>Y       </td><td>Y       </td><td>         </td><td>     </td><td>      </td><td>available</td><td>the minimum value of a number or string                                                                                                                                 </td></tr>
<tr><td>max_value        </td><td>Number or String          </td><td>4023        </td><td>Y       </td><td>Y       </td><td>         </td><td>     </td><td>      </td><td>available</td><td>the maximum value of a number or string                                                                                                                                 </td></tr>
<tr><td>greater_than     </td><td>Number or String          </td><td>4024        </td><td>Y       </td><td>Y       </td><td>         </td><td>     </td><td>      </td><td>available</td><td>the value a number or string must be greater than                                                                                                                       </td></tr>
<tr><td>less_than        </td><td>Number or String          </td><td>4025        </td><td>Y       </td><td>Y       </td><td>         </td><td>     </td><td>      </td><td>available</td><td>the value a number or string must be less than                                                                                                                          </td></tr>
<tr><td>equal_to         </td><td>Boolean, Number or String </td><td>4026        </td><td>Y       </td><td>Y       </td><td>Y        </td><td>     </td><td>      </td><td>available</td><td>the value a number, string or boolean must equal                                                                                                                        </td></tr>
<tr><td>min_size         </td><td>Integer                   </td><td>4031        </td><td>        </td><td>        </td><td>         </td><td>Y    </td><td>Y     </td><td>available</td><td>the minimum size of a map converted to json data or the minimum number of items in a list                                                                               </td></tr>
<tr><td>max_size         </td><td>Integer                   </td><td>4032        </td><td>        </td><td>        </td><td>         </td><td>Y    </td><td>Y     </td><td>available</td><td>the maximum size of a map converted to json data or the maximum number of items in a list                                                                               </td></tr>
<tr><td>unique_values    </td><td>Boolean                   </td><td>4033        </td><td>        </td><td>        </td><td>         </td><td>     </td><td>Y     </td><td>available</td><td>a true boolean treats a list as a set of unique primitives with no duplication                                                                                          </td></tr>
<tr><td>discrete_values  </td><td>List of Strings or Numbers</td><td>4041        </td><td>Y       </td><td>Y       </td><td>         </td><td>     </td><td>      </td><td>available</td><td>a list of values allowed                                                                                                                                                </td></tr>
<tr><td>identical_to     </td><td>String                    </td><td>            </td><td>Y       </td><td>Y       </td><td>Y        </td><td>Y    </td><td>Y     </td><td>         </td><td>the key name in the components map whose value the value of this component must match                                                                                   </td></tr>
<tr><td>lambda_function  </td><td>String                    </td><td>            </td><td>Y       </td><td>Y       </td><td>Y        </td><td>Y    </td><td>Y     </td><td>         </td><td>a single argument function which should be run to validate the value of this component / lambda_function must return true (valid) or false (invalid)                    </td></tr>
<tr><td>validation_url   </td><td>String                    </td><td>            </td><td>Y       </td><td>Y       </td><td>Y        </td><td>Y    </td><td>Y     </td><td>         </td><td>an uri which can be called to validate the value of this component with its input in the body of the request /  uri response must return true (valid) or false (invalid)</td></tr>
<tr><td>valid_path       </td><td>Boolean                   </td><td>            </td><td>Y       </td><td>        </td><td>         </td><td>     </td><td>      </td><td>         </td><td>a true value will check localhost to determine if file path is valid                                                                                                    </td></tr>
<tr><td>example_values   </td><td>List of Strings or Numbers</td><td>            </td><td>Y       </td><td>Y       </td><td>         </td><td>     </td><td>      </td><td>available</td><td>a list of values which satisfy all the validation requirements                                                                                                          </td></tr>
<tr><td>field_title      </td><td>String                    </td><td>n/a         </td><td>Y       </td><td>Y       </td><td>Y        </td><td>Y    </td><td>Y     </td><td>available</td><td>the title of the component for documentation and error reporting                                                                                                        </td></tr>
<tr><td>field_description</td><td>String                    </td><td>n/a         </td><td>Y       </td><td>Y       </td><td>Y        </td><td>Y    </td><td>Y     </td><td>available</td><td>a description of the component for documentation and error reporting                                                                                                    </td></tr>
<tr><td>field_position   </td><td>Integer                   </td><td>n/a         </td><td>Y       </td><td>Y       </td><td>Y        </td><td>Y    </td><td>Y     </td><td>available</td><td>the position of the component in an ordered array of fields                                                                                                             </td></tr>
<tr><td>field_metadata   </td><td>Map                       </td><td>n/a         </td><td>Y       </td><td>Y       </td><td>Y        </td><td>Y    </td><td>Y     </td><td>available</td><td>a dictionary for metadata about the component that passes through validation check                                                                                      </td></tr>
</tbody>
</table>

## Error Handling
Errors created from improper model specification will raise a ModelValidationError with a message that is designed to help determine the source of the model declaration error. To ensure that model initialization occurs properly, no error encoding is included to handle these exceptions. However, it is expected that validation of inputs will produce errors. Otherwise, what's the point?! So, in addition to a text report, a dictionary has been included with the InputValidationError exception to facilitate error handling.

**Error Method Example**::

    self.error = {
        'model_schema': {
            'datetime': 1456190345.543713,
            'address': {
                'country_code': 0,
                'city': 'New Orleans',
                'postal_code': '',
                'region': 'LA',
                'country': 'United States'
            },
            'comments': [ '@GerardMaras Rock the shrimp bouillabaisse!' ],
            'active': True,
            'rating': 8,
            'reference': None,
            'userID': 'gY3Cv81QwL0Fs',
            'emoticon': 'aGFwcHk=',
        },
        'input_path': '.',
        'input_criteria': {
            'required_field': True,
            'value_datatype': 'map',
            'min_size': 10,
            'max_size': 300,
            'maximum_scope': [ 'datetime', 'address', 'active', 'userID', 'comments', 'rating', 'emoticon' ],
            'extra_fields': False
        },
        'failed_test': 'extra_fields',
        'error_value': 'extraKey',
        'error_code': 4003
    }

### Order of Exceptions
The validation process will raise an error as soon as it encounters one, so there is no guarantee that the error that is reported is the only error in the input. Since there is no set order to the keys in a dictionary, there is also no guaranteed a priori order to the evaluation process. However below is an overview of the order of the steps of the validation process:

Structure:
__________
1. Input is a dictionary
2. Required keys in the input
3. Extra keys in the input
4. Value of each key in the input (recursive) *(see below)*
5. Inject default values for missing optional keys

Values (or Items):
__________________
1. Datatype of value
2. Other value qualifiers based upon datatype
3. Identity, Lambda and URL qualifiers # **TODO**

To help the process of error handling and client-server negotiation, both the schema for the model as well as the the map of conditional qualifiers for the field that raised the error are included in the error dictionary.

## Ingesting Kwargs
The process of ingestion recursively walks the valid model searching for key-value pairs which match the keyword arguments of the input. For each match it finds, it constructs a key-value pair in the dictionary using the following rules (in order):

1. Value in kwargs if field passes all its component validation tests
2. Default value declared for the key in the model
3. Empty value appropriate to datatype of key in the model

Like the core validation method, ingestion will also walk through each item in a list field of the kwargs if the item type itself is also a list or dictionary. However, because invalid data will be replaced by empty values appropriate to the datatype declared in the model, unlike the core validation model, output data from ingest may not be model valid data. If it is desirable to ensure that the data is valid, a 'default_value' should be declared for each key in the components section of the data model and the 'min_size' of each list declaration should only be set to 0.

**Sample Kwargs**::

    {
        "userID": "6nPbM9gTwLz3f",
        "datetime": 1449179763.312077,
        "active": false,
        "emoticon": "aGFwcHIk=",
        "comments": [ "gold", "silver", "bronze", "pewter" ],
        "address": {
            "region": "NY",
            "country": "United States"
      }
    }


**Ingest Sample**::

    output = jsonModel.ingest(**sample_kwargs)


**Sample Output**::

    {
        'userID': '6nPbM9gTwLz3f',
        'datetime': 1449179763.312077,
        'active': False,
        'rating': 5,
        'reference': None,
        'emoticon': 'aGFwcHIk='
        'comments': ['gold', 'silver', 'bronze'],
        'address': {
            'postal_code': '',
            'city': 'New York',
            'country_code': 0,
            'region': 'NY',
            'country': 'United States'
        }
    }


**Ingest Empty**::

    output = jsonModel.ingest(**{})


**Empty Output**::

    {
        'userID': '',
        'datetime': 0.0,
        'active': False,
        'rating': 5,
        'reference': None,
        'emoticon': ''
        'comments': [],
        'address': {
            'postal_code': '',
            'city': 'New York',
            'country_code': 0,
            'region': '',
            'country': ''
        }
    }

### Extra Keywords
If 'extra_fields' is declared True in the components for a dictionary in the model, then any extraneous keys in the corresponding dictionary in the kwargs will be added to the output.

### Too Many Items
Items are only added to a list from those items in kwargs if they are valid. If the number of valid items in a list in the kwargs exceeds the 'max_size' of the corresponding list in the model, then subsequent items are not added to the list once the list reaches its maximum size.

## Query Criteria
Query criteria are composed of a dictionary of one or more key-value pairs, where the key names are the dot path to the fields in the model schema to be queried and the values are dictionaries containing any of the conditional operators for the query on the respective fields. Like component declarations, the "." at the beginning of the dot path for a key name is optional. For fields with number, string or boolean datatypes, { "field": { "equal_to": "value" } } can be shortened to { "field": "value" } and the class will automatically interpret the syntax as the "equal_to" criteria. Query criteria can be simple, such as the single field, operator and qualifier in the example in [Home](index.md), or elaborate, such as found in the provided model sample-query.json below:

**Sample Query**::

    {
      ".active": {
        "value_exists": true,
        "equal_to": false
      },
      ".address": {
        "max_size": 100
      },
      ".address.country": "United States",
      ".address.city": {
        "discrete_values": [ "New Orleans", "New York", "Los Angeles", "Miami"]
      },
      ".address.country_code": {
        "discrete_values": [36, 124, 554, 826, 840],
        "integer_data": true
      },
      ".address.region": {
        "contains_either": ["[A-Z]{2}", "[A-Z][a-z]+"],
        "greater_than": "AB",
        "less_than": "Yyyyyyyyyyyyyyyyyyyyyyyy"
      },
      ".comments": {
        "max_size": 3,
        "min_size": 1,
        "unique_values": true
      },
      ".comments[0]": {
        "max_length": 140,
        "must_contain": ["[a-zA-Z]{2,}"]
      },
      ".datetime": {
        "greater_than": 1.1,
        "less_than": 2000000000.0
      },
      ".emoticon": {
        "byte_data": true,
        "excluded_values": ["c2Fk"]
      },
      ".rating": {
        "excluded_values": [7, 9],
        "max_value": 10,
        "min_value": 1
      },
      ".userID": {
        "max_length": 13,
        "max_value": "yyyyyyyyyyyyy",
        "min_length": 13,
        "min_value": "1111111111111",
        "must_not_contain": ["[^\\w]", "_"]
      }
    }

The query method follows a similar process by which input is validated. A record whose field values evaluate to true for all criteria returns true. Otherwise, something in the record does not match one or more query criteria and the query method returns false. Because the query method returns a false as soon as it encounters a failed criteria from a dictionary of fields in the query criteria, query time will vary based upon the number of records, how many fail and how many fields are added to the query criteria.

### Querying Items
Although the query method will evaluate items nested inside lists to an arbitrary depth, it does so by evaluating all items in the list and all sub-branches of any nested lists inside the list. As a result, querying items inside lists suffers non-linear explosion. And, unlike the process of item ingestion, if any item in a list (or branch of a sub-list) evaluates to true to the criteria provided the entire list will evaluate to true. **Be Warned**

### Query Errors
If query criteria contain fields, operators or qualifiers which are outside the scope of the model, the query method will produce a QueryValidationError.

To handle a QueryValidationError::

    try:
        query_results = validModel.query(invalid_criteria, test_record)
    except QueryValidationError as err:
        assert isinstance(err.error['message'], str)


### Query Rules Customization
When the model is initialized, it accepts an optional dictionary for customized query rules. The primary purpose of this customization is to limit query criteria validation to only those query operations which are supported by a specific query engine. Optional query rules must be structured according to the components field of the model-rules.json file and cannot contain any fields, operators or qualifiers outside the full range of the model query rules.

**Query Rules**::

    {
      ".boolean_fields": {
        "identical_to": ".similar_boolean",
        "lambda_function": "",
        "validation_url": "",
        "value_exists": false,
        "equal_to": false
      },
     ".list_fields": {
        "identical_to": ".similar_list",
        "lambda_function": "",
        "max_size": 0,
        "min_size": 0,
        "unique_values": false,
        "validation_url": "",
        "value_exists": false
     },
     ".map_fields": {
        "identical_to": ".similar_map",
        "lambda_function": "",
        "max_size": 0,
        "min_size": 0,
        "validation_url": "",
        "value_exists": false
     },
     ".null_fields": {
        "identical_to": ".similar_null",
        "lambda_function": "",
        "validation_url": "",
        "value_exists": false
     },
     ".number_fields": {
        "discrete_values": [],
        "excluded_values": [],
        "greater_than": 0.0,
        "identical_to": ".similar_number",
        "integer_data": false,
        "lambda_function": "",
        "less_than": 0.0,
        "max_value": 0.0,
        "min_value": 0.0,
        "validation_url": "",
        "value_exists": false,
        "equal_to": 0.0
     },
      ".string_fields": {
        "byte_data": false,
        "contains_either": [],
        "discrete_values": [],
        "excluded_values": [],
        "greater_than": "",
        "identical_to": ".similar_string",
        "lambda_function": "",
        "less_than": "",
        "max_length": 0,
        "max_value": "",
        "min_length": 0,
        "min_value": "",
        "must_contain": [],
        "must_not_contain": [],
        "validation_url": "",
        "value_exists": false,
        "equal_to": ""
      }
    }

*[The lambda_function, identical_to and validation_url operators are not yet supported by the model.]*

A malformed query rules argument on model initialization will produce a ModelValidationError.





