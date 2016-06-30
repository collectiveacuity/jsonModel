__author__ = 'rcj1492'
__created__ = '2016.01'

try:
    import pytest
except:
    import sys
    print('test_validators requires the pytest module. try "pip install pytest".')
    sys.exit()

import json
from copy import deepcopy
from jsonmodel.exceptions import InputValidationError, ModelValidationError
from jsonmodel.exceptions import QueryValidationError
from jsonmodel.validators import jsonModel

class jsonModelTests(jsonModel):

    def __init__(self, data_model):
        jsonModel.__init__(self, data_model)

    def unitTests(self, valid_input, valid_query):

        # print(self.keyMap)

    # test model fields
        assert isinstance(self.title, str)
        assert isinstance(self.description, str)
        assert isinstance(self.url, str)
        assert isinstance(self.metadata, dict)
        assert isinstance(self.maxSize, int)

    # test declarative fields in model keyMap
        assert self.keyMap['.userID']['required_field']
        assert self.keyMap['.rating']['default_value']
        assert self.keyMap['.emoticon']['byte_data']
        assert self.keyMap['.rating']['integer_data']
        assert self.keyMap['.userID']['min_length']
        assert self.keyMap['.comments[0]']['max_length']
        assert self.keyMap['.rating']['min_value']
        assert self.keyMap['.rating']['max_value']
        assert self.keyMap['.comments']['min_size']
        assert self.keyMap['.comments']['max_size']
        assert self.keyMap['.comments']['unique_values']
        assert self.keyMap['.userID']['must_not_contain']
        assert self.keyMap['.comments[0]']['must_contain']
        assert self.keyMap['.address.region']['contains_either']
        assert self.keyMap['.address.country_code']['discrete_values']
        assert self.keyMap['.emoticon']['example_values']
        assert self.keyMap['.address.region']['field_title']
        assert self.keyMap['.userID']['field_description']
        assert self.keyMap['.emoticon']['field_metadata']

        # TODO: "identical_to": ".similar_string",
        # TODO: "lambda_function": "",
        # TODO: "validation_url": "",

    # test empty path to root
        v_input = deepcopy(valid_input)
        assert self.validate(v_input)

    # test dot-path to root
        v_input = deepcopy(valid_input)
        assert self.validate(v_input, '.')

    # test individual component validation
        v_input = deepcopy(valid_input)
        assert self.validate(v_input['datetime'], '.datetime') == \
               v_input['datetime']
        v_input = deepcopy(valid_input)
        assert self.validate(v_input['userID'], '.userID') == \
               v_input['userID']
        v_input = deepcopy(valid_input)
        assert not self.validate(v_input['active'], '.active')
        v_input = deepcopy(valid_input)
        assert self.validate(v_input['comments'], '.comments') == \
               v_input['comments']
        v_input = deepcopy(valid_input)
        assert self.validate(v_input['address'], '.address') == \
               v_input['address']

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

    # test json structure of error message
        try:
            self.validate(invalid_list)
        except InputValidationError as err:
            assert json.dumps(err.error)

    # test invalid input data type
        try:
            self.validate('1449179763.312077', '.datetime')
        except InputValidationError as err:
            assert err.error['failed_test'] == 'value_datatype'
            assert json.dumps(err.error)

    # test extra_fields exception
        extra_key_input = deepcopy(valid_input)
        extra_key_input['extraKey'] = 'string'
        try:
            self.validate(extra_key_input)
        except InputValidationError as err:
            assert err.error['failed_test'] == 'extra_fields'

    # test required_field exception
        missing_key_input = deepcopy(valid_input)
        del missing_key_input['active']
        try:
            self.validate(missing_key_input)
        except InputValidationError as err:
            assert err.error['failed_test'] == 'required_field'

    # test required_field false in dictionaries
        optional_key = deepcopy(valid_input)
        del optional_key['comments']
        assert not 'comments' in self.validate(optional_key).keys()

    # test default_value insertion
        default_rating = deepcopy(valid_input)
        new_default_rating = self.validate(default_rating)
        assert new_default_rating['rating'] == 5

    # test min_size exception
        short_list = deepcopy(valid_input)
        short_list['comments'] = []
        try:
            self.validate(short_list)
        except InputValidationError as err:
            assert err.error['failed_test'] == 'min_size'

    # test max_size exception
        long_list = deepcopy(valid_input)
        long_list['comments'].append('pewter')
        try:
            self.validate(long_list)
        except InputValidationError as err:
            assert err.error['failed_test'] == 'max_size'

    # test value_datatype exception
        mixed_list = deepcopy(valid_input)
        mixed_list['comments'][1] = 100
        try:
            self.validate(mixed_list)
        except InputValidationError as err:
            assert err.error['failed_test'] == 'value_datatype'

    # test unique_values exception
        duplicate_list = deepcopy(valid_input)
        duplicate_list['comments'][2] = 'gold'
        try:
            self.validate(duplicate_list)
        except InputValidationError as err:
            assert err.error['failed_test'] == 'unique_values'

    # test integer_data exception
        integers_only = deepcopy(valid_input)
        integers_only['rating'] = 3.5
        try:
            self.validate(integers_only)
        except InputValidationError as err:
            assert err.error['failed_test'] == 'integer_data'

    # test min_value exception
        min_number = deepcopy(valid_input)
        min_number['rating'] = 0
        try:
            self.validate(min_number)
        except InputValidationError as err:
            assert err.error['failed_test'] == 'min_value'

    # test max_value exception
        max_number = deepcopy(valid_input)
        max_number['rating'] = 11
        try:
            self.validate(max_number)
        except InputValidationError as err:
            assert err.error['failed_test'] == 'max_value'

    # test greater_than exception for numbers
        greater_number = deepcopy(valid_input)
        greater_number['datetime'] = 0.1
        try:
            self.validate(greater_number)
        except InputValidationError as err:
            assert err.error['failed_test'] == 'greater_than'

    # test less_than exception for numbers
        less_number = deepcopy(valid_input)
        less_number['datetime'] = 2000000000.1
        try:
            self.validate(less_number)
        except InputValidationError as err:
            assert err.error['failed_test'] == 'less_than'

    # test min_value for strings exception
        low_string = deepcopy(valid_input)
        low_string['userID'] = '0000000000000'
        try:
            self.validate(low_string)
        except InputValidationError as err:
            assert err.error['failed_test'] == 'min_value'

    # test max_value for strings exception
        high_string = deepcopy(valid_input)
        high_string['userID'] = 'zzzzzzzzzzzzz'
        try:
            self.validate(high_string)
        except InputValidationError as err:
            assert err.error['failed_test'] == 'max_value'

    # test greater_than exception for strings
        greater_string = deepcopy(valid_input)
        greater_string['address']['region'] = 'AA'
        try:
            self.validate(greater_string)
        except InputValidationError as err:
            assert err.error['failed_test'] == 'greater_than'

    # test less_than exception for strings
        less_string = deepcopy(valid_input)
        less_string['address']['region'] = 'Zzzzzzzzzzzzzzzzzzzzzzzz'
        try:
            self.validate(less_string)
        except InputValidationError as err:
            assert err.error['failed_test'] == 'less_than'

    # test excluded_values for strings exception
        excluded_string = deepcopy(valid_input)
        excluded_string['emoticon'] = 'c2Fk'
        try:
            self.validate(excluded_string)
        except InputValidationError as err:
            assert err.error['failed_test'] == 'excluded_values'

    # test excluded_values for strings exception
        excluded_number = deepcopy(valid_input)
        excluded_number['rating'] = 7
        try:
            self.validate(excluded_number)
        except InputValidationError as err:
            assert err.error['failed_test'] == 'excluded_values'

    # test discrete_values exception
        discrete_string = deepcopy(valid_input)
        discrete_string['address']['city'] = 'Boston'
        try:
            self.validate(discrete_string)
        except InputValidationError as err:
            assert err.error['failed_test'] == 'discrete_values'

    # test discrete_values exception
        discrete_number = deepcopy(valid_input)
        discrete_number['address']['country_code'] = 20
        try:
            self.validate(discrete_number)
        except InputValidationError as err:
            assert err.error['failed_test'] == 'discrete_values'

    # test byte_data exception
        byte_string = deepcopy(valid_input)
        byte_string['emoticon'] = 'happy'
        try:
            self.validate(byte_string)
        except InputValidationError as err:
            assert err.error['failed_test'] == 'byte_data'

    # test max_length
        max_string = deepcopy(valid_input)
        max_string['userID'] = 'LongAlphaNumericID'
        try:
            self.validate(max_string)
        except InputValidationError as err:
            assert err.error['failed_test'] == 'max_length'

    # test min_length exception
        min_string = deepcopy(valid_input)
        min_string['userID'] = 'ShortID'
        try:
            self.validate(min_string)
        except InputValidationError as err:
            assert err.error['failed_test'] == 'min_length'

    # test must_not_contain exception
        prohibited_string = deepcopy(valid_input)
        prohibited_string['userID'] = '6nPb/9gTwLz3f'
        try:
            self.validate(prohibited_string)
        except InputValidationError as err:
            assert err.error['failed_test'] == 'must_not_contain'

    # test must_contain exception
        required_words = deepcopy(valid_input)
        required_words['comments'][0] = 'a'
        try:
            self.validate(required_words)
        except InputValidationError as err:
            assert err.error['failed_test'] == 'must_contain'

    # test contains_either exception
        optional_words = deepcopy(valid_input)
        optional_words['address']['region'] = 'N1'
        try:
            self.validate(optional_words)
        except InputValidationError as err:
            assert err.error['failed_test'] == 'contains_either'

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
        # print(self.ingest(**valid_input))
        # print(self.ingest(**{}))

        test_model = {
            'schema': self.schema,
            'components': self.components,
            'metadata': self.metadata,
            'title': self.title,
            'description': self.description,
            'max_size': self.maxSize,
            'url': self.url
        }

    # test json valid structure of model components
        assert json.dumps(test_model)

    # test . use in key names
        dot_key_names = deepcopy(test_model)
        dot_key_names['schema']['.'] = { '.': '' }
        dot_key_names['components']['..'] = { 'required_field': False }
        dot_model = jsonModel(dot_key_names)
        dot_ingested = dot_model.ingest(**{'.': {'.': 'test'}})
        assert dot_ingested['.']['.'] == 'test'

    # test null value in model
        null_schema = deepcopy(test_model)
        null_schema['test'] = None
        assert jsonModel(null_schema)

    # test empty schema exception
        empty_schema = deepcopy(test_model)
        empty_schema['schema'] = {}
        try:
            jsonModel(empty_schema)
        except ModelValidationError as err:
            assert err

    # test wrong datatype qualifier keys in components exception
        integer_criteria_error = deepcopy(test_model)
        integer_criteria_error['components']['.rating']['must_not_contain'] = [ '\\w' ]
        try:
            jsonModel(integer_criteria_error)
        except ModelValidationError as err:
            assert str(err).find('.rating') > 0

    # test wrong datatype qualifier values in components exception
        contains_either_error = deepcopy(test_model)
        contains_either_error['components']['.address.region']['contains_either'].append(2)
        try:
            jsonModel(contains_either_error)
        except ModelValidationError as err:
            assert str(err).find('.address.region') > 0

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

    # test item designator pattern used in schema keys
        item_designator_error = deepcopy(test_model)
        item_designator_error['schema']['[1]'] = ''
        try:
            jsonModel(item_designator_error)
        except ModelValidationError as err:
            assert str(err).find('.[1]') > 0

    # test query rules input
        assert jsonModel(test_model, self.queryRules)

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

    # test evaluate valid input
        truth_table = []
        for key, value in valid_query.items():
            truth_table.append(self._evaluate_field(valid_input, key, value))
        assert True in truth_table
        assert False in truth_table

        print(valid_input)
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

    # test evaluate maximum size query failure
        eval_kwargs['field_name'] = '.comments'
        eval_kwargs['field_criteria'] = test_query['.comments']
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
        eval_kwargs['field_criteria'] = test_query['.emoticon']
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
        eval_kwargs['field_name'] = '.address.country',
        eval_kwargs['field_criteria'] = { 'must_contain': [ 'America' ] }
        eval_outcome = self._evaluate_field(**eval_kwargs)
        assert not eval_outcome
        del eval_kwargs['field_criteria']['must_contain']

    # test evaluate must not contain query failure
        eval_kwargs['field_criteria'] = { 'must_not_contain': [ 'States' ] }
        eval_outcome = self._evaluate_field(**eval_kwargs)
        assert not eval_outcome

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
        assert not self.query({'.userID': {'must_not_contain': ['6nPbM9gTwLz']}}, valid_input)
        assert self.query({'.userID': {'must_not_contain': ['/']}}, valid_input)
        assert self.query({'.userID': {'contains_either': ['6nPbM9gTwLz', '/']}}, valid_input)
        assert not self.query({'.userID': {'contains_either': [':', '/']}}, valid_input)
        assert self.query({'.emoticon': {'byte_data': True}}, valid_input)
        assert not self.query({'.userID': {'byte_data': True}}, valid_input)
        assert self.query({'.userID': {'byte_data': False}}, valid_input)
        assert not self.query({'.emoticon': {'byte_data': False}}, valid_input)

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
        assert not self.query({'.comments[0]': {'min_length': 5}}, valid_input)
        assert self.query({'.comments[0]': {'must_contain': ['.{2}']}}, valid_input)
        assert not self.query({'.comments[0]': {'must_contain': ['g.{2}']}}, valid_input)
        assert self.query({'.comments[0]': {'contains_either': ['l', 'o']}}, valid_input)
        assert not self.query({'.comments[0]': {'contains_either': ['r', 'e']}}, valid_input)

        return self

if __name__ == '__main__':
    from timeit import timeit as timer
    t0 = timer()
    testQuery = json.loads(open('../models/sample-query.json').read())
    testModel = json.loads(open('../models/sample-model.json').read())
    testInput = json.loads(open('../models/sample-input.json').read())
    jsonModelTests(testModel).unitTests(testInput, testQuery)
    t1 = timer()
    print(str(t1 - t0))