__author__ = 'rcj1492'
__created__ = '2016.01'

import json
from copy import deepcopy
from jsonmodel.exceptions import InputValidationError
from jsonmodel.validators import jsonModel

class jsonModelTests(jsonModel):

    def __init__(self, data_model):
        jsonModel.__init__(self, data_model)

    def unitTests(self, valid_input):
        # print(self.keyMap)
        invalid_list = []
        try:
            self.validate(invalid_list)
        except InputValidationError as err:
            assert err.error['model_schema']
            assert err.error['failed_test'] == 'value_datatype'
        extra_key_input = deepcopy(valid_input)
        extra_key_input['extraKey'] = 'string'
        try:
            self.validate(extra_key_input)
        except InputValidationError as err:
            assert err.error['failed_test'] == 'extra_fields'
        missing_key_input = deepcopy(valid_input)
        del missing_key_input['active']
        try:
            self.validate(missing_key_input)
        except InputValidationError as err:
            assert err.error['failed_test'] == 'required_field'
        optional_key = deepcopy(valid_input)
        del optional_key['comments']
        assert not 'comments' in self.validate(optional_key).keys()
        default_rating = deepcopy(valid_input)
        new_default_rating = self.validate(default_rating)
        assert new_default_rating['rating'] == 5
        short_list = deepcopy(valid_input)
        short_list['comments'] = []
        try:
            self.validate(short_list)
        except InputValidationError as err:
            assert err.error['failed_test'] == 'min_size'
        long_list = deepcopy(valid_input)
        long_list['comments'].append('pewter')
        try:
            self.validate(long_list)
        except InputValidationError as err:
            assert err.error['failed_test'] == 'max_size'
        mixed_list = deepcopy(valid_input)
        mixed_list['comments'][1] = 100
        try:
            self.validate(mixed_list)
        except InputValidationError as err:
            assert err.error['failed_test'] == 'value_datatype'
        duplicate_list = deepcopy(valid_input)
        duplicate_list['comments'][2] = 'gold'
        try:
            self.validate(duplicate_list)
        except InputValidationError as err:
            assert err.error['failed_test'] == 'unique_values'
        integers_only = deepcopy(valid_input)
        integers_only['rating'] = 3.5
        try:
            self.validate(integers_only)
        except InputValidationError as err:
            assert err.error['failed_test'] == 'integer_only'
        max_number = deepcopy(valid_input)
        max_number['rating'] = 11
        try:
            self.validate(max_number)
        except InputValidationError as err:
            assert err.error['failed_test'] == 'max_value'
        min_number = deepcopy(valid_input)
        min_number['rating'] = 0
        try:
            self.validate(min_number)
        except InputValidationError as err:
            assert err.error['failed_test'] == 'min_value'
        discrete_number = deepcopy(valid_input)
        discrete_number['address']['country_code'] = 20
        try:
            self.validate(discrete_number)
        except InputValidationError as err:
            assert err.error['failed_test'] == 'discrete_values'
        byte_string = deepcopy(valid_input)
        byte_string['emoticon'] = 'happy'
        try:
            self.validate(byte_string)
        except InputValidationError as err:
            assert err.error['failed_test'] == 'byte_data'
        max_string = deepcopy(valid_input)
        max_string['userID'] = 'LongAlphaNumericID'
        try:
            self.validate(max_string)
        except InputValidationError as err:
            assert err.error['failed_test'] == 'max_length'
        min_string = deepcopy(valid_input)
        min_string['userID'] = 'ShortID'
        try:
            self.validate(min_string)
        except InputValidationError as err:
            assert err.error['failed_test'] == 'min_length'
        discrete_string = deepcopy(valid_input)
        discrete_string['address']['city'] = 'Boston'
        try:
            self.validate(discrete_string)
        except InputValidationError as err:
            assert err.error['failed_test'] == 'discrete_values'
        prohibited_string = deepcopy(valid_input)
        prohibited_string['userID'] = '6nPb/9gTwLz3f'
        try:
            self.validate(prohibited_string)
        except InputValidationError as err:
            assert err.error['failed_test'] == 'must_not_contain'
        required_words = deepcopy(valid_input)
        required_words['comments'][0] = 'a'
        try:
            self.validate(required_words)
        except InputValidationError as err:
            assert err.error['failed_test'] == 'must_contain'
        optional_words = deepcopy(valid_input)
        optional_words['address']['region'] = 'N1'
        try:
            self.validate(optional_words)
        except InputValidationError as err:
            assert err.error['failed_test'] == 'contains_either'
        # print(self.validate(valid_input))
        return self

testModel = json.loads(open('../models/sample-model.json').read())
testInput = json.loads(open('../models/sample-input.json').read())

jsonModelTests(testModel).unitTests(testInput)