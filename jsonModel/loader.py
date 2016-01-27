__author__ = 'rcj1492'
__created__ = '2016.01'

import json
from re import compile
from os import path
from importlib.util import find_spec

def jsonLoader(module_name, file_path):
    file_type = compile('\.json$')
    leading_slash = compile('/')
    if not file_type.findall(file_path):
        raise Exception('%s must be a .json file type' % file_path)
    elif not leading_slash.match(file_path):
        file_path = '/%s' % file_path
    module_path = find_spec(module_name).submodule_search_locations[0]
    json_path = module_path + file_path
    if not path.isfile(json_path):
        raise Exception('%s is not a valid module path.' % json_path)
    model_dict = json.loads(open(json_path).read())
    return model_dict