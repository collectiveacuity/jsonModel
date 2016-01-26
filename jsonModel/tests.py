__author__ = 'rcj1492'
__created__ = '2016.01'

from jsonModel.classes import jsonModel, json

testModel = json.loads(open('../models/sample-model.json').read())
testInput = json.loads(open('../models/sample-input.json').read())
jsonModel(testModel).unitTests(testInput)