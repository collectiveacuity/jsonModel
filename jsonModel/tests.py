__author__ = 'rcj1492'
__created__ = '2016.01'

import json
from jsonmodel.validators import jsonModel

testModel = json.loads(open('../models/sample-model.json').read())
testInput = json.loads(open('../models/sample-input.json').read())
jsonModel(testModel).unitTests(testInput)