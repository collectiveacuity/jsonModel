''' a package of exception classes '''
__author__ = 'rcj1492'
__created__ = '2016.01'
__license__ = 'MIT'

class ModelValidationError(Exception):

    def __init__(self, message='', error_dict=None):
        text = '\nModel declaration is invalid.\n%s' % message
        self.error = {
            'message': message
        }
        if error_dict:
            if isinstance(error_dict, dict):
                self.error = error_dict
        super(ModelValidationError, self).__init__(text)

class QueryValidationError(Exception):

    def __init__(self, message='', error_dict=None):
        text = '\nQuery declaration is invalid.\n%s' % message
        self.error = {
            'message': message
        }
        if error_dict:
            if isinstance(error_dict, dict):
                self.error = error_dict
        super(QueryValidationError, self).__init__(text)

class InputValidationError(Exception):
    ''' a class for reporting jsonmodel input validation errors '''
    def __init__(self, error_dict=None):
    
        # construct default error property
        self.error = {
            'object_title': '',
            'model_schema': {},
            'input_criteria': {},
            'failed_test': '',
            'input_path': '',
            'error_value': None,
            'error_code': 0
        }

        # add values from args to error property
        if isinstance(error_dict, dict):
            if 'object_title' in error_dict:
                self.error['object_title'] = error_dict['object_title']
            if 'model_schema' in error_dict:
                self.error['model_schema'] = error_dict['model_schema']
            if 'input_criteria' in error_dict:
                self.error['input_criteria'] = error_dict['input_criteria']
            if 'failed_test' in error_dict:
                self.error['failed_test'] = error_dict['failed_test']
            if 'failed_match' in error_dict:
                self.error['failed_match'] = error_dict['failed_match']
            if 'input_path' in error_dict:
                self.error['input_path'] = error_dict['input_path']
            if 'error_value' in error_dict:
                self.error['error_value'] = error_dict['error_value']
            if 'error_code' in error_dict:
                self.error['error_code'] = error_dict['error_code']

        # compose message
        if self.error['object_title']:
            failed_test = self.error['failed_test']
            first_line = '\n%s is invalid.' % (self.error['object_title'].rstrip())
            second_line = "\nValue %s for field %s failed test '%s'" % (self.error['error_value'], self.error['input_path'], failed_test)
            if failed_test in self.error['input_criteria']:
                if failed_test == 'required_field':
                    second_line += ': True'
                elif failed_test in ('must_contain','must_not_contain','contains_either') and isinstance(self.error['input_criteria'][failed_test], dict):
                    second_line += ': %s' % list(self.error['input_criteria'][failed_test].keys())
                else:
                    second_line += ': %s' % self.error['input_criteria'][failed_test]
            self.message = '%s%s' % (first_line, second_line)
        else:
            self.message = '\nError Report: %s' % self.error

        super(InputValidationError, self).__init__(self.message)

    def explain(self):

        # retrieve variables from report
        test = self.error['failed_test']
        value = self.error['input_criteria'][test]
        error = self.error['error_value']
        datatype = self.error['input_criteria']['value_datatype']
        field = self.error['input_path'][1:]

        # define disjunction script
        def conjoin(words, truncate=0, junction='or'):
            text = ''
            for i in range(len(words)):
                if text:
                    if i + 1 == len(words):
                        text += ' %s ' % junction
                    else:
                        text += ', '
                if isinstance(words[i], str):
                    text += words[i][truncate:]
                else:
                    text += str(words[i])
            return text

        # construct default explanation
        explanation = '%s must be %s' % (test, value)

        # generate explanation for missing or extra fields
        if test in ('required_field'):
            explanation = 'is missing required field %s' % error[0][1:]
            if field:
                truncate = len(field) + 2
                subfield = error[0][truncate:]
                explanation = 'is missing required sub-field %s' % subfield
        elif test in ('extra_fields'):
            plural = ''
            if len(error) > 1:
                plural = 's'
            explanation = 'may not contain field%s %s' % (plural, conjoin(error, truncate=1))
            if field:
                truncate = len(field) + 2
                explanation = 'may not contain sub-field%s %s' % (plural, conjoin(error, truncate=truncate))
        elif test in ('key_datatype'):
            explanation = 'datatype of key must be a %s' % value

        # generate explanation for map and list fields
        elif test in ('min_size'):
            if datatype == 'map':
                explanation = 'must be at least %s characters long when converted to a string' % value
                if value == 1:
                    explanation = 'may not be empty'
            elif datatype == 'list':
                explanation = 'must have at least %s items' % value
                if value == 1:
                    explanation = 'may not be empty'
        elif test in ('max_size'):
            if datatype == 'map':
                explanation = 'may not be longer than %s characters when converted to a string' % value
                if value == 1:
                    explanation = 'may only be 1 character long when converted to a string'
            elif datatype == 'list':
                explanation = 'may not have more than %s items' % value
                if value == 1:
                    explanation = 'may only have 1 item'
        elif test in ('unique_values'):
            explanation = 'must contain unique values'

        # generate explanation for invalid string, number and boolean fields
        elif test in ('value_datatype'):
            explanation = 'must be a %s' % value
            if value == 'null':
                explanation = 'must be null'
            elif 'integer_data' in self.error['input_criteria'].keys():
                if self.error['input_criteria']['integer_data']:
                    explanation = 'must be an integer'
        elif test in ('integer_data'):
            explanation = 'must be an integer'
        elif test in ('byte_data'):
            explanation = 'must be byte data encoded as a base64 string'
        elif test in ('max_value'):
            explanation = 'must be no greater than %s' % value
            if datatype == 'string':
                explanation = 'must not fall after %s in alphanumeric order' % value
        elif test in ('min_value'):
            explanation = 'must be no less than %s' % value
            if datatype == 'string':
                explanation = 'must not come before %s in alphanumeric order' % value
        elif test in ('equal_to'):
            explanation = 'must equal %s' % value
            if datatype in ('boolean'):
                explanation = 'must equal %s' % str(value).lower() 
        elif test in ('greater_than'):
            explanation = 'must be greater than %s' % value
            if datatype == 'string':
                explanation = 'must fall after %s in alphanumeric order' % value
        elif test in ('less_than'):
            explanation = 'must be less than %s' % value
            if datatype == 'string':
                explanation = 'must come before %s in alphanumeric order' % value
        elif test in ('min_length'):
            explanation = 'must be at least %s characters long' % value
            if value == 1:
                explanation = 'may not be empty'
        elif test in ('max_length'):
            explanation = 'may not be longer than %s characters' % value
            if value == 1:
                explanation = 'may only be 1 character long'
        elif test in ('discrete_values'):
            explanation = 'must be either %s' % conjoin(value)
            if len(value) == 1:
                explanation = 'must be %s' % value[0]
        elif test in ('excluded_values'):
            explanation = 'can be neither %s' % conjoin(value, junction='nor')
            if len(value) == 1:
                explanation = 'cannot be %s' % value[0]
        elif test in ('must_not_contain'):
            if isinstance(value, dict):
                failed_match = self.error['failed_match']
                explanation = value[failed_match]
            else:
                explanation = 'can match neither regex patterns %s' % conjoin(value, junction='nor')
                if len(value) == 1:
                    explanation = 'cannot match regex pattern %s' % value[0]
        elif test in ('must_contain'):
            if isinstance(value, dict):
                failed_match = self.error['failed_match']
                explanation = value[failed_match]
            else:
                explanation = 'must match regex patterns %s' % conjoin(value, junction='and')
                if len(value) == 1:
                    explanation = 'must match regex pattern %s' % value[0]
        elif test in ('contains_either'):
            if isinstance(value, dict):
                matches = []
                for k, v in value.items():
                    matches.append(v)
                explanation = 'either %s' % conjoin(matches)
                if len(matches) == 1:
                    explanation = matches[0] 
            else:
                explanation = 'must match either regex patterns %s' % conjoin(value)
                if len(value) == 1:
                    explanation = 'must match regex pattern %s' % value[0]

        return explanation