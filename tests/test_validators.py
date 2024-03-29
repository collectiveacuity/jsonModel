__author__ = 'rcj1492'
__created__ = '2016.01'

try:
    import pytest
except:
    import sys
    print('test_validators requires the pytest module. try: pip3 install pytest')
    sys.exit()

import json
from copy import deepcopy
from jsonmodel.exceptions import InputValidationError, ModelValidationError
from jsonmodel.exceptions import QueryValidationError
from jsonmodel.validators import jsonModel

class jsonModelTests(jsonModel):

    def __init__(self, data_model):
        jsonModel.__init__(self, data_model)

    def unitTests(self, valid_input, valid_query, valid_rules):

        # print(self.keyMap)

    # test model fields
        assert isinstance(self.title, str)
        assert isinstance(self.description, str)
        assert isinstance(self.url, str)
        assert isinstance(self.metadata, dict)
        # assert isinstance(self.maxSize, int)

    # test declarative fields in model keyMap
        assert self.keyMap['.']['value_datatype']
        assert self.keyMap['.']['min_size']
        assert self.keyMap['.']['max_size']
        assert self.keyMap['.userID']['required_field']
        assert self.keyMap['.address.region']['declared_value']
        assert self.keyMap['.rating']['default_value']
        assert self.keyMap['.emoticon']['byte_data']
        assert self.keyMap['.reference']['value_datatype']
        assert self.keyMap['.rating']['integer_data']
        assert self.keyMap['.userID']['min_length']
        assert self.keyMap['.comments[0]']['max_length']
        assert self.keyMap['.rating']['min_value']
        assert self.keyMap['.rating']['max_value']
        assert self.keyMap['.comments']['min_size']
        assert self.keyMap['.comments']['max_size']
        assert self.keyMap['.comments']['unique_values']
        assert self.keyMap['.comments']['declared_value']
        assert self.keyMap['.userID']['must_not_contain']
        assert self.keyMap['.comments[0]']['must_contain']
        assert self.keyMap['.address.region']['contains_either']
        assert self.keyMap['.address.country']['must_contain'].keys()
        assert self.keyMap['.address.country_code']['discrete_values']
        assert self.keyMap['.emoticon']['example_values']
        assert self.keyMap['.address.region']['field_title']
        assert self.keyMap['.datetime']['field_position']
        assert self.keyMap['.userID']['field_description']
        assert self.keyMap['.emoticon']['field_metadata']

        # TODO: "identical_to": ".similar_string",
        # TODO: "lambda_function": "",
        # TODO: "validation_url": "",

    # test declared values for empty values
        assert isinstance(self.keyMap['.address.country_code']['declared_value'], int)
        assert isinstance(self.keyMap['.address.postal_code']['declared_value'], str)

    # test integers in key name exception
        try:
            test_schema = { 'schema': { 0: 'value' } }
            jsonModel(test_schema)
        except ModelValidationError as err:
            assert str(err).find('Model declaration is invalid')

    # test validation with empty path to root
        v_input = deepcopy(valid_input)
        assert self.validate(v_input)

    # test validation with dot-path to root
        v_input = deepcopy(valid_input)
        assert self.validate(v_input, '.')

    # test individual component validation
        v_input = deepcopy(valid_input)
        assert self.validate(v_input['datetime'], '.datetime') == v_input['datetime']
        v_input = deepcopy(valid_input)
        assert self.validate(v_input['userID'], '.userID') == v_input['userID']
        v_input = deepcopy(valid_input)
        assert not self.validate(v_input['active'], '.active')
        v_input = deepcopy(valid_input)
        assert self.validate(v_input['comments'], '.comments') == v_input['comments']
        v_input = deepcopy(valid_input)
        assert self.validate(v_input['address'], '.address') == v_input['address']

    # test non-existent path to root exception
        v_input = deepcopy(valid_input)
        try:
            self.validate(v_input, '.not_a_path')
        except ModelValidationError as err:
            assert str(err).find('Model declaration is invalid')

    # test path to root not a string
        v_input = deepcopy(valid_input)
        try:
            self.validate(v_input, [ '.datetime' ])
        except ModelValidationError as err:
            assert str(err).find('Model declaration is invalid')

    # test invalid input type
        invalid_list = []
        try:
            self.validate(invalid_list)
        except InputValidationError as err:
            assert err.error['model_schema']
            assert err.error['failed_test'] == 'value_datatype'
            assert err.explain().find('map') > -1

    # test object title in error message
        try:
            self.validate(invalid_list, object_title='List input')
        except InputValidationError as err:
            assert err.error['object_title']
            assert str(err).find('input is invalid.')
            assert str(err).find('Value []')

    # test non-json valid object exception
        invalid_object = jsonModel({'schema':{'test':'object'}})
        try:
            self.validate(invalid_object, object_title='jsonModel input')
        except InputValidationError as err:
            assert str(err).find('Value jsonModel')

    # test json structure of error message
        try:
            self.validate(invalid_list)
        except InputValidationError as err:
            assert json.dumps(err.error)
        try:
            self.validate(invalid_object)
        except InputValidationError as err:
            assert json.dumps(err.error)

    # test invalid input data type
        try:
            self.validate('1449179763.312077', '.datetime')
        except InputValidationError as err:
            assert err.error['failed_test'] == 'value_datatype'
            assert json.dumps(err.error)
            assert err.explain().find('number') > -1

    # test non-json valid input datatype
        try:
            self.validate(invalid_object, '.comments[0]')
        except InputValidationError as err:
            assert err.error['failed_test'] == 'value_datatype'
            assert json.dumps(err.error)
            assert err.explain().find('string') > -1

    # test key_datatype exception
        integer_keyname_error = deepcopy(valid_input)
        integer_keyname_error[2] = 'integer key name'
        try:
            self.validate(integer_keyname_error)
        except InputValidationError as err:
            assert err.error['error_value'] == 2
            assert err.explain().find('key') > -1
            
    # test extra_fields exception
        extra_key_input = deepcopy(valid_input)
        extra_key_input['address']['extraKey'] = 'string'
        try:
            self.validate(extra_key_input)
        except InputValidationError as err:
            assert not err.error['object_title']
            assert err.error['failed_test'] == 'extra_fields'
            assert '.address.extraKey' in err.error['error_value']
            assert '.address.city' in err.error['input_criteria']['maximum_scope']
            assert err.explain().find('sub-field') > -1
        del extra_key_input['address']['extraKey']

    # test required_field exception
        missing_key_input = deepcopy(valid_input)
        del missing_key_input['active']
        try:
            self.validate(missing_key_input, object_title='Required field exception')
        except InputValidationError as err:
            assert err.error['failed_test'] == 'required_field'
            assert err.error['object_title']
            assert err.explain().find('required field') > -1

    # test required_field false in dictionaries
        optional_key = deepcopy(valid_input)
        del optional_key['comments']
        assert not 'comments' in self.validate(optional_key).keys()

    # test null value declaration
        null_value = deepcopy(valid_input)
        null_value['reference'] = 1
        self.validate(null_value)

    # test null value declaration of invalid json data exception
        null_error = deepcopy(valid_input)
        null_error['reference'] = invalid_object
        count = 1
        try:
            self.validate(null_error)
            count = 0
        except InputValidationError as err:
            assert err.error['failed_test'] == 'value_datatype'
            assert err.explain().find('be null') > -1
        assert count

    # test default_value insertion
        default_rating = deepcopy(valid_input)
        new_default_rating = self.validate(default_rating)
        assert new_default_rating['rating'] == 5

    # test default_value ingestion
        default_rating_ingest = deepcopy(valid_input)
        new_default_rating = self.ingest(**default_rating_ingest)
        assert new_default_rating['rating'] == 5

    # test map max_size exception
        from base64 import b64encode
        z = 'too many things to emote in order to put into one line without extending well beyond the max size'
        big_map = deepcopy(valid_input)
        big_map['emoticon'] = b64encode(z.encode('utf-8')).decode()
        try:
            self.validate(big_map)
        except InputValidationError as err:
            assert err.error['failed_test'] == 'max_size'
            assert err.explain().find('converted to a string') > -1

    # test list min_size exception
        short_list = deepcopy(valid_input)
        short_list['comments'] = []
        try:
            self.validate(short_list)
        except InputValidationError as err:
            assert err.error['failed_test'] == 'min_size'
            assert not err.error['object_title']
            assert err.explain().find('empty') > -1

    # test list max_size exception
        long_list = deepcopy(valid_input)
        long_list['comments'].append('pewter')
        try:
            self.validate(long_list, object_title='Max size exception')
        except InputValidationError as err:
            assert err.error['failed_test'] == 'max_size'
            assert err.error['object_title']
            assert err.explain().find('items') > -1

    # test value_datatype exception
        mixed_list = deepcopy(valid_input)
        mixed_list['comments'][1] = 100
        try:
            self.validate(mixed_list)
        except InputValidationError as err:
            assert err.error['failed_test'] == 'value_datatype'
            assert err.explain().find('string') > -1

    # test unique_values exception
        duplicate_list = deepcopy(valid_input)
        duplicate_list['comments'][2] = 'gold'
        try:
            self.validate(duplicate_list)
        except InputValidationError as err:
            assert err.error['failed_test'] == 'unique_values'
            assert err.explain().find('unique values') > -1
            
    # test integer_data exception
        integers_only = deepcopy(valid_input)
        integers_only['rating'] = 3.5
        try:
            self.validate(integers_only, object_title='Integer data exception')
        except InputValidationError as err:
            assert err.error['failed_test'] == 'integer_data'
            assert err.error['object_title']
            assert err.explain().find('an integer') > -1
            
    # test min_value exception
        min_number = deepcopy(valid_input)
        min_number['rating'] = 0
        try:
            self.validate(min_number)
        except InputValidationError as err:
            assert err.error['failed_test'] == 'min_value'
            assert not err.error['object_title']
            assert err.explain().find('no less than') > -1

    # test max_value exception
        max_number = deepcopy(valid_input)
        max_number['rating'] = 11
        try:
            self.validate(max_number)
        except InputValidationError as err:
            assert err.error['failed_test'] == 'max_value'
            assert err.explain().find('no greater than') > -1
            
    # test greater_than exception for numbers
        greater_number = deepcopy(valid_input)
        greater_number['datetime'] = 0.1
        try:
            self.validate(greater_number)
        except InputValidationError as err:
            assert err.error['failed_test'] == 'greater_than'
            assert err.explain().find('greater than') > -1

    # test less_than exception for numbers
        less_number = deepcopy(valid_input)
        less_number['datetime'] = 2000000000.1
        try:
            self.validate(less_number)
        except InputValidationError as err:
            assert err.error['failed_test'] == 'less_than'
            assert err.explain().find('less than') > -1
    
    # test equal_to exception for booleans
        equal_boolean = deepcopy(valid_input)
        equal_boolean['active'] = True
        try:
            self.validate(equal_boolean)
        except InputValidationError as err:
            assert err.error['failed_test'] == 'equal_to'
            assert err.explain().find('equal false')
            
    # test min_value for strings exception
        low_string = deepcopy(valid_input)
        low_string['userID'] = '0000000000000'
        try:
            self.validate(low_string)
        except InputValidationError as err:
            assert err.error['failed_test'] == 'min_value'
            assert err.explain().find('alphanumeric order') > -1
            
    # test max_value for strings exception
        high_string = deepcopy(valid_input)
        high_string['userID'] = 'zzzzzzzzzzzzz'
        try:
            self.validate(high_string)
        except InputValidationError as err:
            assert err.error['failed_test'] == 'max_value'
            assert err.explain().find('not fall after') > -1

    # test greater_than exception for strings
        greater_string = deepcopy(valid_input)
        greater_string['address']['region'] = 'AA'
        try:
            self.validate(greater_string, object_title='Greater than exception')
        except InputValidationError as err:
            assert err.error['failed_test'] == 'greater_than'
            assert err.error['object_title']
            assert err.explain().find('fall after') > -1
            
    # test less_than exception for strings
        less_string = deepcopy(valid_input)
        less_string['address']['region'] = 'Zzzzzzzzzzzzzzzzzzzzzzzz'
        try:
            self.validate(less_string)
        except InputValidationError as err:
            assert err.error['failed_test'] == 'less_than'
            assert not err.error['object_title']
            assert err.explain().find('come before') > -1

    # test excluded_values for strings exception
        excluded_string = deepcopy(valid_input)
        excluded_string['emoticon'] = 'c2Fk'
        try:
            self.validate(excluded_string)
        except InputValidationError as err:
            assert err.error['failed_test'] == 'excluded_values'
            assert err.explain().find('cannot be') > -1

    # test excluded_values for strings exception
        excluded_number = deepcopy(valid_input)
        excluded_number['rating'] = 7
        try:
            self.validate(excluded_number)
        except InputValidationError as err:
            assert err.error['failed_test'] == 'excluded_values'
            assert err.explain().find('be neither') > -1
            
    # test discrete_values exception
        discrete_string = deepcopy(valid_input)
        discrete_string['address']['city'] = 'Boston'
        try:
            self.validate(discrete_string)
        except InputValidationError as err:
            assert err.error['failed_test'] == 'discrete_values'
            assert err.explain().find('be either') > -1

    # test discrete_values exception
        discrete_number = deepcopy(valid_input)
        discrete_number['address']['country_code'] = 20
        try:
            self.validate(discrete_number)
        except InputValidationError as err:
            assert err.error['failed_test'] == 'discrete_values'
            assert err.explain().find('be either') > -1
            
    # test byte_data exception
        byte_string = deepcopy(valid_input)
        byte_string['emoticon'] = 'happy'
        try:
            self.validate(byte_string)
        except InputValidationError as err:
            assert err.error['failed_test'] == 'byte_data'
            assert err.explain().find('byte data encoded') > -1

    # test max_length exception
        max_string = deepcopy(valid_input)
        max_string['userID'] = 'LongAlphaNumericID'
        try:
            self.validate(max_string)
        except InputValidationError as err:
            assert err.error['failed_test'] == 'max_length'
            assert err.explain().find('not be longer') > -1

    # test min_length exception
        min_string = deepcopy(valid_input)
        min_string['userID'] = 'ShortID'
        try:
            self.validate(min_string)
        except InputValidationError as err:
            assert err.error['failed_test'] == 'min_length'
            assert err.explain().find('be at least') > -1

    # test must_not_contain exception
        prohibited_string = deepcopy(valid_input)
        prohibited_string['userID'] = '6nPb/9gTwLz3f'
        try:
            self.validate(prohibited_string)
        except InputValidationError as err:
            assert err.error['failed_test'] == 'must_not_contain'
            assert err.explain().find('match neither') > -1

    # test must_contain exception
        required_words = deepcopy(valid_input)
        required_words['comments'][0] = 'a'
        try:
            self.validate(required_words)
        except InputValidationError as err:
            assert err.error['failed_test'] == 'must_contain'
            assert err.explain().find('match regex') > -1

    # test must_contain dictionary exception
        required_country = deepcopy(valid_input)
        required_country['address']['country'] = 'Canada'
        try:
            self.validate(required_country)
        except InputValidationError as err:
            assert err.error['failed_test'] == 'must_contain'
            assert err.explain().find('must reside in a United state') > -1

    # test contains_either exception
        optional_words = deepcopy(valid_input)
        optional_words['address']['region'] = 'N1'
        try:
            self.validate(optional_words)
        except InputValidationError as err:
            assert err.error['failed_test'] == 'contains_either'
            assert err.explain().find('match either') > -1

    # test empty list
        empty_list = deepcopy(valid_input)
        empty_list['comments'] = []
        input_value = self.keyMap['.comments']['min_size']
        self.keyMap['.comments']['min_size'] = 0
        assert self.validate(empty_list)
        self.keyMap['.comments']['min_size'] = input_value

    # test list reconstruction
        assert isinstance(self._reconstruct('.comments'), list)

    # test dict reconstruction
        assert isinstance(self._reconstruct('.address'), dict)

    # test nested reconstruction
        assert isinstance(self._reconstruct('.address.country_code'), int)
        assert isinstance(self._reconstruct('.comments[0]'), str)

    # test ingest valid input
        ingest_input = deepcopy(valid_input)
        self.ingest(**ingest_input)

    # test malformed dictionary datatype input ingestion
        malformed_datatype = deepcopy(valid_input)
        malformed_datatype['address'] = 'my home'
        valid_output = self.ingest(**malformed_datatype)
        assert not valid_output['address']['region']

    # test missing default input injection
        missing_default = deepcopy(valid_input)
        assert not 'rating' in missing_default.keys()
        valid_output = self.ingest(**missing_default)
        assert valid_output['rating'] == 5

    # test malformed default input replacement
        malformed_default = deepcopy(valid_input)
        malformed_default['rating'] = '5'
        valid_output = self.ingest(**malformed_default)
        assert valid_output['rating'] == 5

    # test invalid default input replacement
        invalid_default = deepcopy(valid_input)
        invalid_default['rating'] = 11
        valid_output = self.ingest(**invalid_default)
        assert valid_output['rating'] == 5

    # test missing input null injection
        missing_string = deepcopy(valid_input)
        del missing_string['userID']
        valid_output = self.ingest(**missing_string)
        assert isinstance(valid_output['userID'], str)
        assert not valid_output['userID']

    # test malformed input null injection
        malformed_string = deepcopy(valid_input)
        malformed_string['userID'] = { "key": "value" }
        valid_output = self.ingest(**malformed_string)
        assert isinstance(valid_output['userID'], str)
        assert not valid_output['userID']

    # test invalid input null injection
        invalid_string = deepcopy(valid_input)
        invalid_string['userID'] = 'tooShort'
        valid_output = self.ingest(**invalid_string)
        assert isinstance(valid_output['userID'], str)
        assert not valid_output['userID']

    # test strip extra field input
        extra_key_input['extraKey'] = 'string'
        ingest_input = deepcopy(extra_key_input)
        valid_output = self.ingest(**ingest_input)
        assert 'extraKey' in ingest_input.keys()
        assert not 'extraKey' in valid_output.keys()

    # test tag along of extra fields in input
        self.keyMap['.']['extra_fields'] = True
        ingest_input = deepcopy(extra_key_input)
        valid_output = self.ingest(**ingest_input)
        assert 'extraKey' in ingest_input.keys()
        assert 'extraKey' in valid_output.keys()
        self.keyMap['.']['extra_fields'] = False

    # test mass injection of defaults and nulls
        valid_output = self.ingest(**{})
        for key in self.schema.keys():
            assert key in valid_output.keys()
        assert valid_output['rating'] == 5
        assert not valid_output['userID']
        assert not valid_output['comments']
        assert valid_output['address']
        ex_int = 0
        assert valid_output['address']['country_code'].__class__ == ex_int.__class__

    # test nested default injection
        ingest_input = deepcopy(valid_input)
        assert not 'city' in ingest_input['address'].keys()
        valid_output = self.ingest(**ingest_input)
        assert valid_output['address']['city'] == 'New York'

    # test max list length ingestion
        long_list = deepcopy(valid_input)
        long_list['comments'].insert(0, 'pewter')
        assert len(long_list['comments']) == 4
        valid_output = self.ingest(**long_list)
        assert len(valid_output['comments']) == 3
        assert 'bronze' not in valid_output['comments']

        # print(self.validate(valid_input))
        print(self.ingest(**valid_input))
        # print(self.ingest(**{}))

        test_model = {
            'schema': self.schema,
            'components': self.components,
            'metadata': self.metadata,
            'title': self.title,
            'description': self.description,
            # 'max_size': self.maxSize,
            'url': self.url
        }

    # test list ingestion of dictionaries
        new_model = deepcopy(test_model)
        new_model['schema']['test_list'] = [ { 'test': 'me' } ]
        list_model = jsonModel(new_model)
        test_input = { 'test_list': [ { 'test': 'me' }, { 'test': 'you' } ] }
        valid_output = list_model.ingest(**test_input)
        assert valid_output['test_list']
        
    # test json valid structure of model components
        assert json.dumps(test_model)

    # test . use in key names
        dot_key_names = deepcopy(test_model)
        dot_key_names['schema']['.'] = { '.': '' }
        dot_key_names['components']['..'] = { 'required_field': False }
        dot_model = jsonModel(dot_key_names)
        dot_ingested = dot_model.ingest(**{'.': {'.': 'test'}})
        assert dot_ingested['.']['.'] == 'test'

    # test null values in model
        null_schema = deepcopy(test_model)
        null_schema['test'] = None
        null_model = jsonModel(null_schema)

    # test ingested values for declared null fields
        null_ingested = null_model.ingest(**{'reference': 'test'})
        assert null_ingested['reference'] == 'test'
        null_ingested = null_model.ingest(**{'reference': invalid_object})
        assert null_ingested['reference'] == None

    # test default_value ingestion of list datatypes
        default_list_model = deepcopy(test_model)
        default_list_model['components']['.comments']['default_value'] = [ 'default comment' ]
        default_list_input = deepcopy(valid_input)
        del default_list_input['comments']
        default_list_output = jsonModel(default_list_model).validate(default_list_input)
        assert default_list_output['comments'][0] == 'default comment'
        default_list_output = jsonModel(default_list_model).ingest(**default_list_input)
        assert default_list_output['comments'][0] == 'default comment'
        
    # test empty schema exception
        empty_schema = deepcopy(test_model)
        empty_schema['schema'] = {}
        try:
            jsonModel(empty_schema)
        except ModelValidationError as err:
            assert err

    # test invalid object data exception
        object_model = deepcopy
        count = 1
        try:
            jsonModel(object_model)
            count = 0
        except ModelValidationError as err:
            assert str(err).find('dictionary') > 0
        assert count

    # test invalid json data exception in dictionaries
        object_model = deepcopy(test_model)
        object_model['schema']['not_json'] = list_model
        try:
            jsonModel(object_model)
        except ModelValidationError as err:
            assert str(err).find('.not_json') > 0

    # test invalid json data exception in lists
        object_model['schema']['not_json'] = [ list_model ]
        try:
            jsonModel(object_model)
        except ModelValidationError as err:
            assert str(err).find('.not_json[0]') > 0

    # test wrong datatype qualifier keys in components exception
        null_criteria_error = deepcopy(test_model)
        null_criteria_error['components']['.reference']['integer_data'] = True
        count = 1
        try:
            jsonModel(null_criteria_error)
            count = 0
        except ModelValidationError as err:
            assert str(err).find('.reference') > 0
        assert count

    # test wrong datatype qualifier keys in components exception
        integer_criteria_error = deepcopy(test_model)
        integer_criteria_error['components']['.rating']['must_not_contain'] = [ '\\w' ]
        count = 1
        try:
            jsonModel(integer_criteria_error)
            count = 0
        except ModelValidationError as err:
            assert str(err).find('.rating') > 0
        assert count

    # test wrong datatype qualifier values in components exception
        contains_either_error = deepcopy(test_model)
        contains_either_error['components']['.address.region']['contains_either'].append(2)
        try:
            jsonModel(contains_either_error)
        except ModelValidationError as err:
            assert str(err).find('.address.region') > 0
    
    # test optional dictionary values for regex criteria
        regex_criteria_dict = deepcopy(test_model)
        country_contains = { '^United\s': 'must reside in a United state', '^[A|a].+': 'must reside in an A+ country' }
        regex_criteria_dict['components']['.address.country']['contains_either'] = country_contains
        regex_criteria_dict['components']['.address.country']['must_not_contain'] = { '^[A|a]': 'must not reside in an A+ country' }
        assert jsonModel(regex_criteria_dict)
    
    # test conflict between declared value and optional regex criteria
        regex_criteria_dict_error = deepcopy(test_model)
        regex_criteria_dict_error['components']['.address.country']['must_not_contain'] = { '^U': 'must not reside in U country' }
        try:
            jsonModel(regex_criteria_dict_error)
        except ModelValidationError as err:
            assert str(err).find('matches regex pattern')

    # test wrong datatype qualifier values in components exception
        min_size_error = deepcopy(test_model)
        min_size_error['components']['.comments']['min_size'] = -2
        try:
            jsonModel(min_size_error)
        except ModelValidationError as err:
            assert str(err).find('.comments') > 0

    # test wrong datatype qualifier values in components exception
        max_value_error = deepcopy(test_model)
        max_value_error['components']['.rating']['max_value'] = '10'
        try:
            jsonModel(max_value_error)
        except ModelValidationError as err:
            assert str(err).find('.rating') > 0

    # test wrong datatype qualifier values in components exception
        field_description_error = deepcopy(test_model)
        field_description_error['components']['.userID']['field_description'] = []
        try:
            jsonModel(field_description_error)
        except ModelValidationError as err:
            assert str(err).find('.userID') > 0

    # test integer only datatype qualifier values in components exception
        contains_either_error = deepcopy(test_model)
        contains_either_error['components']['.datetime']['field_position'] = 1.1
        try:
            jsonModel(contains_either_error)
        except ModelValidationError as err:
            assert str(err).find('.datetime') > 0

    # test conflicting byte data and range criteria exception
        byte_range_error = deepcopy(test_model)
        byte_range_error['components']['.emoticon']['min_value'] = 'Ng=='
        try:
            jsonModel(byte_range_error)
        except ModelValidationError as err:
            assert str(err).find('.emoticon') > 0

    # test conflicting greater_than and contains_either exception
        value_contains_error = deepcopy(test_model)
        value_contains_error['components']['.address.region']['greater_than'] = '1B'
        try:
            jsonModel(value_contains_error)
        except ModelValidationError as err:
            assert str(err).find('.address.region') > 0

    # test conflicting declared and excluded values in schema exception
        excluded_value_error = deepcopy(test_model)
        excluded_value_error['components']['.address.city']['excluded_values'] = [ 'New Orleans']
        try:
            jsonModel(excluded_value_error)
        except ModelValidationError as err:
            assert str(err).find('.address.city') > 0

    # test conflicting discrete and excluded values in schema exception
        discrete_value_error = deepcopy(test_model)
        discrete_value_error['components']['.address.city']['excluded_values'] = [ 'Miami' ]
        try:
            jsonModel(discrete_value_error)
        except ModelValidationError as err:
            assert str(err).find('.address.city') > 0

    # test conflicting default value and datatype in list exception
        default_value_error = deepcopy(test_model)
        default_value_error['components']['.comments']['default_value'] = [ 1 ]
        try:
            jsonModel(default_value_error)
        except ModelValidationError as err:
            assert str(err).find('.comments qualifier default_value[0]') > 0
            
    # test item designator pattern used in schema keys
        item_designator_error = deepcopy(test_model)
        item_designator_error['schema']['[1]'] = ''
        try:
            jsonModel(item_designator_error)
        except ModelValidationError as err:
            assert str(err).find('.[1]') > 0

    # test query rules input
        assert jsonModel(test_model, self.queryRules)

    # test query rules json file
        assert jsonModel(test_model, valid_rules)

    # test query rules extra field exception
        query_rules_field = deepcopy(self.queryRules)
        query_rules_field['.none_fields'] = {}
        try:
            jsonModel(test_model, query_rules_field)
        except ModelValidationError as err:
            assert str(err).find('.string_fields') > 0

    # test query rules extra qualifier exception
        query_rules_qualifier = deepcopy(self.queryRules)
        query_rules_qualifier['.string_fields']['field_title'] = 'not a qualifier'
        try:
            jsonModel(test_model, query_rules_qualifier)
        except ModelValidationError as err:
            assert str(err).find('.string_fields') > 0

    # test query rules qualifier value exception
        query_rules_value = deepcopy(self.queryRules)
        query_rules_value['.string_fields']['min_value'] = 0.0
        try:
            jsonModel(test_model, query_rules_value)
        except ModelValidationError as err:
            assert str(err).find('.string_fields') > 0

    # test internal walk method
        metals_list = [ 'gold', 'silver', 'bronze' ]
        metal_list = [ { 'metal': 'gold' }, { 'metal': 'silver' }, { 'metal': 'bronze' } ]
        test_input = {
            'metals': deepcopy(metals_list)
        }
        results = self._walk('.metals[0]', test_input)
        assert len(results) == 3
        test_input = {
            'metals': deepcopy(metal_list)
        }
        results = self._walk('.metals[0].metal', test_input)
        assert len(results) == 3
        for group in test_input['metals']:
            group['metal'] = deepcopy(metals_list)
        results = self._walk('.metals[0].metal[0]', test_input)
        assert len(results) == 9
        for group in test_input['metals']:
            group['metal'] = deepcopy(metal_list)
        results = self._walk('.metals[0].metal[0].metal', test_input)
        assert len(results) == 9
        for metals in test_input['metals']:
            for metal in metals['metal']:
                metal['metal'] = deepcopy(metals_list)
        results = self._walk('.metals[0].metal[0].metal[0]', test_input)
        assert len(results) == 27
        for metals in test_input['metals']:
            for metal in metals['metal']:
                metal['metal'] = deepcopy(metal_list)
        # print(test_input)
        results = self._walk('.metals[0].metal[0].metal[0].metal', test_input)
        assert len(results) == 27
        # print(results)
    
    # test internal walk with dictionaries
        test_input = { 'here': { 'there': { 'where': [ 'stare' ] } } }
        results = self._walk('.here.there.where', test_input)
        assert results[0][0] == 'stare'

    # test evaluate valid input
        truth_table = []
        for key, value in valid_query.items():
            if not isinstance(value, dict):
                value = { 'equal_to': value }
            truth_table.append(self._evaluate_field(valid_input, key, value))
        assert True in truth_table
        assert False in truth_table

        # print(valid_input)
        # print(valid_query)
        # print(truth_table)

    # test evaluate query field missing in input
        test_query = deepcopy(valid_query)
        test_input = deepcopy(valid_input)
        eval_kwargs = {
            'record_dict': test_input,
            'field_name': '.address.country_code',
            'field_criteria': test_query['.address.country_code']
        }
        eval_outcome = self._evaluate_field(**eval_kwargs)
        assert not eval_outcome

    # test evaluate query field missing with value_exists: false
        eval_kwargs['field_criteria']['value_exists'] = False
        eval_outcome = self._evaluate_field(**eval_kwargs)
        assert eval_outcome

    # test evaluate query field exists in input
        eval_kwargs['field_name'] = '.datetime'
        eval_kwargs['field_criteria'] = test_query['.datetime']
        eval_outcome = self._evaluate_field(**eval_kwargs)
        assert eval_outcome

    # test evaluate query field exists with value_exists: false
        eval_kwargs['field_criteria']['value_exists'] = False
        eval_outcome = self._evaluate_field(**eval_kwargs)
        assert not eval_outcome
        del eval_kwargs['field_criteria']['value_exists']

    # test evaluate map maximum size query failure
        eval_kwargs['field_name'] = '.address'
        eval_kwargs['field_criteria'] = test_query['address']
        eval_kwargs['field_criteria']['max_size'] = 10
        eval_outcome = self._evaluate_field(**eval_kwargs)
        assert not eval_outcome
        del eval_kwargs['field_criteria']['max_size']
        
    # test evaluate list maximum size query failure
        eval_kwargs['field_name'] = '.comments'
        eval_kwargs['field_criteria'] = test_query['comments']
        eval_kwargs['field_criteria']['max_size'] = 2
        eval_outcome = self._evaluate_field(**eval_kwargs)
        assert not eval_outcome
        del eval_kwargs['field_criteria']['max_size']

    # test evaluate unique values query failure
        eval_kwargs['record_dict']['comments'].append('gold')
        eval_outcome = self._evaluate_field(**eval_kwargs)
        assert not eval_outcome
        eval_kwargs['record_dict']['comments'].pop()

    # test evaluate min length query failure
        eval_kwargs['field_name'] = '.userID'
        eval_kwargs['field_criteria'] = test_query['.userID']
        eval_kwargs['field_criteria']['min_length'] = 14
        del eval_kwargs['field_criteria']['min_value']
        eval_kwargs['field_criteria']['max_length'] = 14
        del eval_kwargs['field_criteria']['max_value']
        eval_outcome = self._evaluate_field(**eval_kwargs)
        assert not eval_outcome

    # test evaluate max value query failure
        eval_kwargs['field_criteria']['min_length'] = 12
        eval_kwargs['field_criteria']['max_length'] = 14
        eval_kwargs['field_criteria']['max_value'] = '2222222222222'
        eval_outcome = self._evaluate_field(**eval_kwargs)
        assert not eval_outcome

    # test evaluate less than query failure
        eval_kwargs['field_name'] = '.datetime'
        eval_kwargs['field_criteria'] = test_query['.datetime']
        eval_kwargs['field_criteria']['less_than'] = 200000.0
        eval_outcome = self._evaluate_field(**eval_kwargs)
        assert not eval_outcome
        eval_kwargs['field_criteria']['less_than'] = 2000000000.0

    # test evaluate integer only query failure
        eval_kwargs['field_criteria']['integer_data'] = True
        eval_outcome = self._evaluate_field(**eval_kwargs)
        assert not eval_outcome
        del eval_kwargs['field_criteria']['integer_data']

    # test evaluate excluded values query failure
        eval_kwargs['field_name'] = '.emoticon',
        eval_kwargs['field_criteria'] = test_query['emoticon']
        eval_kwargs['field_criteria']['excluded_values'].append('aGFwcHk=')
        eval_outcome = self._evaluate_field(**eval_kwargs)
        assert not eval_outcome
        eval_kwargs['field_criteria']['excluded_values'].pop()

    # test evaluate discrete value query failure
        eval_kwargs['field_name'] = '.address.region',
        eval_kwargs['field_criteria'] = test_query['.address.region']
        eval_kwargs['field_criteria']['discrete_values'] = [ 'CA', 'MA' ]
        eval_outcome = self._evaluate_field(**eval_kwargs)
        assert not eval_outcome
        del eval_kwargs['field_criteria']['discrete_values']

    # test evaluate byte data query failure
        eval_kwargs['field_criteria']['byte_data'] = True
        eval_outcome = self._evaluate_field(**eval_kwargs)
        assert not eval_outcome
        del eval_kwargs['field_criteria']['byte_data']

    # test evaluate contains either query failure
        eval_kwargs['field_criteria']['contains_either'][0] = '[A-Z]{3}'
        eval_outcome = self._evaluate_field(**eval_kwargs)
        assert not eval_outcome
        eval_kwargs['field_criteria']['contains_either'][0] = '[A-Z]{2}'

    # test evaluate must contain query failure
        eval_kwargs['field_name'] = '.address.country'
        eval_kwargs['field_criteria'] = { 'must_contain': [ 'America' ] }
        eval_outcome = self._evaluate_field(**eval_kwargs)
        assert not eval_outcome
        del eval_kwargs['field_criteria']['must_contain']

    # test evaluate must not contain query failure
        eval_kwargs['field_criteria'] = { 'must_not_contain': [ 'States' ] }
        eval_outcome = self._evaluate_field(**eval_kwargs)
        assert not eval_outcome
        del eval_kwargs['field_criteria']['must_not_contain']

    # test evaluate must contain dictionary query failure
        eval_kwargs['field_criteria'] = {'must_contain': { 'America': 'must be from America'}}
        eval_outcome = self._evaluate_field(**eval_kwargs)
        assert not eval_outcome
        del eval_kwargs['field_criteria']['must_contain']

    # test evaluate must contain dictionary query failure
        eval_kwargs['field_criteria'] = {'must_not_contain': {'State': 'cannot be from a state'}}
        eval_outcome = self._evaluate_field(**eval_kwargs)
        assert not eval_outcome
        del eval_kwargs['field_criteria']['must_not_contain']

    # test evaluate contains either dictionary query
        eval_kwargs['field_criteria'] = {'contains_either': country_contains }
        eval_outcome = self._evaluate_field(**eval_kwargs)
        assert eval_outcome
        del eval_kwargs['field_criteria']['contains_either']
    
    # test sample empty query
        assert self.query(valid_query)
        assert isinstance(self.query(valid_query), bool)

    # test query criteria invalid qualifier exception
        query_qualifier_error = deepcopy(valid_query)
        query_qualifier_error['.address.region']['required_field'] = False
        try:
            self.query(query_qualifier_error)
        except QueryValidationError as err:
            assert str(err).find('.address.region') > 0

    # test query criteria value exists exception
        query_value_exists = deepcopy(valid_query)
        query_value_exists['.address.region']['value_exists'] = True
        self.query(query_value_exists)
        query_value_exists['.address.region']['value_exists'] = False
        try:
            self.query(query_value_exists)
        except QueryValidationError as err:
            assert str(err).find('value_exists:') > 0

    # test query method with valid query on valid input
        assert not self.query(valid_query, valid_input)
        assert isinstance(self.query(valid_query, valid_input), bool)

    # test query method with non-existent field
        assert self.query({'.rating': {'value_exists': False}}, valid_input)
        assert not self.query({'.rating': {'value_exists': True}}, valid_input)

    # test query method with boolean field queries
        assert self.query({'active': False}, valid_input)
        assert not self.query({'active': True}, valid_input)

    # test query method with number field queries
        assert self.query({'.datetime': {'value_exists': True}}, valid_input)
        assert not self.query({'.datetime': {'value_exists': False}}, valid_input)
        assert self.query({'.datetime':{'min_value': 1.1}}, valid_input)
        assert not self.query({'.datetime':{'min_value': 1500000000}}, valid_input)
        assert self.query({'.datetime': {'max_value': 1500000000}}, valid_input)
        assert not self.query({'.datetime': {'max_value': 1.1}}, valid_input)
        assert self.query({'.datetime': {'integer_data': False}}, valid_input)
        assert not self.query({'.datetime': {'integer_data': True}}, valid_input)
        test_input = deepcopy(valid_input)
        test_input['datetime'] = 50
        assert not self.query({'.datetime': {'integer_data': False}}, test_input)
        assert self.query({'.datetime': {'integer_data': True}}, test_input)
        assert not self.query({'.datetime': {'greater_than': 1449179763.312077}}, valid_input)
        assert not self.query({'.datetime': {'less_than': 1449179763.312077}}, valid_input)
        assert self.query({'.datetime': {'discrete_values': [1449179763.312077]}}, valid_input)
        assert not self.query({'.datetime': {'excluded_values': [1449179763.312077]}}, valid_input)
        assert self.query({'datetime': 1449179763.312077}, valid_input)
        assert not self.query({'datetime': 1449179763.31207}, valid_input)

    # test query method with string field queries
        assert self.query({'.userID': {'value_exists': True}}, valid_input)
        assert not self.query({'.userID': {'value_exists': False}}, valid_input)
        assert self.query({'.userID': {'min_length': 2}}, valid_input)
        assert not self.query({'.userID': {'min_length': 14}}, valid_input)
        assert not self.query({'.userID': {'max_length': 2}}, valid_input)
        assert self.query({'.userID': {'max_length': 14}}, valid_input)
        assert self.query({'.userID': {'min_value': '11111111111'}}, valid_input)
        assert not self.query({'.userID': {'min_value': 'zzzzzzzzzzz'}}, valid_input)
        assert not self.query({'.userID': {'max_value': '11111111111'}}, valid_input)
        assert self.query({'.userID': {'max_value': 'zzzzzzzzzzz'}}, valid_input)
        assert not self.query({'.userID': {'greater_than': '6nPbM9gTwLz3f'}}, valid_input)
        assert self.query({'.userID': {'greater_than': '6nPbM9gTwLz'}}, valid_input)
        assert not self.query({'.userID': {'less_than': '6nPbM9gTwLz3f'}}, valid_input)
        assert self.query({'.userID': {'less_than': '6nPbM9gTwLz3g'}}, valid_input)
        assert self.query({'.userID': {'discrete_values': ['6nPbM9gTwLz3f']}}, valid_input)
        assert not self.query({'.userID': {'discrete_values': ['6nPbM9gTwLz']}}, valid_input)
        assert not self.query({'.userID': {'excluded_values': ['6nPbM9gTwLz3f']}}, valid_input)
        assert self.query({'.userID': {'excluded_values': ['6nPbM9gTwLz']}}, valid_input)
        assert self.query({'.userID': {'must_contain': ['6nPbM9gTwLz']}}, valid_input)
        assert not self.query({'.userID': {'must_contain': ['/']}}, valid_input)
        assert self.query({'.address.country': {'must_contain': { '^United\s': 'US'}}}, valid_input)
        assert not self.query({'.address.country': {'must_contain': { '^States': 'US'}}}, valid_input)
        assert not self.query({'.userID': {'must_not_contain': ['6nPbM9gTwLz']}}, valid_input)
        assert self.query({'.userID': {'must_not_contain': ['/']}}, valid_input)
        assert self.query({'.address.country': {'must_not_contain': {'^[A|a].+': 'not A+'}}}, valid_input)
        assert not self.query({'.address.country': {'must_not_contain': {'States': 'not US'}}}, valid_input)
        assert self.query({'.userID': {'contains_either': ['6nPbM9gTwLz', '/']}}, valid_input)
        assert not self.query({'.userID': {'contains_either': [':', '/']}}, valid_input)
        assert self.query({'.address.country': {'contains_either': country_contains }}, valid_input)
        assert not self.query({'.address.country': {'contains_either': {'^[A|a].+': 'A+'}}}, valid_input)
        assert self.query({'.emoticon': {'byte_data': True}}, valid_input)
        assert not self.query({'.userID': {'byte_data': True}}, valid_input)
        assert self.query({'.userID': {'byte_data': False}}, valid_input)
        assert not self.query({'.emoticon': {'byte_data': False}}, valid_input)
        assert self.query({'address.country': 'United States'}, valid_input)
        assert not self.query({'address.country': 'United'}, valid_input)

    # test query method with map field queries
        assert self.query({'address': {'min_size': 2}}, valid_input)
        assert not self.query({'address': {'min_size': 1000}}, valid_input)
        assert not self.query({'address': {'max_size': 2}}, valid_input)
        assert self.query({'address': {'max_size': 1000}}, valid_input)
        
    # test query method with list field queries
        assert self.query({'.comments': {'value_exists': True}}, valid_input)
        assert not self.query({'.comments': {'value_exists': False}}, valid_input)
        assert self.query({'.comments': {'min_size': 2}}, valid_input)
        assert not self.query({'.comments': {'min_size': 4}}, valid_input)
        assert not self.query({'.comments': {'max_size': 2}}, valid_input)
        assert self.query({'.comments': {'max_size': 4}}, valid_input)
        assert self.query({'.comments': {'unique_values': True}}, valid_input)
        assert not self.query({'.comments': {'unique_values': False}}, valid_input)
        test_input = deepcopy(valid_input)
        test_input['comments'].append('gold')
        assert not self.query({'.comments': {'unique_values': True}}, test_input)
        assert self.query({'.comments': {'unique_values': False}}, test_input)

    # test items in list field queries
        assert self.query({'.comments[0]': {'value_exists': True}}, valid_input)
        assert not self.query({'.comments[0]': {'value_exists': False}}, valid_input)
        assert self.query({'.comments[0]': {'min_length': 3}}, valid_input)
        assert not self.query({'.comments[0]': {'min_length': 7}}, valid_input)
        assert self.query({'.comments[0]': {'must_contain': ['.{4}']}}, valid_input)
        assert not self.query({'.comments[0]': {'must_contain': ['tin']}}, valid_input)
        assert self.query({'.comments[0]': {'contains_either': ['gold', 'tin']}}, valid_input)
        assert not self.query({'.comments[0]': {'contains_either': ['tin', 'zinc']}}, valid_input)

    # test use_declared method
        use_declared_schema = deepcopy(test_model)
        use_declared_model = jsonModel(use_declared_schema)
        assert use_declared_model.use_declared()
        assert use_declared_model.keyMap['.rating']['default_value'] == 5
        assert use_declared_model.keyMap['.address.city']['default_value'] == 'New York'
        assert use_declared_model.keyMap['.address.region']['default_value'] == 'LA'
        assert len(use_declared_model.keyMap['.comments']['default_value']) == 1
        assert use_declared_model.keyMap['.active']['default_value']
    
    # test use_declared ingestion
        ingest_declared_schema = deepcopy(test_model)
        ingest_declared_schema['schema']['comments'].append('Escargot delecticious!!!')
        ingest_declared_model = jsonModel(ingest_declared_schema)
        assert len(ingest_declared_model.keyMap['.comments']['declared_value']) == 2
        ingest_declared_model.use_declared()
        assert len(ingest_declared_model.keyMap['.comments']['default_value']) == 2
        ingest_declared = ingest_declared_model.ingest()
        assert ingest_declared['userID'] == 'gY3Cv81QwL0Fs'
        assert ingest_declared['active']
        assert ingest_declared['rating'] == 5
        assert len(ingest_declared['comments']) == 2

        return self

if __name__ == '__main__':
    from timeit import timeit as timer
    t0 = timer()
    testQuery = json.loads(open('../samples/sample-query.json').read())
    testModel = json.loads(open('../samples/sample-model.json').read())
    testInput = json.loads(open('../samples/sample-input.json').read())
    testRules = json.loads(open('../samples/query-rules.json').read())
    jsonModelTests(testModel).unitTests(testInput, testQuery, testRules)
    t1 = timer()
    print(str(t1 - t0))
