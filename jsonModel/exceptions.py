__author__ = 'rcj1492'
__created__ = '2016.01'

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