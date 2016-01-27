__author__ = 'rcj1492'
__created__ = '2016.01'

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
            criteria_dict = {
                'required_field': False,
                'value_datatype': input_list[0].__class__
            }
            if isinstance(input_list[0], bool) or isinstance(input_list[0], str) or isinstance(input_list[0], int) or isinstance(input_list[0], float):
                criteria_dict['declared_value'] = input_list[0]
            key_criteria.append(criteria_dict)
            if isinstance(input_list[0], dict):
                self.dict(input_dict=input_list[0], path_to_root=key_path, key_name=key_name, key_criteria=key_criteria)
            elif isinstance(input_list[0], list):
                self.list(input_list=input_list[0], path_to_root=key_path, key_name=key_name, key_criteria=key_criteria)
        return key_name, key_criteria
