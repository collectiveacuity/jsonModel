__author__ = 'rcj1492'
__created__ = '2016.06'
__license__ = 'MIT'

from jsonmodel.mapping import mapModel

class testMapModel(mapModel):

    def __init__(self, input):
        mapModel.__init__(self, input)

    def unitTests(self):

        assert self.keyCriteria[self.keyName.index('.')]['value_datatype'] == 'map'

        return self

if __name__ == '__main__':
    import json
    testModel = json.loads(open('../models/sample-model.json').read())
    testMapModel(testModel).unitTests()