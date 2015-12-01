__author__ = 'rcj1492'
__created__ = '2015.11'

import json
import re
from copy import deepcopy

class ModelValidationError(Exception):

    def __init__(self, message='', error=None):
        text = '\nModel declaration is invalid.\n%s' % message
        super(ModelValidationError, self).__init__(text)
        self.error = error

class InputValidationError(Exception):

    def __init__(self, error_dict=None):
        self.error = {
            'model_schema': {},
            'input_criteria': {},
            'failed_test': '',
            'input_path': {},
            'error_value': None,
            'error_code': 0
        }
        if isinstance(error_dict, dict):
            if 'model_schema' in error_dict:
                self.error['model_schema'] = error_dict['model_schema']
            if 'input_criteria' in error_dict:
                self.error['input_criteria'] = error_dict['input_criteria']
            if 'failed_test' in error_dict:
                self.error['failed_test'] = error_dict['failed_test']
            if 'input_path' in error_dict:
                self.error['input_path'] = error_dict['input_path']
            if 'error_value' in error_dict:
                self.error['error_value'] = error_dict['error_value']
            if 'error_code' in error_dict:
                self.error['error_code'] = error_dict['error_code']
        self.message = '\nError Report: %s' % self.error
        super(InputValidationError, self).__init__(self.message)

class mapModel(object):

    '''
        a helper class of recursive methods to map the json model
    '''

    def __init__(self, input):
        if isinstance(input, dict):
            key_name = [ '.' ]
            key_criteria = [ { 'required_field': True, 'value_datatype': {}.__class__, 'extra_fields': False } ]
            self.keyName, self.keyCriteria = self.dict(input, '', key_name, key_criteria)
        elif isinstance(input, list):
            self.keyName, self.keyCriteria = self.list(input, '', [], [])

    def dict(self, input_dict, path_to_root, key_name, key_criteria):
        for key, value in input_dict.items():
            key_path = path_to_root + '.' + key
            key_name.append(key_path)
            criteria_dict = {
                'required_field': False,
                'value_datatype': value.__class__
            }
            if input_dict[key]:
                criteria_dict['required_field'] = True
            if isinstance(value, dict):
                criteria_dict['extra_fields'] = False
            key_criteria.append(criteria_dict)
            if isinstance(value, dict):
                self.dict(input_dict=input_dict[key], path_to_root=key_path, key_name=key_name, key_criteria=key_criteria)
            elif isinstance(value, list):
                self.list(input_list=input_dict[key], path_to_root=key_path, key_name=key_name, key_criteria=key_criteria)
        return key_name, key_criteria

    def list(self, input_list, path_to_root, key_name, key_criteria):
        key_path = path_to_root + '[0]'
        key_name.append(key_path)
        criteria_dict = {
            'required_field': False,
            'value_datatype': input_list[0].__class__
        }
        key_criteria.append(criteria_dict)
        if isinstance(input_list[0], dict):
            self.dict(input_dict=input_list[0], path_to_root=key_path, key_name=key_name, key_criteria=key_criteria)
        elif isinstance(input_list[0], list):
            self.list(input_list=input_list[0], path_to_root=key_path, key_name=key_name, key_criteria=key_criteria)
        return key_name, key_criteria

