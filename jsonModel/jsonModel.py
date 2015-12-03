__author__ = 'rcj1492'
__created__ = '2015.11'

import json
import re
from base64 import b64encode, b64decode
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
            if isinstance(value, bool) or isinstance(value, str) or isinstance(value, int) or isinstance(value, float):
                criteria_dict['declared_value'] = value
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

        '''
            a method for testing data model declaration & initializing the class

        :param data_model: dictionary with json model architecture
        :return: jsonModel object
        '''

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
                    message = 'List at data model path .schema%s must declare an initial item for the list.' % self.keyName[i]
                    raise ModelValidationError(message)

    # validate title input & construct title method
        self.title = ''
        if 'title' in data_model.keys():
            if not isinstance(data_model['title'], str):
                raise ModelValidationError('Value for data model path .title must be a string.')
            self.title = data_model['title']

    # validate title input & construct title method
        self.url = ''
        if 'url' in data_model.keys():
            if not isinstance(data_model['url'], str):
                raise ModelValidationError('Value for data model path .url must be a string.')
            self.title = data_model['url']

    # validate max size input & construct max size method
        self.maxSize = None
        if 'max_size' in data_model.keys():
            if not isinstance(data_model['max_size'], int):
                raise ModelValidationError('Value for data model path .max_size must be a positive integer.')
            elif data_model['max_size'] < 0:
                raise ModelValidationError('Value for data model path .max_size must be a positive integer.')
            elif data_model['max_size']:
                self.maxSize = data_model['max_size']

    # validate components input & construct component method
        self.components = {}
        if 'components' in data_model.keys():
            if not isinstance(data_model['components'], dict):
                raise ModelValidationError('Value for data model path .components must be a dictionary.')
            self.components = data_model['components']

    # validate key names in components
        for key, value in self.components.items():
            number_field = False
            if key not in self.keyName:
                raise ModelValidationError('Data model path .components%s is not declared in "schema".' % key)
            elif not isinstance(value, dict):
                raise ModelValidationError('Value for data model path .components%s must be a dictionary.' % key)

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
                raise ModelValidationError('Data model "components%s" may only have datatype %s qualifiers %s.' % (key, data_type, set(type_dict.keys())))

    # validate component qualifier field values are appropriate value datatype
            for k, v in value.items():
                if k == 'default_value':
                    if number_field:
                        if not isinstance(v, int) and not isinstance(v, float):
                            raise ModelValidationError('Value for data model "components%s.%s"default_value" must be a number.' % key)
                    elif not isinstance(v, data_type):
                        raise ModelValidationError('Value for data model "components%s.default_value" must be a %s datatype.' % (key, data_type))
                elif k == 'min_value' or k == 'max_value':
                    if isinstance(v, bool) or (not isinstance(v, int) and not isinstance(v, float)):
                        raise ModelValidationError('Value for data model "components%s.%s" must be a number.' % (key, k))
                elif not isinstance(v, type_dict[k].__class__):
                    raise ModelValidationError('Value for data model "components%s.%s" must be a %s datatype.' % (key, k, type_dict[k].__class__))

    # validate individual qualifier field values
                if k == 'must_not_contain' or k == 'must_contain':
                    for item in v:
                        if not isinstance(item, str):
                            message = 'Each item in list at data model path .components%s.%s must be a string.' % (key, k)
                            raise ModelValidationError(message)
                if k == 'min_length' or k == 'max_length' or k == 'min_size' or k == 'max_size':
                    if v < 0:
                        message = 'Value for data model path components%s.%s cannot be negative.' % (key, k)
                        raise ModelValidationError(message)
                if k == 'discrete_values' or k == 'example_values':
                    for item in v:
                        if number_field:
                            if not isinstance(item, int) and not isinstance(item, float):
                                raise ModelValidationError('Each item in data model "components%s.%s" list must be a number.' % (key, k))
                        elif not isinstance(item, str):
                            message = 'Each item in list at data model path .components%s.%s must be a string.' % (key, k)
                            raise ModelValidationError(message)
                if k == 'identical_to':
                    if not v in self.keyName:
                        message = 'Value "%s" for data model path .components%s.%s not found in components keys.' % (v, key, k)
                        raise ModelValidationError(message)
                if k == 'unique_values':
                    if v:
                        item_name = key + '[0]'
                        item_datatype = self.keyCriteria[self.keyName.index(item_name)]['value_datatype']
                        if not isinstance("string", item_datatype) and not isinstance(2, item_datatype) and not isinstance(2.2, item_datatype):
                            message = '"unique_values": true requires value at data model path .components.%s[0] to be a string or number primitive.' % key
                            raise ModelValidationError(message)

    # validate default value declaration against other criteria
            declared_values = [ 'declared_value', 'default_value' ]
            schema_field = self.keyCriteria[self.keyName.index(key)]
            for qualifier in declared_values:
                if qualifier in value.keys() or qualifier in schema_field:
                    if qualifier in value.keys():
                        default = value[qualifier]
                        value_path = '.components%s.default_value' % key
                    else:
                        default = schema_field[qualifier]
                        value_path = '.schema%s' % key
                    if isinstance(default, str):
                        value_key = '"%s"' % default
                    else:
                        value_key = default
                    header = 'Value %s at data model path %s' % (value_key, value_path)
                    if 'min_value' in value.keys():
                        if default < value['min_value']:
                            message = '%s must not be less than %s "min_value".' % (header, value['min_value'])
                            raise ModelValidationError(message)
                    if 'max_value' in value.keys():
                        if default > value['max_value']:
                            message = '%s must not be greater than %s "max_value".' % (header, value['max_value'])
                            raise ModelValidationError(message)
                    if 'integer_only' in value.keys():
                        if value['integer_only']:
                            if not isinstance(default, int):
                                message = '%s must be an "integer_only".' % header
                                raise ModelValidationError(message)
                    if 'min_length' in value.keys():
                        if len(default) < value['min_length']:
                            message = '%s must be at least %s characters "min_length".' % (header, value['min_length'])
                            raise ModelValidationError(message)
                    if 'max_length' in value.keys():
                        if len(default) > value['max_length']:
                            message = '%s cannot be more than %s characters "max_length".' % (header, value['max_length'])
                            raise ModelValidationError(message)
                    if 'must_not_contain' in value.keys():
                        for regex in value['must_not_contain']:
                            regex_pattern = re.compile(regex)
                            if regex_pattern.findall(default):
                                message = '%s matches regex pattern "%s" in "must_not_contain".' % (header, regex)
                                raise ModelValidationError(message)
                    if 'must_contain' in value.keys():
                        for regex in value['must_contain']:
                            regex_pattern = re.compile(regex)
                            if not regex_pattern.findall(default):
                                message = '%s does not match regex pattern "%s" in "must_contain".' % (header, regex)
                                raise ModelValidationError(message)
                    if 'discrete_values' in value.keys():
                        if default not in value['discrete_values']:
                            message = '%s is not found in "discrete_values".' % header
                            raise ModelValidationError(message)
                    if 'byte_data' in value.keys():
                        message = '%s cannot be base64 decoded to "byte_data".' % header
                        try:
                            decoded_bytes = b64decode(default)
                        except:
                            raise ModelValidationError(message)
                        if not isinstance(decoded_bytes, bytes):
                            raise ModelValidationError(message)

    # validate example values declarations against other criteria
            if 'example_values' in value.keys():
                for i in range(len(value['example_values'])):
                    example = value['example_values'][i]
                    if isinstance(example, str):
                        header = 'Value "%s" at data model path .components%s.example_values[%s]' % (example, key, i)
                    else:
                        header = 'Value %s at data model path .components%s.example_values[%s]' % (example, key, i)
                    if 'min_value' in value.keys():
                        if example < value['min_value']:
                            message = '%s must not be less than %s "min_value".' % (header, value['min_value'])
                            raise ModelValidationError(message)
                    if 'max_value' in value.keys():
                        if example > value['max_value']:
                            message = '%s must not be greater than %s "max_value".' % (header, value['max_value'])
                            raise ModelValidationError(message)
                    if 'integer_only' in value.keys():
                        if value['integer_only']:
                            if not isinstance(example, int):
                                message = '%s must be an "integer_only".' % header
                                raise ModelValidationError(message)
                    if 'min_length' in value.keys():
                        if len(example) < value['min_length']:
                            message = '%s must be at least %s characters "min_length".' % (header, value['min_length'])
                            raise ModelValidationError(message)
                    if 'max_length' in value.keys():
                        if len(example) > value['max_length']:
                            message = '%s cannot be more than %s characters "max_length".' % (header, value['max_length'])
                            raise ModelValidationError(message)
                    if 'must_not_contain' in value.keys():
                        for regex in value['must_not_contain']:
                            regex_pattern = re.compile(regex)
                            if regex_pattern.findall(example):
                                message = '%s matches regex pattern "%s" in "must_not_contain".' % (header, regex)
                                raise ModelValidationError(message)
                    if 'must_contain' in value.keys():
                        for regex in value['must_contain']:
                            regex_pattern = re.compile(regex)
                            if not regex_pattern.findall(example):
                                message = '%s does not match regex pattern "%s" in "must_contain".' % (header, regex)
                                raise ModelValidationError(message)
                    if 'discrete_values' in value.keys():
                        if example not in value['discrete_values']:
                            message = '%s is not found in "discrete_values".' % header
                            raise ModelValidationError(message)
                    if 'byte_data' in value.keys():
                        message = '%s cannot be base64 decoded to "byte_data".' % header
                        try:
                            decoded_bytes = b64decode(example)
                        except:
                            raise ModelValidationError(message)
                        if not isinstance(decoded_bytes, bytes):
                            raise ModelValidationError(message)

    # TODO: validate discrete values declarations against other criteria

    # TODO: validate integer_only against min_value and max_value declarations

    # construct keyMap from components, key names and key criteria
        self.keyMap = {}
        for i in range(len(self.keyName)):
            self.keyMap[self.keyName[i]] = self.keyCriteria[i]
        for key, value in self.components.items():
            if key in self.keyMap.keys():
                for k, v in self.components[key].items():
                    self.keyMap[key][k] = v

    def dict(self, input_dict, schema_dict, path_to_root):

        '''
            a helper method for recursively validating keys in dictionaries

        :return input_dict
        '''

    # construct lists of keys in input dictionary
        if path_to_root:
            top_level_key = path_to_root
        else:
            top_level_key = '.'
        rules_top_level_key = re.sub('\[\d+\]', '[0]', top_level_key)
        input_keys = []
        input_key_list = []
        for key in input_dict.keys():
            input_key_name = path_to_root + '.' + key
            input_keys.append(input_key_name)
            input_key_list.append(key)

    # TODO: validate identical to qualifier for dictionary

    # TODO: incorporate lambda function and validation url methods

    # construct lists of keys in schema dictionary
        max_keys = []
        max_key_list = []
        req_keys = []
        req_key_list = []
        for key in schema_dict.keys():
            schema_key_name = path_to_root + '.' + key
            max_keys.append(schema_key_name)
            max_key_list.append(key)
            rules_schema_key_name = re.sub('\[\d+\]', '[0]', schema_key_name)
            if self.keyMap[rules_schema_key_name]['required_field']:
                req_keys.append(schema_key_name)
                req_key_list.append(key)

    # validate existence of required fields
        missing_keys = set(req_keys) - set(input_keys)
        if missing_keys:
            error_dict = {
                'model_schema': self.schema,
                'input_criteria': self.keyMap[rules_top_level_key],
                'failed_test': 'required_field',
                'input_path': top_level_key,
                'error_value': req_key_list,
                'error_code': 4002
            }
            error_dict['input_criteria']['required_keys'] = req_keys
            raise InputValidationError(error_dict)

    # validate existence of extra fields
        extra_keys = set(input_keys) - set(max_keys)
        if extra_keys and not self.keyMap[rules_top_level_key]['extra_fields']:
            extra_key_list = []
            for key in extra_keys:
                pathless_key = re.sub(rules_top_level_key, '', key, count=1)
                extra_key_list.append(pathless_key)
            error_dict = {
                'model_schema': self.schema,
                'input_criteria': self.keyMap[rules_top_level_key],
                'failed_test': 'extra_fields',
                'input_path': top_level_key,
                'error_value': extra_key_list,
                'error_code': 4003
            }
            error_dict['input_criteria']['maximum_scope'] = max_key_list
            raise InputValidationError(error_dict)

    # validate datatype of value
        for key, value in input_dict.items():
            input_key_name = path_to_root + '.' + key
            rules_input_key_name = re.sub('\[\d+\]', '[0]', input_key_name)
            if input_key_name in max_keys:
                input_criteria = self.keyMap[rules_input_key_name]
                error_dict = {
                    'model_schema': self.schema,
                    'input_criteria': input_criteria,
                    'failed_test': 'value_datatype',
                    'input_path': input_key_name,
                    'error_value': value.__class__,
                    'error_code': 4001
                }
                if value.__class__ != input_criteria['value_datatype']:
                    if isinstance(value, bool) or (not isinstance(value, int) and not isinstance(value, float)):
                        raise InputValidationError(error_dict)
                    elif not isinstance(2.2, input_criteria['value_datatype']) and not isinstance(2, input_criteria['value_datatype']):
                        raise InputValidationError(error_dict)

    # call appropriate validation sub-routine for datatype of value
                if isinstance(value, bool):
                    input_dict[key] = self.boolean(value, input_key_name)
                elif isinstance(value, int) or isinstance(value, float):
                    input_dict[key] = self.number(value, input_key_name)
                elif isinstance(value, str):
                    input_dict[key] = self.string(value, input_key_name)
                elif isinstance(value, dict):
                    input_dict[key] = self.dict(value, schema_dict[key], input_key_name)
                elif isinstance(value, list):
                    input_dict[key] = self.list(value, schema_dict[key], input_key_name)

    # set default values for empty optional fields
        for key in max_key_list:
            if key not in input_key_list:
                indexed_key = max_keys[max_key_list.index(key)]
                if indexed_key in self.components.keys():
                    if 'default_value' in self.components[indexed_key]:
                        input_dict[key] = self.components[indexed_key]['default_value']

        return input_dict

    def list(self, input_list, schema_list, path_to_root):

        '''
            a helper method for recursively validating items in a list

        :return: input_list
        '''

    # construct rules for list and items
        rules_path_to_root = re.sub('\[\d+\]', '[0]', path_to_root)
        list_rules = self.keyMap[rules_path_to_root]
        initial_key = rules_path_to_root + '[0]'
        item_rules = self.keyMap[initial_key]

    # construct list error report template
        list_error = {
            'model_schema': self.schema,
            'input_criteria': list_rules,
            'failed_test': 'value_datatype',
            'input_path': path_to_root,
            'error_value': 0,
            'error_code': 4001
        }

    # validate list rules
        if 'min_size' in list_rules.keys():
            if len(input_list) < list_rules['min_size']:
                list_error['failed_test'] = 'min_size'
                list_error['error_value'] = len(input_list)
                list_error['error_code'] = 4010
                raise InputValidationError(list_error)
        if 'max_size' in list_rules.keys():
            if len(input_list) > list_rules['max_size']:
                list_error['failed_test'] = 'max_size'
                list_error['error_value'] = len(input_list)
                list_error['error_code'] = 4011
                raise InputValidationError(list_error)

    # construct item error report template
        item_error = {
            'model_schema': self.schema,
            'input_criteria': item_rules,
            'failed_test': 'value_datatype',
            'input_path': initial_key,
            'error_value': input_list[0],
            'error_code': 4001
        }

    # validate datatype of items
        for i in range(len(input_list)):
            input_path = path_to_root + '[%s]' % i
            item = input_list[i]
            item_error['input_path'] = input_path
            item_error['error_value'] = item.__class__
            if item.__class__ != item_rules['value_datatype']:
                if isinstance(item, bool) or (not isinstance(item, int) and not isinstance(item, float)):
                    raise InputValidationError(item_error)
                elif not isinstance(2.2, item_rules['value_datatype']) and not isinstance(2, item_rules['value_datatype']):
                    raise InputValidationError(item_error)

    # call appropriate validation sub-routine for datatype of item
            if isinstance(item, bool):
                input_list[i] = self.boolean(item, input_path)
            elif isinstance(item, int) or isinstance(item, float):
                input_list[i] = self.number(item, input_path)
            elif isinstance(item, str):
                input_list[i] = self.string(item, input_path)
            elif isinstance(item, dict):
                input_list[i] = self.dict(item, schema_list[0], input_path)
            elif isinstance(item, list):
                input_list[i] = self.list(item, schema_list[0], input_path)

    # validate unique values in list
        if 'unique_values' in list_rules.keys():
            if len(set(input_list)) < len(input_list):
                list_error['failed_test'] = 'unique_values'
                list_error['error_value'] = input_list
                list_error['error_code'] = 4012
                raise InputValidationError(list_error)

    # TODO: validate identical to references

        return input_list

    def number(self, input_number, path_to_root):

        '''
            a helper method for recursively validating properties of a number

        :return: input_number
        '''

        rules_path_to_root = re.sub('\[\d+\]', '[0]', path_to_root)
        input_criteria = self.keyMap[rules_path_to_root]
        error_dict = {
            'model_schema': self.schema,
            'input_criteria': input_criteria,
            'failed_test': 'value_datatype',
            'input_path': path_to_root,
            'error_value': input_number,
            'error_code': 4001
        }


        return input_number

    def string(self, input_string, path_to_root):
        rules_path_to_root = re.sub('\[\d+\]', '[0]', path_to_root)
        input_criteria = self.keyMap[rules_path_to_root]
        error_dict = {
            'model_schema': self.schema,
            'input_criteria': input_criteria,
            'failed_test': 'value_datatype',
            'input_path': path_to_root,
            'error_value': input_string,
            'error_code': 4001
        }

        return input_string

    def boolean(self, input_boolean, path_to_root):
        rules_path_to_root = re.sub('\[\d+\]', '[0]', path_to_root)
        input_criteria = self.keyMap[rules_path_to_root]
        error_dict = {
            'model_schema': self.schema,
            'input_criteria': input_criteria,
            'failed_test': 'value_datatype',
            'input_path': path_to_root,
            'error_value': input_boolean,
            'error_code': 4001
        }

        return input_boolean

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
        input_dict = self.dict(input_dict, self.schema, '')
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
        default_input = deepcopy(valid_input)
        del default_input['datetime']
        new_default_input = self.validate(default_input)
        assert new_default_input['datetime'] == 1500
        short_list = deepcopy(valid_input)
        short_list['comments'].pop()
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
        print(self.validate(valid_input))
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