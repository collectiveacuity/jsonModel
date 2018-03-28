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
        self.error = {
            'object_title': '',
            'model_schema': {},
            'input_criteria': {},
            'failed_test': '',
            'input_path': '',
            'error_value': None,
            'error_code': 0
        }
        if isinstance(error_dict, dict):
            if 'object_title' in error_dict:
                self.error['object_title'] = error_dict['object_title']
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
        if self.error['object_title']:
            failed_test = self.error['failed_test']
            first_line = '\n%s is invalid.' % (self.error['object_title'].rstrip())
            second_line = "\nValue %s for field %s failed test '%s'" % (self.error['error_value'], self.error['input_path'], failed_test)
            if failed_test in self.error['input_criteria']:
                if failed_test == 'required_field':
                    second_line += ': True'
                else:
                    second_line += ': %s' % self.error['input_criteria'][failed_test]
            self.message = '%s%s' % (first_line, second_line)
        else:
            self.message = '\nError Report: %s' % self.error
        super(InputValidationError, self).__init__(self.message)