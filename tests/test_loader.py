__author__ = 'rcj1492'
__created__ = '2016.03'
__license__ = 'MIT'

import pytest
from jsonmodel import __module__
from jsonmodel.loader import jsonLoader

class jsonLoaderTests(object):

    def __init__(self):
        pass

    def unitTests(self):

    # test invalid module exception
        with pytest.raises(Exception):
            jsonLoader('not_a_module', 'models/model-rules.json')

    # test valid relative paths
        assert jsonLoader(__module__, 'models/model-rules.json')
        assert jsonLoader(__module__, './models/model-rules.json')
        assert jsonLoader(__module__, '../samples/sample-model.json')

    # test invalid relative path exception
        with pytest.raises(Exception):
            jsonLoader(__module__, './sample-model.json')

    # test invalid absolute path exception
        with pytest.raises(Exception):
            jsonLoader(__module__, '/model-rules.json')

    # test invalid file type exception
        with pytest.raises(Exception):
            jsonLoader(__module__, 'loader.py')

        return self

if __name__ == '__main__':
    jsonLoaderTests().unitTests()