class jsonModel(object):

    __rules__ = json.loads(open('model-rules.json').read())

    def __init__(self, data_model):

    # validate schema input
        if not isinstance(data_model, dict):
            raise ModelValidationError('Data model must be a dictionary.')
        elif 'schema' not in data_model.keys():
            raise ModelValidationError('Data model must have a schema key.')
        elif not isinstance(data_model['schema'], dict):
            raise ModelValidationError('Value for the data model "schema" field must be a dictionary.')
        elif not data_model['schema']:
            raise ModelValidationError('Data model "schema" field must not be empty.')

    # construct base methods
        self.schema = data_model['schema']
        self.keyName = mapModel(self.schema).keyName
        self.keyCriteria = mapModel(self.schema).keyCriteria

    # validate existence of first item in list declarations
        key_set = set(self.keyName)
        for i in range(len(self.keyName)):
            if isinstance([], self.keyCriteria[i]['value_datatype']):
                item_key = self.keyName[i] + '[0]'
                if not item_key in key_set:
                    raise ModelValidationError('List in "schema" key of data model at path "%s" must declare an initial item for the list.' % self.keyName[i])

    # validate title input & construct title method
        self.title = ''
        if 'title' in data_model.keys():
            if not isinstance(data_model['title'], str):
                raise ModelValidationError('The value of data model "title" must be a string.')
            self.title = data_model['title']

    # validate title input & construct title method
        self.url = ''
        if 'url' in data_model.keys():
            if not isinstance(data_model['url'], str):
                raise ModelValidationError('The value of data model "url" must be a string.')
            self.title = data_model['url']

    # validate max size input & construct max size method
        self.maxSize = None
        if 'max_size' in data_model.keys():
            if not isinstance(data_model['max_size'], int):
                raise ModelValidationError('The value of data model "max_size" must be a positive integer.')
            elif data_model['max_size'] < 0:
                raise ModelValidationError('The value of data model "max_size" must be a positive integer.')
            elif data_model['max_size']:
                self.maxSize = data_model['max_size']

    # validate components input & construct component method
        self.components = {}
        if 'components' in data_model.keys():
            if not isinstance(data_model['components'], dict):
                raise ModelValidationError('The value of data model "components" must be a dictionary.')
            self.components = data_model['components']

    # validate key names in components
        for key, value in self.components.items():
            number_field = False
            if key not in self.keyName:
                raise ModelValidationError('Data model "components" key "%s" is not declared in "schema".' % key)
            elif not isinstance(value, dict):
                raise ModelValidationError('Value for the data model "components" key "%s" must be a dictionary.' % key)

    # validate component qualifier fields are appropriate to component datatype
            data_type = self.keyCriteria[self.keyName.index(key)]['value_datatype']
            type_dict = {}
            if isinstance("string", data_type):
                type_dict = self.__rules__['components']['.string_fields']
            elif isinstance(2, data_type):
                type_dict = self.__rules__['components']['.number_fields']
                number_field = True
            elif isinstance(2.2, data_type):
                type_dict = self.__rules__['components']['.number_fields']
                number_field = True
            elif isinstance(True, data_type):
                type_dict = self.__rules__['components']['.boolean_fields']
            elif isinstance([], data_type):
                type_dict = self.__rules__['components']['.list_fields']
            elif isinstance({}, data_type):
                type_dict = self.__rules__['components']['.map_fields']
            if set(value.keys()) - set(type_dict.keys()):
                raise ModelValidationError('Data model "components" key "%s" may only have datatype %s qualifiers %s.' % (key, data_type, set(type_dict.keys())))

    # validate component qualifier field values are appropriate value datatype
            for k, v in value.items():
                if k == 'default_value':
                    if number_field:
                        if not isinstance(v, int) and not isinstance(v, float):
                            raise ModelValidationError('Value of data model "components" key "%s" qualifier field "default_value" must be a number datatype.' % key)
                    elif not isinstance(v, data_type):
                        raise ModelValidationError('Value of data model "components" key "%s" qualifier field "default_value" must be a %s datatype.' % (key, data_type))
                elif k == 'min_value' or k == 'max_value':
                    if not isinstance(v, int) and not isinstance(v, float):
                        raise ModelValidationError('Value of data model "components" key "%s" qualifier field "%s" must be a number datatype.' % (key, k))
                elif not isinstance(v, type_dict[k].__class__):
                    raise ModelValidationError('Value of data model "components" key "%s" qualifier field "%s" must be a %s datatype.' % (key, k, type_dict[k].__class__))

    # validate individual qualifier field values
                if k == 'must_not_contain' or k == 'must_contain':
                    for item in v:
                        if not isinstance(item, str):
                            raise ModelValidationError('Each data model "components" key "%s" qualifier field "%s" item must be a string.' % (key, k))
                if k == 'min_length' or k == 'max_length' or k == 'min_size' or k == 'max_size':
                    if v < 0:
                        raise ModelValidationError('Value of data model "components" key "%s" qualifier field "%s" cannot be negative.' % (key, k))
                if k == 'discrete_values' or k == 'example_values':
                    for item in v:
                        if number_field:
                            if not isinstance(item, int) and not isinstance(item, float):
                                raise ModelValidationError('Each data model "components" key "%s" qualifier field "%s" item must be a number.' % (key, k))
                        elif not isinstance(item, str):
                            raise ModelValidationError('Each data model "components" key "%s" qualifier field "%s" item must be a string.' % (key, k))
                if k == 'identical_to':
                    if not v in self.keyName:
                        raise ModelValidationError('Value of data model "components" key "%s" qualifier field "%s" not found in components keys.' % (key, k))
                if k == 'unique_values':
                    if v:
                        item_name = key + '[0]'
                        item_datatype = self.keyCriteria[self.keyName.index(item_name)]['value_datatype']
                        if not isinstance("string", item_datatype) and not isinstance(2, item_datatype) and not isinstance(2.2, item_datatype):
                            raise ModelValidationError('A "true" value for "unique_values" requires data model "components" key "%s[0]" to be a string or number primitive.' % key)

    # construct keyMap from components, key names and key criteria
        self.keyMap = {}
        for i in range(len(self.keyName)):
            self.keyMap[self.keyName[i]] = self.keyCriteria[i]
        for key, value in self.components.items():
            if key in self.keyMap.keys():
                for k, v in self.components[key].items():
                    self.keyMap[key][k] = v

    def dict(self, input_dict, schema_dict, path_to_root):
        max_keys = []
        key_list = []
        req_keys = []
        key_set = []
        input_keys = []
        if path_to_root:
            top_level_key = path_to_root
        else:
            top_level_key = '.'
        for key in schema_dict.keys():
            schema_key_name = path_to_root + '.' + key
            max_keys.append(schema_key_name)
            key_list.append(key)
            if self.keyMap[schema_key_name]['required_field']:
                req_keys.append(schema_key_name)
                key_set.append(key)
        for key in input_dict.keys():
            input_key_name = path_to_root + '.' + key
            input_keys.append(input_key_name)
        missing_keys = set(req_keys) - set(input_keys)
        if not path_to_root:
            input_path = '.'
        else:
            input_path = path_to_root
        if missing_keys:
            error_dict = {
                'model_schema': self.schema,
                'input_criteria': self.keyMap[top_level_key],
                'failed_test': 'required_field',
                'input_path': input_path,
                'error_value': key_set,
                'error_code': 4002
            }
            error_dict['input_criteria']['required_keys'] = req_keys
            raise InputValidationError(error_dict)
        for key, value in input_dict.items():
            input_key_name = path_to_root + '.' + key
            if input_key_name in max_keys:
                input_criteria = self.keyMap[input_key_name]
                error_dict = {
                    'model_schema': self.schema,
                    'input_criteria': input_criteria,
                    'failed_test': 'value_datatype',
                    'input_path': input_path,
                    'error_value': key,
                    'error_code': 4001
                }
                if isinstance(value, bool):
                    if not isinstance(value, input_criteria['value_datatype']):
                        raise InputValidationError(error_dict)
                    else:
                        self.boolean(value, input_key_name)
                elif isinstance(value, int) or isinstance(value, float):
                    if isinstance(3, input_criteria['value_datatype']) or isinstance(3.3, input_criteria['value_datatype']):
                        self.number(value, input_key_name)
                    else:
                        raise InputValidationError(error_dict)
                elif not isinstance(value, input_criteria['value_datatype']):
                    raise InputValidationError(error_dict)
                elif isinstance(value, str):
                    self.string(value, input_key_name)
                elif isinstance(value, dict):
                    self.dict(value, schema_dict[key], input_key_name)
                elif isinstance(value, list):
                    if 'unique_values' in input_criteria.keys():
                        if input_criteria['unique_values']:
                            self.set(value, schema_dict[key], input_key_name)
                        else:
                            self.list(value, schema_dict[key], input_key_name)
                    else:
                        self.list(value, schema_dict[key], input_key_name)
            elif not self.keyMap[top_level_key]['extra_fields']:
                error_dict = {
                    'model_schema': self.schema,
                    'input_criteria': self.keyMap[top_level_key],
                    'failed_test': 'extra_fields',
                    'input_path': input_path,
                    'error_value': key,
                    'error_code': 4003
                }
                error_dict['input_criteria']['maximum_scope'] = key_list
                raise InputValidationError(error_dict)


    def list(self, input_list, schema_list, path_to_root):
        pass

    def set(self, input_set, schema_set, path_to_root):
        pass

    def number(self, input_number, path_to_root):
        pass

    def string(self, input_string, path_to_root):
        pass

    def boolean(self, input_boolean, path_to_root):
        pass

    def validate(self, input_dict):
        if not isinstance(input_dict, dict):
            error_dict = {
                'model_schema': self.schema,
                'input_criteria': self.keyMap['.'],
                'failed_test': 'value_datatype',
                'input_path': '.',
                'error_value': input_dict.__class__,
                'error_code': 4001
            }
            raise InputValidationError(error_dict)
        self.dict(input_dict, self.schema, '')
        return input_dict

    def unitTests(self, valid_input):
        # print(self.keyMap)
        invalid_list = []
        try:
            self.validate(invalid_list)
        except InputValidationError as err:
            assert err.error['failed_test'] == 'value_datatype'
        extra_key_input = deepcopy(valid_input)
        extra_key_input['extraKey'] = 'string'
        try:
            self.validate(extra_key_input)
        except InputValidationError as err:
            assert err.error['model_schema']
            assert err.error['failed_test'] == 'extra_fields'
        missing_key_input = deepcopy(valid_input)
        del missing_key_input['active']
        try:
            self.validate(missing_key_input)
        except InputValidationError as err:
            assert err.error['failed_test'] == 'required_field'
        self.validate(valid_input)
        return self

class requestModel(object):

    __rules__ = json.loads(open('request-rules.json').read())

    def __init__(self, request_model):
        self.model = jsonModel(self.__rules__).validate(request_model)

    def request(self, request_input):
        return request_input


testModel = json.loads(open('../models/sample-model.json').read())
testInput = json.loads(open('../models/sample-input.json').read())
jsonModel(testModel).unitTests(testInput)