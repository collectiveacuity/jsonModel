__author__ = 'rcj1492'
__created__ = '2015.11'

import json

class ModelValidationError(Exception):

    def __init__(self, message='', error=None):
        text = '\nModel declaration is invalid.\n%s' % message
        super(ModelValidationError, self).__init__(text)
        self.error = error

class InputValidationError(Exception):

    def __init__(self, message='', error=None):
        text = '\nInput is invalid.\n%s' % message
        super(InputValidationError, self).__init__(text)
        self.error = error

class mapModel(object):

    def __init__(self, input):
        if isinstance(input, dict):
            self.keyName, self.keyType = self.dict(input, '', [], [])
        elif isinstance(input, list):
            self.keyName, self.keyType = self.list(input, '', [], [])

    def dict(self, input_dict, path_to_root, key_name, key_type):
        for key, value in input_dict.items():
            if path_to_root:
                key_path = path_to_root + '.' + key
            else:
                key_path = key
            key_name.append(key_path)
            key_type.append(value.__class__)
            if isinstance(value, dict):
                self.dict(input_dict=input_dict[key], path_to_root=key_path, key_name=key_name, key_type=key_type)
            elif isinstance(value, list):
                self.list(input_list=input_dict[key], path_to_root=key_path, key_name=key_name, key_type=key_type)
        return key_name, key_type

    def list(self, input_list, path_to_root, key_name, key_type):
        for i in range(len(input_list)):
            key_path = path_to_root + '[%s]' % i
            key_name.append(key_path)
            key_type.append(input_list[i].__class__)
            if isinstance(input_list[i], dict):
                self.dict(input_dict=input_list[i], path_to_root=key_path, key_name=key_name, key_type=key_type)
            elif isinstance(input_list[i], list):
                self.list(input_list=input_list[i], path_to_root=key_path, key_name=key_name, key_type=key_type)
        return key_name, key_type

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
        self.keyType = mapModel(self.schema).keyType

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

    # validate components input & construct component method
        self.components = {}
        if 'components' in data_model.keys():
            if not isinstance(data_model['components'], dict):
                raise ModelValidationError('The value of data model "components" must be a dictionary.')
            self.components = data_model['components']

    # validate key names in components
        dummy_string = 'string'
        dummy_integer = 2
        dummy_float = 2.2
        dummy_boolean = True
        dummy_list = []
        dummy_map = {}
        for key, value in self.components.items():
            number_field = False
            if key not in self.keyName:
                raise ModelValidationError('Data model "components" key "%s" is not declared in "schema".' % key)
            elif not isinstance(value, dict):
                raise ModelValidationError('Value for the data model "components" key "%s" must be a dictionary.' % key)

    # validate component qualifier fields are appropriate to datatype
            data_type = self.keyType[self.keyName.index(key)]
            type_dict = {}
            if data_type == dummy_string.__class__:
                type_dict = self.__rules__['components']['string_fields']
            elif data_type == dummy_integer.__class__:
                type_dict = self.__rules__['components']['number_fields']
                number_field = True
            elif data_type == dummy_float.__class__:
                type_dict = self.__rules__['components']['number_fields']
                number_field = True
            elif data_type == dummy_boolean.__class__:
                type_dict = self.__rules__['components']['boolean_fields']
            elif data_type == dummy_list.__class__:
                type_dict = self.__rules__['components']['list_fields']
            elif data_type == dummy_map.__class__:
                type_dict = self.__rules__['components']['map_fields']
            if set(value.keys()) - set(type_dict.keys()):
                raise ModelValidationError('Data model "components" key "%s" may only have datatype %s qualifiers %s.' % (key, data_type, set(type_dict.keys())))

    # validate component qualifier field values are appropriate datatype
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


    def validate(self, input_dict):
        return input_dict

class requestModel(object):

    __rules__ = json.loads(open('request-rules.json').read())

    def __init__(self, request_model):
        self.model = jsonModel(self.__rules__).validate(request_model)

    def request(self, request_input):
        return request_input


testModel = json.loads(open('../models/sample-model.json').read())
jsonModel(testModel)