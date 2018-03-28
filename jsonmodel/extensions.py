''' a package of extensions to a jsonModel class object '''
__author__ = 'rcj1492'
__created__ = '2018.03'
__license__ = 'MIT'

def tabulate(json_model):
    
    '''
        a function to add the tabulate method to a jsonModel object
        
    :param json_model: jsonModel object
    :return: jsonModel object
    '''

    import types
    from jsonmodel._extensions import tabulate as _tabulate
    try:
        from tabulate import tabulate
    except:
        import sys
        print('jsonmodel.extensions.tabulate requires the tabulate module. try: pip install tabulate')
        sys.exit(1)

    setattr(json_model, 'tabulate', _tabulate.__get__(json_model, types.MethodType))

    return json_model

if __name__ == '__main__':
    
    from jsonmodel import __module__
    from jsonmodel.loader import jsonLoader
    from jsonmodel.validators import jsonModel
    
    model_rules = jsonLoader(__module__, '../samples/sample-model.json')
    model_rules['components']['.']['extra_fields'] = True
    model_rules['components']['.datetime']['field_description'] = 'https://collectiveacuity.com'
    rules_model = jsonModel(model_rules)
    rules_model = tabulate(rules_model)
    
    documentation = rules_model.tabulate(syntax='javascript')
    with open('../docs/test.md', 'wt') as f:
        f.write(documentation)
        f.close()
