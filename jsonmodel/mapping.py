''' a package of data mapping classes '''
__author__ = 'rcj1492'
__created__ = '2016.01'
__license__ = 'MIT'

from jsonmodel.exceptions import ModelValidationError

class mapModel(object):

    '''
        a helper class of recursive methods to map the json model
    '''

    _dummy_int = 1
    _dummy_float = 1.1

    _datatype_names = [
        'string',
        'number',
        'number',
        'boolean',
        'map',
        'list',
        'null'
    ]
    _datatype_classes = [
        ''.__class__,
        _dummy_int.__class__,
        _dummy_float.__class__,
        True.__class__,
        {}.__class__,
        [].__class__,
        None.__class__
    ]

    def __init__(self, input):

        self.keyName = []
        self.keyCriteria = []

        if isinstance(input, dict):
            self.keyName = [ '.' ]
            self.keyCriteria = [ { 'required_field': True, 'value_datatype': 'map', 'extra_fields': False } ]
            self.dict(input, '')
        elif isinstance(input, list):
            self.list(input, '')
        else:
            raise ModelValidationError('Input for mapModel must be a dictionary or list.')

    def dict(self, input_dict, path_to_root):
        for key, value in input_dict.items():
            if not isinstance(key, str):
                key_path = path_to_root + '.' + str(key)
                raise ModelValidationError('Key name for field %s must be a string datatype.' % key_path)
            key_path = path_to_root + '.' + key
            self.keyName.append(key_path)
            try:
                class_index = self._datatype_classes.index(value.__class__)
            except:
                raise ModelValidationError('Value for field %s must be a json-valid datatype.' % key_path)
            criteria_dict = {
                'required_field': False,
                'value_datatype': self._datatype_names[class_index]
            }
        # add integer data criteria to integer fields
            if class_index == 1:
                criteria_dict['integer_data'] = True
        # enable required field if field has a non-empty value
            if input_dict[key]:
                criteria_dict['required_field'] = True
        # add extra fields to dictionary fields
            if isinstance(value, dict):
                criteria_dict['extra_fields'] = True
                if value:
                    criteria_dict['extra_fields'] = False
        # add declared value to string, integer and boolean fields
            if criteria_dict['value_datatype'] in ('boolean', 'string', 'number', 'list'):
                criteria_dict['declared_value'] = value
            self.keyCriteria.append(criteria_dict)
            if isinstance(value, dict):
                self.dict(input_dict=input_dict[key], path_to_root=key_path)
            elif isinstance(value, list):
                self.list(input_list=input_dict[key], path_to_root=key_path)

    def list(self, input_list, path_to_root):
        if input_list:
            key_path = path_to_root + '[0]'
            self.keyName.append(key_path)
            try:
                class_index = self._datatype_classes.index(input_list[0].__class__)
            except:
                raise ModelValidationError('Value for field %s must be a json-valid datatype.' % key_path)
            criteria_dict = {
                'required_field': False,
                'value_datatype': self._datatype_names[class_index]
            }
        # add integer data criteria to integer fields
            if class_index == 1:
                criteria_dict['integer_data'] = True
        # add extra fields to dictionary fields
            if isinstance(input_list[0], dict):
                criteria_dict['extra_fields'] = True
                if input_list[0]:
                    criteria_dict['extra_fields'] = False
        # add declared value to string, integer and boolean fields
            if isinstance(input_list[0], bool) or isinstance(input_list[0], str) or isinstance(input_list[0], int) or isinstance(input_list[0], float):
                criteria_dict['declared_value'] = input_list[0]
            self.keyCriteria.append(criteria_dict)
            if isinstance(input_list[0], dict):
                self.dict(input_dict=input_list[0], path_to_root=key_path)
            elif isinstance(input_list[0], list):
                self.list(input_list=input_list[0], path_to_root=key_path)
