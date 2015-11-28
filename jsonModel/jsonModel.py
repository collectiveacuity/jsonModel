__author__ = 'rcj1492'
__created__ = '2015.11'

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

class jsonModel(object):

    def __init__(self):
        pass

    def validate(self, input_dict):
        return input_dict
