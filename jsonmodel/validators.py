''' a package of data validation classes '''
__author__ = 'rcj1492'
__created__ = '2015.11'
__license__ = 'MIT'

import re
import sys
import json
from base64 import b64decode
from jsonmodel.exceptions import InputValidationError, ModelValidationError
from jsonmodel.exceptions import QueryValidationError
from jsonmodel.loader import jsonLoader
from jsonmodel.mapping import mapModel

class jsonModel(object):

    __rules__ = jsonLoader('jsonmodel', 'models/model-rules.json')

    def __init__(self, data_model, query_rules=None):

        '''
            a method for testing data model declaration & initializing the class

        :param data_model: dictionary with json model architecture
        :param query_rules: [optional] dictionary with valid field type qualifiers
        :return: object with jsonModel methods
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
        from copy import deepcopy
        self.dataModel = deepcopy(data_model)
        self.schema = self.dataModel['schema']
        model_map = mapModel(self.schema)
        self.keyName = model_map.keyName
        self.keyCriteria = model_map.keyCriteria

    # construct protected type classes
        self._datatype_names = mapModel._datatype_names
        self._datatype_classes = mapModel._datatype_classes

    # validate absence of item designators in keys
        item_pattern = re.compile('\[\d+\]')
        for i in range(len(self.keyName)):
            patterns_found = item_pattern.findall(self.keyName[i])
            if patterns_found:
                for designator in patterns_found:
                    if designator != '[0]':
                        message = 'Key name for schema field %s must not contain the item designator pattern %s' % (self.keyName[i], designator)
                        raise ModelValidationError(message)

    # validate existence of first item in list declarations
        key_set = set(self.keyName)
        for i in range(len(self.keyName)):
            if self.keyCriteria[i]['value_datatype'] == 'list':
                item_key = self.keyName[i] + '[0]'
                if not item_key in key_set:
                    message = 'Schema field %s must declare an initial item for the list.' % self.keyName[i]
                    raise ModelValidationError(message)

            # alter list requirement if first item is empty
                else:
                    item_index = self.keyName.index(item_key)
                    if not self.keyCriteria[item_index]['required_field']:
                        self.keyCriteria[i]['required_field'] = False

    # validate title input & construct title method
        self.title = ''
        if 'title' in self.dataModel.keys():
            if not isinstance(self.dataModel['title'], str):
                raise ModelValidationError('Value for model title must be a string.')
            self.title = self.dataModel['title']

    # validate description input & construct description method
        self.description = ''
        if 'description' in self.dataModel.keys():
            if not isinstance(self.dataModel['description'], str):
                raise ModelValidationError('Value for model description must be a string.')
            self.description = self.dataModel['description']

    # validate url input & construct title method
        self.url = ''
        if 'url' in self.dataModel.keys():
            if not isinstance(self.dataModel['url'], str):
                raise ModelValidationError('Value for model url must be a string.')
            self.title = self.dataModel['url']

    # validate metadata input & construct metadata method
        self.metadata = {}
        if 'metadata' in self.dataModel.keys():
            if not isinstance(self.dataModel['metadata'], dict):
                raise ModelValidationError('Value for model metadata must be a dictionary.')
            self.metadata = self.dataModel['metadata']

    # validate max size input & construct maxSize property
    #     self.maxSize = None
    #     if 'max_size' in self.dataModel.keys():
    #         if not isinstance(self.dataModel['max_size'], int):
    #             raise ModelValidationError('Value for model max_size must be a positive integer.')
    #         elif self.dataModel['max_size'] < 0:
    #             raise ModelValidationError('Value for model max_size must be a positive integer.')
    #         elif self.dataModel['max_size']:
    #             self.maxSize = self.dataModel['max_size']

    # validate components input & construct component property
        self.components = {}
        if 'components' in self.dataModel.keys():
            if not isinstance(self.dataModel['components'], dict):
                raise ModelValidationError('Value for model components must be a dictionary.')
            self.components = self._validate_fields(self.dataModel['components'], self.__rules__['components'])

    # construct keyMap fields from key names and key criteria
        self.keyMap = {}
        for i in range(len(self.keyName)):
            self.keyMap[self.keyName[i]] = self.keyCriteria[i]
        for key, value in self.components.items():

        # convert javascript dot_path to class dot_path
            dot_key = ''
            if not key:
                dot_key = '.'
            else:
                if key[0] != '.':
                    dot_key = '.%s' % key

        # add component declarations to keyMap
            if key in self.keyMap.keys():
                for k, v in self.components[key].items():
                    self.keyMap[key][k] = v
            elif dot_key and dot_key in self.keyMap.keys():
                for k, v in self.components[key].items():
                    self.keyMap[dot_key][k] = v

    # validate default values in lists
        self._validate_defaults(self.keyMap)

    # construct queryRules property from class model rules
        self.queryRules = {}
        for key, value in self.__rules__['components'].items():
            remove_from_query = [ 'required_field', 'default_value', 'example_values', 'field_title', 'field_position', 'field_description', 'field_metadata', 'extra_fields' ]
            field_qualifiers = {
                'value_exists': False
            }
            for k, v in value.items():
                if k not in remove_from_query:
                    field_qualifiers[k] = v
            self.queryRules[key] = field_qualifiers

    # validate query rules input and replace queryRules property
        if query_rules:
            if not isinstance(query_rules, dict):
                message = 'Value for query rules input must be a dictionary.'
                raise ModelValidationError(message)
            input_set = set(query_rules.keys())
            req_set = set(self.queryRules.keys())
            if input_set - req_set:
                message = 'Query rules input may only have %s field key names.' % req_set
                raise ModelValidationError(message)
            elif req_set - input_set:
                message = 'Query rules input must have all %s field key names.' % req_set
                raise ModelValidationError(message)
            for key in req_set:
                if not isinstance(query_rules[key], dict):
                    message = 'Value for query rules %s field must be a dictionary.' % key
                    raise ModelValidationError(message)
                input_qualifier_set = set(query_rules[key].keys())
                req_qualifier_set = set(self.queryRules[key].keys())
                if input_qualifier_set - req_qualifier_set:
                    message = 'Query rules field %s may only have qualifiers %s' % (key, req_qualifier_set)
                    raise ModelValidationError(message)
                for k, v in query_rules[key].items():
                    if v.__class__ != self.queryRules[key][k].__class__:
                        qualifier_index = self._datatype_classes.index(self.queryRules[key][k].__class__)
                        qualifier_type = self._datatype_names[qualifier_index]
                        message = 'Value for query rules field %s qualifier %s must be a "%s" datatype.' % (key, k, qualifier_type)
                        raise ModelValidationError(message)
            self.queryRules = query_rules

    def _validate_fields(self, fields_dict, fields_rules, declared_value=True):

    # validate key names in fields
        for key, value in fields_dict.items():
    
        # convert javascript dot_path to class dot_path
            if not key:
                key = '.'
            else:
                if key[0] != '.':
                    key = '.%s' % key
            
            if key not in self.keyName:
                raise ModelValidationError('Field %s is not a field declared in model schema.' % key)
            elif not isinstance(value, dict):
                raise ModelValidationError('Value for field %s must be a dictionary.' % key)

    # validate field criteria are appropriate to field datatype
            value_type = self.keyCriteria[self.keyName.index(key)]['value_datatype']
            type_dict = {}
            if value_type == 'string':
                type_dict = fields_rules['.string_fields']
            elif value_type == 'number':
                type_dict = fields_rules['.number_fields']
            elif value_type == 'boolean':
                type_dict = fields_rules['.boolean_fields']
            elif value_type == 'list':
                type_dict = fields_rules['.list_fields']
            elif value_type == 'map':
                type_dict = fields_rules['.map_fields']
            elif value_type == 'null':
                type_dict = fields_rules['.null_fields']
            if set(value.keys()) - set(type_dict.keys()):
                raise ModelValidationError('Field %s may only have datatype %s qualifiers %s.' % (key, value_type, set(type_dict.keys())))

    # validate criteria qualifier values are appropriate datatype
            for k, v in value.items():
                v_index = self._datatype_classes.index(v.__class__)
                v_type = self._datatype_names[v_index]
                qualifier_index = self._datatype_classes.index(type_dict[k].__class__)
                qualifier_type = self._datatype_names[qualifier_index]
                if v_type != qualifier_type:
                    if v_type != 'map' or k not in ('must_not_contain','must_contain','contains_either'):
                        message = 'Value for field %s qualifier %s must be a %s datatype.' % (key, k, qualifier_type)
                        raise ModelValidationError(message)
                if qualifier_type == 'number':
                    if isinstance(type_dict[k], int):
                        if not isinstance(v, int):
                            message = 'Value for field %s qualifier %s must be an integer.' % (key, k)
                            raise ModelValidationError(message)

    # validate internal logic of each qualifier value declaration
                if k in ('must_not_contain', 'must_contain', 'contains_either'):
                    patterns = v
                    k_type = 'list'
                    if isinstance(patterns, dict):
                        patterns = v.keys()
                        k_type = 'map'
                    for item in patterns:
                        if not isinstance(item, str):
                            message = 'Each %s in %s field %s qualifier %s must be a string.' % (v_type, k_type, key, k)
                            raise ModelValidationError(message)
                if k in ('min_length', 'max_length', 'min_size', 'max_size'):
                    if v < 0:
                        message = 'Value for field %s qualifier %s cannot be negative.' % (key, k)
                        raise ModelValidationError(message)
                if k in ('discrete_values', 'excluded_values', 'example_values'):
                    for item in v:
                        if value_type == 'number':
                            if not isinstance(item, int) and not isinstance(item, float):
                                message = 'Each item in field %s qualifier %s list must be a number.' % (key, k)
                                raise ModelValidationError(message)
                        elif not isinstance(item, str):
                            message = 'Each item in list for field %s qualifier %s must be a string.' % (key, k)
                            raise ModelValidationError(message)
                if k == 'identical_to':
                    if not v in self.keyName:
                        message = 'Value "%s" for field %s qualifier %s not found in components keys.' % (v, key, k)
                        raise ModelValidationError(message)
                if k == 'unique_values':
                    if v:
                        item_name = key + '[0]'
                        item_type = self.keyCriteria[self.keyName.index(item_name)]['value_datatype']
                        if not item_type in ('number', 'string'):
                            message = 'Field %s[0] must be either a string or number if qualifier "unique_values": true' % key
                            raise ModelValidationError(message)

    # validate lack of other qualifiers if value exist is false
            if 'value_exists' in value.keys():
                if not value['value_exists']:
                    if set(value.keys()) - {'value_exists'}:
                        message = 'If field %s qualifier value_exists: false, field may not have other qualifiers.' % key
                        raise ModelValidationError(message)

    # validate size qualifiers against each other
            size_qualifiers = ['min_size', 'max_size']
            for qualifier in size_qualifiers:
                if qualifier in value.keys():
                    test_value = value[qualifier]
                    value_path = 'field %s qualifier %s' % (key, qualifier)
                    header = 'Value %s for %s' % (test_value, value_path)
                    if 'min_size' in value.keys():
                        if test_value < value['min_size']:
                            message = '%s must not be less than "min_size": %s' % (header, value['min_size'])
                            raise ModelValidationError(message)
                    if 'max_size' in value.keys():
                        if test_value > value['max_size']:
                            message = '%s must not be greater than "max_size": %s' % (header, value['max_size'])
                            raise ModelValidationError(message)

    # validate length qualifiers against each other
            length_qualifiers = ['min_length', 'max_length']
            for qualifier in length_qualifiers:
                if qualifier in value.keys():
                    test_value = value[qualifier]
                    value_path = 'field %s qualifier %s' % (key, qualifier)
                    header = 'Value %s for %s' % (test_value, value_path)
                    if 'min_length' in value.keys():
                        if test_value < value['min_length']:
                            message = '%s must be at least "min_length": %s' % (header, value['min_length'])
                            raise ModelValidationError(message)
                    if 'max_length' in value.keys():
                        if test_value > value['max_length']:
                            message = '%s cannot be more than "max_length": %s' % (header, value['max_length'])
                            raise ModelValidationError(message)

    # validate range qualifiers against each other & length qualifiers
            range_qualifiers = ['min_value', 'max_value', 'greater_than', 'less_than', 'equal_to']
            for qualifier in range_qualifiers:
                if qualifier in value.keys():
                    test_value = value[qualifier]
                    value_path = 'field %s qualifier %s' % (key, qualifier)
                    quote_text = ''
                    if isinstance(test_value, str):
                        quote_text = '"'
                    header = 'Value %s%s%s for %s' % (quote_text, test_value, quote_text, value_path)
                    if 'min_value' in value.keys():
                        if test_value < value['min_value']:
                            message = '%s must not be less than "min_value": %s' % (header, value['min_value'])
                            raise ModelValidationError(message)
                    if 'max_value' in value.keys():
                        if test_value > value['max_value']:
                            message = '%s must not be greater than "max_value": %s' % (header, value['max_value'])
                            raise ModelValidationError(message)
                    if 'greater_than' in value.keys():
                        if test_value <= value['greater_than'] and not qualifier == 'greater_than':
                            message = '%s must be "greater_than": %s' % (header, value['greater_than'])
                            raise ModelValidationError(message)
                    if 'less_than' in value.keys():
                        if test_value >= value['less_than'] and not qualifier == 'less_than':
                            message = '%s must be "less_than": %s' % (header, value['less_than'])
                            raise ModelValidationError(message)
                    if 'min_length' in value.keys():
                        if len(test_value) < value['min_length']:
                            message = '%s must be at least "min_length": %s' % (header, value['min_length'])
                            raise ModelValidationError(message)
                    if 'max_length' in value.keys():
                        if len(test_value) > value['max_length']:
                            message = '%s cannot be more than "max_length": %s' % (header, value['max_length'])
                            raise ModelValidationError(message)
                    if 'integer_data' in value.keys():
                        if value['integer_data']:
                            if not isinstance(test_value, int):
                                message = '%s must be an "integer_data".' % header
                                raise ModelValidationError(message)
                    if 'must_not_contain' in value.keys():
                        patterns = value['must_not_contain']
                        if isinstance(patterns, dict):
                            patterns = value['must_not_contain'].keys()
                        for regex in patterns:
                            regex_pattern = re.compile(regex)
                            if regex_pattern.findall(test_value):
                                message = '%s matches regex pattern in "must_not_contain": ["%s"]' % (header, regex)
                                raise ModelValidationError(message)
                    if 'must_contain' in value.keys():
                        patterns = value['must_contain']
                        if isinstance(patterns, dict):
                            patterns = value['must_contain'].keys()
                        for regex in patterns:
                            regex_pattern = re.compile(regex)
                            if not regex_pattern.findall(test_value):
                                message = '%s does not match regex pattern in "must_contain": ["%s"].' % (header, regex)
                                raise ModelValidationError(message)
                    if 'contains_either' in value.keys():
                        regex_match = False
                        regex_patterns = []
                        patterns = value['contains_either']
                        if isinstance(patterns, dict):
                            patterns = value['contains_either'].keys()
                        for regex in patterns:
                            regex_patterns.append(regex)
                            regex_pattern = re.compile(regex)
                            if regex_pattern.findall(test_value):
                                regex_match = True
                        if not regex_match:
                            message = '%s does not match any regex patterns in "contains_either": %s' % (header, regex_patterns)
                            raise ModelValidationError(message)
                    if 'byte_data' in value.keys():
                        if value['byte_data']:
                            if qualifier != 'equal_to':
                                message = '%s cannot be used with base64 encoded "byte_data".' % header
                                raise ModelValidationError(message)

    # validate discrete value qualifiers against other criteria
            schema_field = self.keyCriteria[self.keyName.index(key)]
            discrete_qualifiers = ['declared_value', 'default_value', 'excluded_values', 'discrete_values', 'example_values']
            for qualifier in discrete_qualifiers:
                test_qualifier = False
                if qualifier in schema_field:
                    test_qualifier = True
                    if qualifier == 'declared_value' and not schema_field[qualifier]:
                        test_qualifier = False
                if qualifier in value.keys() or (test_qualifier and declared_value):
                    multiple_values = False
                    if qualifier in value.keys():
                        if isinstance(value[qualifier], list):
                            test_list = value[qualifier]
                            multiple_values = True
                        else:
                            test_list = [value[qualifier]]
                    else:
                        test_list = [schema_field[qualifier]]
                    value_path = 'field %s qualifier %s' % (key, qualifier)
                    for i in range(len(test_list)):
                        test_value = test_list[i]
                        quote_text = ''
                        if isinstance(test_value, str):
                            quote_text = '"'
                        item_text = ''
                        if multiple_values:
                            item_text = '[%s]' % i
                        header = 'Value %s%s%s for %s%s' % (quote_text, test_value, quote_text, value_path, item_text)
                        if 'min_value' in value.keys():
                            if test_value < value['min_value']:
                                message = '%s must not be less than "min_value": %s' % (header, value['min_value'])
                                raise ModelValidationError(message)
                        if 'max_value' in value.keys():
                            if test_value > value['max_value']:
                                message = '%s must not be greater than "max_value": %s' % (header, value['max_value'])
                                raise ModelValidationError(message)
                        if 'equal_to' in value.keys():
                            if test_value != value['equal_to']:
                                if qualifier != 'declared_value' and isinstance(test_value, bool):
                                    message = '%s must be "equal_to": %s' % (header, value['equal_to'])
                                    raise ModelValidationError(message)
                        if 'greater_than' in value.keys():
                            if test_value <= value['greater_than']:
                                message = '%s must be "greater_than": %s' % (header, value['greater_than'])
                                raise ModelValidationError(message)
                        if 'less_than' in value.keys():
                            if test_value >= value['less_than']:
                                message = '%s must be "less_than": %s' % (header, value['less_than'])
                                raise ModelValidationError(message)
                        if 'integer_data' in value.keys():
                            if value['integer_data']:
                                if not isinstance(test_value, int):
                                    message = '%s must be an "integer_data".' % header
                                    raise ModelValidationError(message)
                        if 'min_length' in value.keys():
                            if len(test_value) < value['min_length']:
                                message = '%s must be at least "min_length": %s' % (header, value['min_length'])
                                raise ModelValidationError(message)
                        if 'max_length' in value.keys():
                            if len(test_value) > value['max_length']:
                                message = '%s cannot be more than "max_length": %s' % (header, value['max_length'])
                                raise ModelValidationError(message)
                        if 'must_not_contain' in value.keys():
                            patterns = value['must_not_contain']
                            if isinstance(patterns, dict):
                                patterns = value['must_not_contain'].keys()
                            for regex in patterns:
                                regex_pattern = re.compile(regex)
                                if regex_pattern.findall(test_value):
                                    message = '%s matches regex pattern in "must_not_contain": ["%s"]' % (header, regex)
                                    raise ModelValidationError(message)
                        if 'must_contain' in value.keys():
                            patterns = value['must_contain']
                            if isinstance(patterns, dict):
                                patterns = value['must_contain'].keys()
                            for regex in patterns:
                                regex_pattern = re.compile(regex)
                                if not regex_pattern.findall(test_value):
                                    message = '%s does not match regex pattern in "must_contain": ["%s"]' % (header, regex)
                                    raise ModelValidationError(message)
                        if 'contains_either' in value.keys():
                            regex_match = False
                            regex_patterns = []
                            patterns = value['contains_either']
                            if isinstance(patterns, dict):
                                patterns = value['contains_either'].keys()
                            for regex in patterns:
                                regex_patterns.append(regex)
                                regex_pattern = re.compile(regex)
                                if regex_pattern.findall(test_value):
                                    regex_match = True
                            if not regex_match:
                                message = '%s does not match any regex patterns in "contains_either": %s' % (header, regex_patterns)
                                raise ModelValidationError(message)
                        if 'byte_data' in value.keys():
                            message = '%s cannot be base64 decoded to "byte_data".' % header
                            try:
                                decoded_bytes = b64decode(test_value)
                            except:
                                raise ModelValidationError(message)
                            if not isinstance(decoded_bytes, bytes):
                                raise ModelValidationError(message)

    # validate discrete value qualifiers against each other
            for qualifier in discrete_qualifiers:
                test_qualifier = False
                if qualifier in schema_field:
                    test_qualifier = True
                    if qualifier == 'declared_value' and not schema_field[qualifier]:
                        test_qualifier = False
                if qualifier in value.keys() or (test_qualifier and declared_value):
                    multiple_values = False
                    if qualifier in value.keys():
                        if isinstance(value[qualifier], list):
                            test_list = value[qualifier]
                            multiple_values = True
                        else:
                            test_list = [value[qualifier]]
                    else:
                        test_list = [schema_field[qualifier]]
                    value_path = 'field %s qualifier %s' % (key, qualifier)
                    for i in range(len(test_list)):
                        test_value = test_list[i]
                        quote_text = ''
                        if isinstance(test_value, str):
                            quote_text = '"'
                        item_text = ''
                        if multiple_values:
                            item_text = '[%s]' % i
                        header = 'Value %s%s%s for %s%s' % (quote_text, test_value, quote_text, value_path, item_text)
                        if 'excluded_values' in value.keys():
                            if not qualifier == 'excluded_values':
                                if test_value in value['excluded_values']:
                                    message = '%s cannot be one of "excluded_values": %s.' % (header, value['excluded_values'])
                                    raise ModelValidationError(message)
                        if 'discrete_values' in value.keys():
                            if not qualifier == 'excluded_values':
                                if test_value not in value['discrete_values']:
                                    message = '%s must be one of "discrete_values": %s' % (header, value['discrete_values'])
                                    raise ModelValidationError(message)

        return fields_dict

    def _validate_defaults(self, fields_dict):

    # validate key names in fields
        for key, value in fields_dict.items():
                    
    # retrieve value type and type dict
            value_type = self.keyCriteria[self.keyName.index(key)]['value_datatype']

    # validate discrete value qualifiers against other criteria
            qualifier = 'default_value'
            if qualifier in value.keys():
                multiple_values = False
                if isinstance(value[qualifier], list):
                    test_list = value[qualifier]
                    multiple_values = True
                else:
                    test_list = [value[qualifier]]
                value_path = 'field %s qualifier %s' % (key, qualifier)
                for i in range(len(test_list)):
                    test_value = test_list[i]
                    quote_text = ''
                    if isinstance(test_value, str):
                        quote_text = '"'
                    item_text = ''
                    if multiple_values:
                        item_text = '[%s]' % i
                    qualifier_text = value_path + item_text
                    header = 'Value %s%s%s for %s' % (quote_text, test_value, quote_text, qualifier_text)
                    if value_type == 'list':
                        default_item_key = '%s[0]' % key
                        try:
                            self.validate(test_value, default_item_key, object_title=header)
                        except Exception as err:
                            raise ModelValidationError(str(err).strip().replace('field %s' % default_item_key, qualifier_text))

        return fields_dict

    def _evaluate_field(self, record_dict, field_name, field_criteria):

        ''' a helper method for evaluating record values based upon query criteria

        :param record_dict: dictionary with model valid data to evaluate
        :param field_name: string with path to root of query field
        :param field_criteria: dictionary with query operators and qualifiers
        :return: boolean (True if no field_criteria evaluate to false)
        '''

    # determine value existence criteria
        value_exists = True
        if 'value_exists' in field_criteria.keys():
            if not field_criteria['value_exists']:
                value_exists = False

    # validate existence of field
        field_exists = True
        record_values = []
        try:
            record_values = self._walk(field_name, record_dict)
        except:
            field_exists = False

    # evaluate existence query criteria
        if value_exists != field_exists:
            return False
        elif not value_exists:
            return True

    # convert javascript dot_path to class dot_path
        field_key = field_name
        if not field_name:
            field_key = '.'
        else:
            if field_name[0] != '.':
                field_key = '.%s' % field_name

    # evaluate other query criteria
        for key, value in field_criteria.items():
            if key in ('min_size', 'min_length'):
                found = False
                if self.keyMap[field_key]['value_datatype'] == 'map':
                    for record_value in record_values:
                        record_size = sys.getsizeof(json.dumps(str(record_value)).replace(' ','')) - 51
                        if record_size >= value:
                            found = True
                            break
                else:
                    for record_value in record_values:
                        if len(record_value) >= value:
                            found = True
                            break
                if not found:
                    return False
            elif key in ('max_size', 'max_length'):
                found = False
                if self.keyMap[field_key]['value_datatype'] == 'map':
                    for record_value in record_values:
                        record_size = sys.getsizeof(json.dumps(str(record_value)).replace(' ','')) - 51
                        if record_size <= value:
                            found = True
                            break
                else:
                    for record_value in record_values:
                        if len(record_value) <= value:
                            found = True
                            break
                if not found:
                    return False
            elif key == 'min_value':
                found = False
                for record_value in record_values:
                    if record_value >= value:
                        found = True
                        break
                if not found:
                    return False
            elif key == 'max_value':
                found = False
                for record_value in record_values:
                    if record_value <= value:
                        found = True
                        break
                if not found:
                    return False
            elif key == 'equal_to':
                found = False
                for record_value in record_values:
                    if record_value == value:
                        found = True
                        break
                if not found:
                    return False
            elif key == 'greater_than':
                found = False
                for record_value in record_values:
                    if record_value > value:
                        found = True
                        break
                if not found:
                    return False
            elif key == 'less_than':
                found = False
                for record_value in record_values:
                    if record_value < value:
                        found = True
                        break
                if not found:
                    return False
            elif key == 'excluded_values':
                for record_value in record_values:
                    if record_value in value:
                        return False
            elif key == 'discrete_values':
                found = False
                for record_value in record_values:
                    if record_value in value:
                        found = True
                        break
                if not found:
                    return False
            elif key == 'integer_data':
                found = False
                dummy_int = 1
                for record_value in record_values:
                    if record_value.__class__ == dummy_int.__class__:
                        found = True
                        break
                if value != found:
                    return False
            elif key == 'byte_data':
                found = False
                for record_value in record_values:
                    try:
                        decoded_bytes = b64decode(record_value)
                    except:
                        decoded_bytes = ''
                    if isinstance(decoded_bytes, bytes):
                        found = True
                        break
                if value != found:
                    return False
            elif key == 'must_contain':
                patterns = value
                if isinstance(value, dict):
                    patterns = value.keys()
                for regex in patterns:
                    regex_pattern = re.compile(regex)
                    found = False
                    for record_value in record_values:
                        if regex_pattern.findall(record_value):
                            found = True
                            break
                    if not found:
                        return False
            elif key == 'must_not_contain':
                patterns = value
                if isinstance(value, dict):
                    patterns = value.keys()
                for regex in patterns:
                    regex_pattern = re.compile(regex)
                    found = False
                    for record_value in record_values:
                        if regex_pattern.findall(record_value):
                            found = True
                            break
                    if found:
                        return False
            elif key == 'contains_either':
                found = False
                patterns = value
                if isinstance(value, dict):
                    patterns = value.keys()
                for regex in patterns:
                    regex_pattern = re.compile(regex)
                    for record_value in record_values:
                        if regex_pattern.findall(record_value):
                            found = True
                            break
                    if found:
                        break
                if not found:
                    return False
            elif key == 'unique_values':
                for record_value in record_values:
                    unique_values = True
                    if len(record_value) != len(set(record_value)):
                        unique_values = False
                    if value != unique_values:
                        return False

        return True

    def _validate_dict(self, input_dict, schema_dict, path_to_root, object_title=''):

        ''' a helper method for recursively validating keys in dictionaries

        :return input_dict
        '''

    # reconstruct key path to current dictionary in model
        rules_top_level_key = re.sub('\[\d+\]', '[0]', path_to_root)
        map_rules = self.keyMap[rules_top_level_key]

    # construct list error report template
        map_error = {
            'object_title': object_title,
            'model_schema': self.schema,
            'input_criteria': map_rules,
            'failed_test': 'value_datatype',
            'input_path': path_to_root,
            'error_value': 0,
            'error_code': 4001
        }

    # validate map size
        if 'min_size' in map_rules.keys():
            input_size = sys.getsizeof(json.dumps(str(input_dict)).replace(' ','')) - 51
            if input_size < map_rules['min_size']:
                map_error['failed_test'] = 'min_size'
                map_error['error_value'] = input_size
                map_error['error_code'] = 4031
                raise InputValidationError(map_error)
        if 'max_size' in map_rules.keys():
            input_size = sys.getsizeof(json.dumps(str(input_dict)).replace(' ','')) - 51
            if input_size > map_rules['max_size']:
                map_error['failed_test'] = 'max_size'
                map_error['error_value'] = input_size
                map_error['error_code'] = 4032
                raise InputValidationError(map_error)

    # construct lists of keys in input dictionary
        input_keys = []
        input_key_list = []
        for key in input_dict.keys():
            error_dict = {
                'object_title': object_title,
                'model_schema': self.schema,
                'input_criteria': self.keyMap[rules_top_level_key],
                'failed_test': 'key_datatype',
                'input_path': path_to_root,
                'error_value': key,
                'error_code': 4004
            }
            error_dict['input_criteria']['key_datatype'] = 'string'
            if path_to_root == '.':
                if not isinstance(key, str):
                    input_key_name = path_to_root + str(key)
                    error_dict['input_path'] = input_key_name
                    raise InputValidationError(error_dict)
                input_key_name = path_to_root + key
            else:
                if not isinstance(key, str):
                    input_key_name = path_to_root + '.' + str(key)
                    error_dict['input_path'] = input_key_name
                    raise InputValidationError(error_dict)
                input_key_name = path_to_root + '.' + key
            input_keys.append(input_key_name)
            input_key_list.append(key)

    # TODO: validate top-level key and values against identical to reference

    # TODO: run lambda function and call validation

    # construct lists of keys in schema dictionary
        max_keys = []
        max_key_list = []
        req_keys = []
        req_key_list = []
        for key in schema_dict.keys():
            if path_to_root == '.':
                schema_key_name = path_to_root + key
            else:
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
                'object_title': object_title,
                'model_schema': self.schema,
                'input_criteria': self.keyMap[rules_top_level_key],
                'failed_test': 'required_field',
                'input_path': path_to_root,
                'error_value': list(missing_keys),
                'error_code': 4002
            }
            error_dict['input_criteria']['required_keys'] = req_keys
            raise InputValidationError(error_dict)

    # validate existence of extra fields
        extra_keys = set(input_keys) - set(max_keys)
        if extra_keys and not self.keyMap[rules_top_level_key]['extra_fields']:
            # extra_key_list = []
            # for key in extra_keys:
            #     pathless_key = re.sub(rules_top_level_key, '', key, count=1)
            #     extra_key_list.append(pathless_key)
            error_dict = {
                'object_title': object_title,
                'model_schema': self.schema,
                'input_criteria': self.keyMap[rules_top_level_key],
                'failed_test': 'extra_fields',
                'input_path': path_to_root,
                'error_value': list(extra_keys),
                'error_code': 4003
            }
            error_dict['input_criteria']['maximum_scope'] = list(max_keys)
            raise InputValidationError(error_dict)

    # validate datatype of value
        for key, value in input_dict.items():
            if path_to_root == '.':
                input_key_name = path_to_root + key
            else:
                input_key_name = path_to_root + '.' + key
            rules_input_key_name = re.sub('\[\d+\]', '[0]', input_key_name)
            if input_key_name in max_keys:
                input_criteria = self.keyMap[rules_input_key_name]
                error_dict = {
                    'object_title': object_title,
                    'model_schema': self.schema,
                    'input_criteria': input_criteria,
                    'failed_test': 'value_datatype',
                    'input_path': input_key_name,
                    'error_value': value,
                    'error_code': 4001
                }
                try:
                    value_index = self._datatype_classes.index(value.__class__)
                except:
                    error_dict['error_value'] = value.__class__.__name__
                    raise InputValidationError(error_dict)
                value_type = self._datatype_names[value_index]
                if input_criteria['value_datatype'] == 'null':
                    pass
                else:
                    if value_type != input_criteria['value_datatype']:
                        raise InputValidationError(error_dict)

    # call appropriate validation sub-routine for datatype of value
                    if value_type == 'boolean':
                        input_dict[key] = self._validate_boolean(value, input_key_name, object_title)
                    elif value_type == 'number':
                        input_dict[key] = self._validate_number(value, input_key_name, object_title)
                    elif value_type == 'string':
                        input_dict[key] = self._validate_string(value, input_key_name, object_title)
                    elif value_type == 'map':
                        input_dict[key] = self._validate_dict(value, schema_dict[key], input_key_name, object_title)
                    elif value_type == 'list':
                        input_dict[key] = self._validate_list(value, schema_dict[key], input_key_name, object_title)

    # set default values for empty optional fields
        for key in max_key_list:
            if key not in input_key_list:
                indexed_key = max_keys[max_key_list.index(key)]
                if indexed_key in self.components.keys():
                    if 'default_value' in self.components[indexed_key]:
                        input_dict[key] = self.components[indexed_key]['default_value']

        return input_dict

    def _validate_list(self, input_list, schema_list, path_to_root, object_title=''):

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
            'object_title': object_title,
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
                list_error['error_code'] = 4031
                raise InputValidationError(list_error)
        if 'max_size' in list_rules.keys():
            if len(input_list) > list_rules['max_size']:
                list_error['failed_test'] = 'max_size'
                list_error['error_value'] = len(input_list)
                list_error['error_code'] = 4032
                raise InputValidationError(list_error)

    # construct item error report template
        item_error = {
            'object_title': object_title,
            'model_schema': self.schema,
            'input_criteria': item_rules,
            'failed_test': 'value_datatype',
            'input_path': initial_key,
            'error_value': None,
            'error_code': 4001
        }

    # validate datatype of items
        for i in range(len(input_list)):
            input_path = path_to_root + '[%s]' % i
            item = input_list[i]
            item_error['input_path'] = input_path
            try:
                item_index = self._datatype_classes.index(item.__class__)
            except:
                item_error['error_value'] = item.__class__.__name__
                raise InputValidationError(item_error)
            item_type = self._datatype_names[item_index]
            item_error['error_value'] = item
            if item_rules['value_datatype'] == 'null':
                pass
            else:
                if item_type != item_rules['value_datatype']:
                    raise InputValidationError(item_error)

    # call appropriate validation sub-routine for datatype of item
                if item_type == 'boolean':
                    input_list[i] = self._validate_boolean(item, input_path, object_title)
                elif item_type == 'number':
                    input_list[i] = self._validate_number(item, input_path, object_title)
                elif item_type == 'string':
                    input_list[i] = self._validate_string(item, input_path, object_title)
                elif item_type == 'map':
                    input_list[i] = self._validate_dict(item, schema_list[0], input_path, object_title)
                elif item_type == 'list':
                    input_list[i] = self._validate_list(item, schema_list[0], input_path, object_title)

    # validate unique values in list
        if 'unique_values' in list_rules.keys():
            if len(set(input_list)) < len(input_list):
                list_error['failed_test'] = 'unique_values'
                list_error['error_value'] = input_list
                list_error['error_code'] = 4033
                raise InputValidationError(list_error)

    # TODO: validate top-level item values against identical to reference

    # TODO: run lambda function and call validation url

        return input_list

    def _validate_number(self, input_number, path_to_root, object_title=''):

        '''
            a helper method for validating properties of a number

        :return: input_number
        '''

        rules_path_to_root = re.sub('\[\d+\]', '[0]', path_to_root)
        input_criteria = self.keyMap[rules_path_to_root]
        error_dict = {
            'object_title': object_title,
            'model_schema': self.schema,
            'input_criteria': input_criteria,
            'failed_test': 'value_datatype',
            'input_path': path_to_root,
            'error_value': input_number,
            'error_code': 4001
        }
        if 'integer_data' in input_criteria.keys():
            if input_criteria['integer_data'] and not isinstance(input_number, int):
                error_dict['failed_test'] = 'integer_data'
                error_dict['error_code'] = 4021
                raise InputValidationError(error_dict)
        if 'min_value' in input_criteria.keys():
            if input_number < input_criteria['min_value']:
                error_dict['failed_test'] = 'min_value'
                error_dict['error_code'] = 4022
                raise InputValidationError(error_dict)
        if 'max_value' in input_criteria.keys():
            if input_number > input_criteria['max_value']:
                error_dict['failed_test'] = 'max_value'
                error_dict['error_code'] = 4023
                raise InputValidationError(error_dict)
        if 'greater_than' in input_criteria.keys():
            if input_number <= input_criteria['greater_than']:
                error_dict['failed_test'] = 'greater_than'
                error_dict['error_code'] = 4024
                raise InputValidationError(error_dict)
        if 'less_than' in input_criteria.keys():
            if input_number >= input_criteria['less_than']:
                error_dict['failed_test'] = 'less_than'
                error_dict['error_code'] = 4025
                raise InputValidationError(error_dict)
        if 'equal_to' in input_criteria.keys():
            if input_number != input_criteria['equal_to']:
                error_dict['failed_test'] = 'equal_to'
                error_dict['error_code'] = 4026
                raise InputValidationError(error_dict)
        if 'discrete_values' in input_criteria.keys():
            if input_number not in input_criteria['discrete_values']:
                error_dict['failed_test'] = 'discrete_values'
                error_dict['error_code'] = 4041
                raise InputValidationError(error_dict)
        if 'excluded_values' in input_criteria.keys():
            if input_number in input_criteria['excluded_values']:
                error_dict['failed_test'] = 'excluded_values'
                error_dict['error_code'] = 4042
                raise InputValidationError(error_dict)

    # TODO: validate number against identical to reference

    # TODO: run lambda function and call validation url

        return input_number

    def _validate_string(self, input_string, path_to_root, object_title=''):

        '''
            a helper method for validating properties of a string

        :return: input_string
        '''

        rules_path_to_root = re.sub('\[\d+\]', '[0]', path_to_root)
        input_criteria = self.keyMap[rules_path_to_root]
        error_dict = {
            'object_title': object_title,
            'model_schema': self.schema,
            'input_criteria': input_criteria,
            'failed_test': 'value_datatype',
            'input_path': path_to_root,
            'error_value': input_string,
            'error_code': 4001
        }
        if 'byte_data' in input_criteria.keys():
            if input_criteria['byte_data']:
                error_dict['failed_test'] = 'byte_data'
                error_dict['error_code'] = 4011
                try:
                    decoded_bytes = b64decode(input_string)
                except:
                    raise InputValidationError(error_dict)
                if not isinstance(decoded_bytes, bytes):
                    raise InputValidationError(error_dict)
        if 'min_value' in input_criteria.keys():
            if input_string < input_criteria['min_value']:
                error_dict['failed_test'] = 'min_value'
                error_dict['error_code'] = 4022
                raise InputValidationError(error_dict)
        if 'max_value' in input_criteria.keys():
            if input_string > input_criteria['max_value']:
                error_dict['failed_test'] = 'max_value'
                error_dict['error_code'] = 4023
                raise InputValidationError(error_dict)
        if 'greater_than' in input_criteria.keys():
            if input_string <= input_criteria['greater_than']:
                error_dict['failed_test'] = 'greater_than'
                error_dict['error_code'] = 4024
                raise InputValidationError(error_dict)
        if 'less_than' in input_criteria.keys():
            if input_string >= input_criteria['less_than']:
                error_dict['failed_test'] = 'less_than'
                error_dict['error_code'] = 4025
                raise InputValidationError(error_dict)
        if 'equal_to' in input_criteria.keys():
            if input_string != input_criteria['equal_to']:
                error_dict['failed_test'] = 'equal_to'
                error_dict['error_code'] = 4026
                raise InputValidationError(error_dict)
        if 'min_length' in input_criteria.keys():
            if len(input_string) < input_criteria['min_length']:
                error_dict['failed_test'] = 'min_length'
                error_dict['error_code'] = 4012
                raise InputValidationError(error_dict)
        if 'max_length' in input_criteria.keys():
            if len(input_string) > input_criteria['max_length']:
                error_dict['failed_test'] = 'max_length'
                error_dict['error_code'] = 4013
                raise InputValidationError(error_dict)
        if 'must_not_contain' in input_criteria.keys():
            patterns = input_criteria['must_not_contain']
            if isinstance(input_criteria['must_not_contain'], dict):
                patterns = input_criteria['must_not_contain'].keys()
            for regex in patterns:
                regex_pattern = re.compile(regex)
                if regex_pattern.findall(input_string):
                    error_dict['failed_test'] = 'must_not_contain'
                    error_dict['failed_match'] = regex
                    error_dict['error_code'] = 4014
                    raise InputValidationError(error_dict)
        if 'must_contain' in input_criteria.keys():
            patterns = input_criteria['must_contain']
            if isinstance(input_criteria['must_contain'], dict):
                patterns = input_criteria['must_contain'].keys()
            for regex in patterns:
                regex_pattern = re.compile(regex)
                if not regex_pattern.findall(input_string):
                    error_dict['failed_test'] = 'must_contain'
                    error_dict['failed_match'] = regex
                    error_dict['error_code'] = 4015
                    raise InputValidationError(error_dict)
        if 'contains_either' in input_criteria.keys():
            regex_match = False
            patterns = input_criteria['contains_either']
            if isinstance(input_criteria['contains_either'], dict):
                patterns = input_criteria['contains_either'].keys()
            for regex in patterns:
                regex_pattern = re.compile(regex)
                if regex_pattern.findall(input_string):
                    regex_match = True
            if not regex_match:
                error_dict['failed_test'] = 'contains_either'
                error_dict['error_code'] = 4016
                raise InputValidationError(error_dict)
        if 'discrete_values' in input_criteria.keys():
            if input_string not in input_criteria['discrete_values']:
                error_dict['failed_test'] = 'discrete_values'
                error_dict['error_code'] = 4041
                raise InputValidationError(error_dict)
        if 'excluded_values' in input_criteria.keys():
            if input_string in input_criteria['excluded_values']:
                error_dict['failed_test'] = 'excluded_values'
                error_dict['error_code'] = 4042
                raise InputValidationError(error_dict)

    # TODO: validate string against identical to reference

    # TODO: run lambda function and call validation url

        return input_string

    def _validate_boolean(self, input_boolean, path_to_root, object_title=''):

        '''
            a helper method for validating properties of a boolean

        :return: input_boolean
        '''

        rules_path_to_root = re.sub('\[\d+\]', '[0]', path_to_root)
        input_criteria = self.keyMap[rules_path_to_root]
        error_dict = {
            'object_title': object_title,
            'model_schema': self.schema,
            'input_criteria': input_criteria,
            'failed_test': 'value_datatype',
            'input_path': path_to_root,
            'error_value': input_boolean,
            'error_code': 4001
        }
        if 'equal_to' in input_criteria.keys():
            if input_boolean != input_criteria['equal_to']:
                error_dict['failed_test'] = 'equal_to'
                error_dict['error_code'] = 4026
                raise InputValidationError(error_dict)

    # TODO: validate boolean against identical to reference

    # TODO: run lambda function and call validation url

        return input_boolean

    def _ingest_dict(self, input_dict, schema_dict, path_to_root):

        '''
            a helper method for ingesting keys, value pairs in a dictionary

        :return: valid_dict
        '''

        valid_dict = {}

    # construct path to root for rules
        rules_path_to_root = re.sub('\[\d+\]', '[0]', path_to_root)

    # iterate over keys in schema dict
        for key, value in schema_dict.items():
            key_path = path_to_root
            if not key_path == '.':
                key_path += '.'
            key_path += key
            rules_key_path = re.sub('\[\d+\]', '[0]', key_path)
            value_match = False
            if key in input_dict.keys():
                value_index = self._datatype_classes.index(value.__class__)
                value_type = self._datatype_names[value_index]
                try:
                    v_index = self._datatype_classes.index(input_dict[key].__class__)
                    v_type = self._datatype_names[v_index]
                    if v_type == value_type:
                        value_match = True
                except:
                    value_match = False
            if value_match:
                if value_type == 'null':
                    valid_dict[key] = input_dict[key]
                elif value_type == 'boolean':
                    valid_dict[key] = self._ingest_boolean(input_dict[key], key_path)
                elif value_type == 'number':
                    valid_dict[key] = self._ingest_number(input_dict[key], key_path)
                elif value_type == 'string':
                    valid_dict[key] = self._ingest_string(input_dict[key], key_path)
                elif value_type == 'map':
                    valid_dict[key] = self._ingest_dict(input_dict[key], schema_dict[key], key_path)
                elif value_type == 'list':
                    valid_dict[key] = self._ingest_list(input_dict[key], schema_dict[key], key_path)
            else:
                value_type = self.keyMap[rules_key_path]['value_datatype']
                if 'default_value' in self.keyMap[rules_key_path]:
                    valid_dict[key] = self.keyMap[rules_key_path]['default_value']
                elif value_type == 'null':
                    valid_dict[key] = None
                elif value_type == 'boolean':
                    valid_dict[key] = False
                elif value_type == 'number':
                    valid_dict[key] = 0.0
                    if 'integer_data' in self.keyMap[rules_key_path].keys():
                        if self.keyMap[rules_key_path]['integer_data']:
                            valid_dict[key] = 0
                elif value_type == 'string':
                    valid_dict[key] = ''
                elif value_type == 'list':
                    valid_dict[key] = []
                elif value_type == 'map':
                    valid_dict[key] = self._ingest_dict({}, schema_dict[key], key_path)

    # add extra fields if set to True
        if self.keyMap[rules_path_to_root]['extra_fields']:
            for key, value in input_dict.items():
                if key not in valid_dict.keys():
                    valid_dict[key] = value

        return valid_dict

    def _ingest_list(self, input_list, schema_list, path_to_root):

        '''
            a helper method for ingesting items in a list

        :return: valid_list
        '''

        valid_list = []

    # construct max list size
        max_size = None
        rules_path_to_root = re.sub('\[\d+\]', '[0]', path_to_root)
        if 'max_size' in self.keyMap[rules_path_to_root].keys():
            if not self.keyMap[rules_path_to_root]['max_size']:
                return valid_list
            else:
                max_size = self.keyMap[rules_path_to_root]['max_size']

    # iterate over items in input list
        if input_list:
            rules_index = self._datatype_classes.index(schema_list[0].__class__)
            rules_type = self._datatype_names[rules_index]
            for i in range(len(input_list)):
                item_path = '%s[%s]' % (path_to_root, i)
                value_match = False
                try:
                    item_index = self._datatype_classes.index(input_list[i].__class__)
                    item_type = self._datatype_names[item_index]
                    if item_type == rules_type:
                        value_match = True
                except:
                    value_match = False
                if value_match:
                    try:
                        if item_type == 'boolean':
                            valid_list.append(self._validate_boolean(input_list[i], item_path))
                        elif item_type == 'number':
                            valid_list.append(self._validate_number(input_list[i], item_path))
                        elif item_type == 'string':
                            valid_list.append(self._validate_string(input_list[i], item_path))
                        elif item_type == 'map':
                            valid_list.append(self._ingest_dict(input_list[i], schema_list[0], item_path))
                        elif item_type == 'list':
                            valid_list.append(self._ingest_list(input_list[i], schema_list[0], item_path))
                    except:
                        pass
                if isinstance(max_size, int):
                    if len(valid_list) == max_size:
                        return valid_list

        return valid_list

    def _ingest_number(self, input_number, path_to_root):

        '''
            a helper method for ingesting a number

        :return: valid_number
        '''

        valid_number = 0.0

        try:
            valid_number = self._validate_number(input_number, path_to_root)
        except:
            rules_path_to_root = re.sub('\[\d+\]', '[0]', path_to_root)
            if 'default_value' in self.keyMap[rules_path_to_root]:
                valid_number = self.keyMap[rules_path_to_root]['default_value']
            elif 'integer_data' in self.keyMap[rules_path_to_root].keys():
                if self.keyMap[rules_path_to_root]['integer_data']:
                    valid_number = 0

        return valid_number

    def _ingest_string(self, input_string, path_to_root):

        '''
            a helper method for ingesting a string

        :return: valid_string
        '''

        valid_string = ''

        try:
            valid_string = self._validate_string(input_string, path_to_root)
        except:
            rules_path_to_root = re.sub('\[\d+\]', '[0]', path_to_root)
            if 'default_value' in self.keyMap[rules_path_to_root]:
                valid_string = self.keyMap[rules_path_to_root]['default_value']

        return valid_string

    def _ingest_boolean(self, input_boolean, path_to_root):

        '''
            a helper method for ingesting a boolean

        :return: valid_boolean
        '''

        valid_boolean = False

        try:
            valid_boolean = self._validate_boolean(input_boolean, path_to_root)
        except:
            rules_path_to_root = re.sub('\[\d+\]', '[0]', path_to_root)
            if 'default_value' in self.keyMap[rules_path_to_root]:
                valid_boolean = self.keyMap[rules_path_to_root]['default_value']

        return valid_boolean

    def _reconstruct(self, path_to_root):

        '''
            a helper method for finding the schema endpoint from a path to root

        :param path_to_root: string with dot path to root from
        :return: list, dict, string, number, or boolean at path to root
        '''

    # split path to root into segments
        item_pattern = re.compile('\d+\\]')
        dot_pattern = re.compile('\\.|\\[')
        path_segments = dot_pattern.split(path_to_root)

    # construct base schema endpoint
        schema_endpoint = self.schema

    # reconstruct schema endpoint from segments
        if path_segments[1]:
            for i in range(1,len(path_segments)):
                if item_pattern.match(path_segments[i]):
                    schema_endpoint = schema_endpoint[0]
                else:
                    schema_endpoint = schema_endpoint[path_segments[i]]

        return schema_endpoint

    def _walk(self, path_to_root, record_dict):

        '''
            a helper method for finding the record endpoint from a path to root

        :param path_to_root: string with dot path to root from
        :param record_dict:
        :return: list, dict, string, number, or boolean at path to root
        '''

    # split path to root into segments
        item_pattern = re.compile('\d+\\]')
        dot_pattern = re.compile('\\.|\\[')
        path_segments = dot_pattern.split(path_to_root)

    # construct empty fields
        record_endpoints = []

    # determine starting position
        if not path_segments[0]:
            path_segments.pop(0)
        
    # define internal recursive function
        def _walk_int(path_segments, record_dict):
            record_endpoint = record_dict
            for i in range(0, len(path_segments)):
                if item_pattern.match(path_segments[i]):
                    for j in range(0, len(record_endpoint)):
                        if len(path_segments) == 2:
                            record_endpoints.append(record_endpoint[j])
                        else:
                            stop_chain = False
                            for x in range(0, i):
                                if item_pattern.match(path_segments[x]):
                                    stop_chain = True
                            if not stop_chain:
                                shortened_segments = []
                                for z in range(i + 1, len(path_segments)):
                                    shortened_segments.append(path_segments[z])
                                _walk_int(shortened_segments, record_endpoint[j])
                else:
                    stop_chain = False
                    for y in range(0, i):
                        if item_pattern.match(path_segments[y]):
                            stop_chain = True
                    if not stop_chain:
                        if len(path_segments) == i + 1:
                            record_endpoints.append(record_endpoint[path_segments[i]])
                        else:
                            record_endpoint = record_endpoint[path_segments[i]]

    # conduct recursive walk
        _walk_int(path_segments, record_dict)

        return record_endpoints

    def validate(self, input_data, path_to_root='', object_title=''):

        '''
            a core method for validating input against the model

            input_data is only returned if all data is valid

        :param input_data: list, dict, string, number, or boolean to validate
        :param path_to_root: [optional] string with dot-path of model component
        :param object_title: [optional] string with name of input to validate
        :return: input_data (or InputValidationError)
        '''

        __name__ = '%s.validate' % self.__class__.__name__
        _path_arg = '%s(path_to_root="...")' % __name__
        _title_arg = '%s(object_title="...")' % __name__

    # validate input
        copy_path = path_to_root
        if path_to_root:
            if not isinstance(path_to_root, str):
                raise ModelValidationError('%s must be a string.' % _path_arg)
            else:
                if path_to_root[0] != '.':
                    copy_path = '.%s' % path_to_root
                if not copy_path in self.keyMap.keys():
                    raise ModelValidationError('%s does not exist in components %s.' % (_path_arg.replace('...', path_to_root), self.keyMap.keys()))
        else:
            copy_path = '.'
        if object_title:
            if not isinstance(object_title, str):
                raise ModelValidationError('%s must be a string' % _title_arg)

    # construct generic error dictionary
        error_dict = {
            'object_title': object_title,
            'model_schema': self.schema,
            'input_criteria': self.keyMap[copy_path],
            'failed_test': 'value_datatype',
            'input_path': copy_path,
            'error_value': input_data,
            'error_code': 4001
        }

    # determine value type of input data
        try:
            input_index = self._datatype_classes.index(input_data.__class__)
        except:
            error_dict['error_value'] = input_data.__class__.__name__
            raise InputValidationError(error_dict)
        input_type = self._datatype_names[input_index]

    # validate input data type
        if input_type != self.keyMap[copy_path]['value_datatype']:
            raise InputValidationError(error_dict)

    # run helper method appropriate to data type
        if input_type == 'boolean':
            input_data = self._validate_boolean(input_data, copy_path, object_title)
        elif input_type == 'number':
            input_data = self._validate_number(input_data, copy_path, object_title)
        elif input_type == 'string':
            input_data = self._validate_string(input_data, copy_path, object_title)
        elif input_type == 'list':
            schema_list = self._reconstruct(copy_path)
            input_data = self._validate_list(input_data, schema_list, copy_path, object_title)
        elif input_type == 'map':
            schema_dict = self._reconstruct(copy_path)
            input_data = self._validate_dict(input_data, schema_dict, copy_path, object_title)

        return input_data

    def ingest(self, **kwargs):

        '''
            a core method to ingest and validate arbitrary keyword data

            **NOTE: data is always returned with this method**

            for each key in the model, a value is returned according
             to the following priority:

                1. value in kwargs if field passes validation test
                2. default value declared for the key in the model
                3. empty value appropriate to datatype of key in the model

            **NOTE: as long as a default value is provided for each key-
             value, returned data will be model valid

            **NOTE: if 'extra_fields' is True for a dictionary, the key-
             value pair of all fields in kwargs which are not declared in
             the model will also be added to the corresponding dictionary
             data

            **NOTE: if 'max_size' is declared for a list, method will
             stop adding input to the list once it reaches max size

        :param kwargs: key, value pairs
        :return: dictionary with keys and value
        '''

        __name__ = '%s.ingest' % self.__class__.__name__

        schema_dict = self.schema
        path_to_root = '.'

        valid_data = self._ingest_dict(kwargs, schema_dict, path_to_root)

        return valid_data

    def query(self, query_criteria, valid_record=None):

        '''
            a core method for querying model valid data with criteria

            **NOTE: input is only returned if all fields & qualifiers are valid for model

            :param query_criteria: dictionary with model field names and query qualifiers
            :param valid_record: dictionary with model valid record
            :return: boolean (or QueryValidationError)

            an example of how to construct the query_criteria argument:

            query_criteria = {
                '.path.to.number': {
                    'min_value': 4.5
                },
                '.path.to.string': {
                    'must_contain': [ '\\regex' ]
                }
            }

            **NOTE: for a full list of operators for query_criteria based upon field
                    datatype, see either the query-rules.json file or REFERENCE file
        '''

        __name__ = '%s.query' % self.__class__.__name__
        _query_arg = '%s(query_criteria={...})' % __name__
        _record_arg = '%s(valid_record={...})' % __name__

    # validate input
        if not isinstance(query_criteria, dict):
            raise ModelValidationError('%s must be a dictionary.' % _query_arg)

    # convert javascript dot_path to class dot_path
        criteria_copy = {}
        equal_fields = []
        dot_fields = []
        for key, value in query_criteria.items():
            copy_key = key
            if not key:
                copy_key = '.'
            else:
                if key[0] != '.':
                    copy_key = '.%s' % key
                    dot_fields.append(copy_key)
            criteria_copy[copy_key] = value

            # allow equal to value of strings, numbers and booleans to be declared directly
            if value.__class__ in self._datatype_classes[0:4]:
                criteria_copy[copy_key] = {
                    'equal_to': value
                }
                equal_fields.append(copy_key)

    # validate query criteria against query rules
        query_kwargs = {
            'fields_dict': criteria_copy,
            'fields_rules': self.queryRules,
            'declared_value': False
        }
        try:
            self._validate_fields(**query_kwargs)
        except ModelValidationError as err:
            message = err.error['message']
            for field in equal_fields:
                equal_error = 'field %s qualifier equal_to' % field
                if message.find(equal_error) > -1:
                    message = message.replace(equal_error, 'field %s' % field)
                    break
            field_pattern = re.compile('ield\s(\..*?)\s')
            field_name = field_pattern.findall(message)
            if field_name:
                if field_name[0] in dot_fields:
                    def _replace_field(x):
                        return 'ield %s ' % x.group(1)[1:]
                    message = field_pattern.sub(_replace_field, message)
            raise QueryValidationError(message)

    # query test record
        if valid_record:
            if not isinstance(valid_record, dict):
                raise ModelValidationError('%s must be a dictionary.' % _record_arg)
            for key, value in criteria_copy.items():
                eval_outcome = self._evaluate_field(valid_record, key, value)
                if not eval_outcome:
                    return False

        return True
