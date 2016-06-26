__author__ = 'rcj1492'
__created__ = '2016.01'

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
        if isinstance(input, dict):
            key_name = [ '.' ]
            key_criteria = [ { 'required_field': True, 'value_datatype': 'map', 'extra_fields': False } ]
            self.keyName, self.keyCriteria = self.dict(input, '', key_name, key_criteria)
        elif isinstance(input, list):
            self.keyName, self.keyCriteria = self.list(input, '', [], [])

    def dict(self, input_dict, path_to_root, key_name, key_criteria):
        for key, value in input_dict.items():
            key_path = path_to_root + '.' + key
            key_name.append(key_path)
            class_index = self._datatype_classes.index(value.__class__)
            criteria_dict = {
                'required_field': False,
                'value_datatype': self._datatype_names[class_index]
            }
            if input_dict[key]:
                criteria_dict['required_field'] = True
            if isinstance(value, dict):
                criteria_dict['extra_fields'] = False
            if criteria_dict['value_datatype'] in ('boolean', 'string', 'number'):
                if value:
                    criteria_dict['declared_value'] = value
            key_criteria.append(criteria_dict)
            if isinstance(value, dict):
                self.dict(input_dict=input_dict[key], path_to_root=key_path, key_name=key_name, key_criteria=key_criteria)
            elif isinstance(value, list):
                self.list(input_list=input_dict[key], path_to_root=key_path, key_name=key_name, key_criteria=key_criteria)
        return key_name, key_criteria

    def list(self, input_list, path_to_root, key_name, key_criteria):
        if input_list:
            key_path = path_to_root + '[0]'
            key_name.append(key_path)
            class_index = self._datatype_classes.index(input_list[0].__class__)
            criteria_dict = {
                'required_field': False,
                'value_datatype': self._datatype_names[class_index]
            }
            if isinstance(input_list[0], bool) or isinstance(input_list[0], str) or isinstance(input_list[0], int) or isinstance(input_list[0], float):
                criteria_dict['declared_value'] = input_list[0]
            key_criteria.append(criteria_dict)
            if isinstance(input_list[0], dict):
                self.dict(input_dict=input_list[0], path_to_root=key_path, key_name=key_name, key_criteria=key_criteria)
            elif isinstance(input_list[0], list):
                self.list(input_list=input_list[0], path_to_root=key_path, key_name=key_name, key_criteria=key_criteria)
        return key_name, key_criteria
