__author__ = 'rcj1492'
__created__ = '2016.01'

import json
import pytest
from copy import deepcopy
from jsonmodel.exceptions import InputValidationError, ModelValidationError
from jsonmodel.validators import jsonModel

class jsonModelTests(jsonModel):

    def __init__(self, data_model):
        jsonModel.__init__(self, data_model)

    def unitTests(self, valid_input):

        # print(self.keyMap)

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

    # test invalid input type
        invalid_list = []
        try:
            self.validate(invalid_list)
        except InputValidationError as err:
            assert err.error['model_schema']
            assert err.error['failed_test'] == 'value_datatype'

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

    # test invalid input data type
        try:
            self.validate('1449179763.312077', '.datetime')
        except InputValidationError as err:
            assert err.error['failed_test'] == 'value_datatype'

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

    # test integer_only exception
        integers_only = deepcopy(valid_input)
        integers_only['rating'] = 3.5
        try:
            self.validate(integers_only)
        except InputValidationError as err:
            assert err.error['failed_test'] == 'integer_only'

    # test max_value exception
        max_number = deepcopy(valid_input)
        max_number['rating'] = 11
        try:
            self.validate(max_number)
        except InputValidationError as err:
            assert err.error['failed_test'] == 'max_value'

    # test min_value exception
        min_number = deepcopy(valid_input)
        min_number['rating'] = 0
        try:
            self.validate(min_number)
        except InputValidationError as err:
            assert err.error['failed_test'] == 'min_value'

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

    # test discrete_values exception
        discrete_string = deepcopy(valid_input)
        discrete_string['address']['city'] = 'Boston'
        try:
            self.validate(discrete_string)
        except InputValidationError as err:
            assert err.error['failed_test'] == 'discrete_values'

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
        long_list['comments'].insert(0, 'peuter')
        assert len(long_list['comments']) == 4
        valid_output = self.ingest(**long_list)
        assert len(valid_output['comments']) == 3
        assert 'bronze' not in valid_output['comments']

        # print(self.validate(valid_input))
        # print(self.ingest(**valid_input))
        # print(self.ingest(**{}))

        return self

if __name__ == '__main__':
    from timeit import timeit as timer
    t0 = timer()
    testModel = json.loads(open('../models/sample-model.json').read())
    testInput = json.loads(open('../models/sample-input.json').read())
    jsonModelTests(testModel).unitTests(testInput)
    t1 = timer()
    print(str(t1 - t0))