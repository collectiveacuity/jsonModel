''' a package of extensions to a jsonModel class object '''
__author__ = 'rcj1492'
__created__ = '2018.03'
__license__ = 'MIT'

def document(json_model):
    
    '''
        a function to add a document method to a jsonModel object
        
    :param json_model: jsonModel object
    :return: jsonModel object
    '''

    import re
    import types
    try:
        from tabulate import tabulate
    except:
        import sys
        print('jsonmodel.extensions.document requires the tabulate module. try: pip install tabulate')
        sys.exit(1)

    def _segment_path(dot_path):
        import re
        digit_pat = re.compile('\[(\d+)\]')
        key_list = dot_path.split('.')
        segment_list = []
        for key in key_list:
            if key:
                item_list = digit_pat.split(key)
                for item in item_list:
                    if item:
                        segment_list.append(item)
        return segment_list
    
    def _replace_url(x):
        url_text = '<a href="%s">%s</a>' % (x.group(1), x.group(0))
        return url_text
    
    def _document(self, format='markdown', syntax=''):

        '''
            a function to create documentation from the class model

        :param format: string with format for documentation output
        :param syntax: [optional] string with linguistic syntax
        :return: string with documentation
        '''

    # define headers
        headers = ['Field', 'Datatype', 'Required', 'Default', 'Examples', 'Conditions']
        rows = []
        default_values = False
        additional_conditions = False
    
    # construct rows
        for key, value in self.keyMap.items():

            key_segments = _segment_path(key)
            print(key_segments)

            if key_segments:
                row = []

            # add field column
                field_name = ''
                if len(key_segments) > 1:
                    for i in range(1,len(key_segments)):
                        field_name += '&nbsp;&nbsp;&nbsp;&nbsp;'
                if key_segments[-1] == '0':
                    field_name += '<i>item</i>'
                else:
                    field_name += key_segments[-1]
                row.append(field_name)

            # add datatype column
                value_datatype = value['value_datatype']
                if 'integer_data' in value.keys():
                    if value['integer_data'] and syntax != 'javascript':
                        value_datatype = 'integer'
                elif value['value_datatype'] == 'map':
                    if syntax == 'javascript':
                        value_datatype = 'object'
                elif value['value_datatype'] == 'list':
                    if syntax == 'javascript':
                        value_datatype = 'array'
                # retrieve datatype of item in list
                    item_key = key + '[0]'
                    item_datatype = self.keyMap[item_key]['value_datatype']
                    if syntax == 'javascript':
                        if item_datatype == 'list':
                            item_datatype = 'array'
                        elif item_datatype == 'map':
                            item_datatype = 'object'
                    elif 'integer_data' in self.keyMap[item_key].keys():
                        if self.keyMap[item_key]['integer_data']:
                            item_datatype = 'integer'
                    value_datatype += ' of %ss' % item_datatype
                row.append(value_datatype)

            # add required column
                if value['required_field']:
                    row.append('yes')
                else:
                    row.append('')

            # add default column
                if 'default_value' in value.keys():
                    default_values = True
                    if isinstance(value['default_value'], str):
                        row.append('"%s"' % value['default_value'])
                    elif isinstance(value['default_value'], bool):
                        row.append(str(value['default_value']).lower())
                    else:
                        row.append(str(value['default_value']))
                else:
                    row.append('')

            # define recursive example constructor
                def determine_example(k, v):
                    example_value = ''
                    if 'example_values' in v.keys():
                        for i in v['example_values']:
                            if example_value:
                                example_value += ', '
                            if isinstance(i, str):
                                example_value += '"%s"' % i
                            else:
                                example_value += value
                    elif 'declared_value' in v.keys():
                        if isinstance(v['declared_value'], str):
                            example_value = '"%s"' % v['declared_value']
                        elif isinstance(v['declared_value'], bool):
                            example_value = str(v['declared_value']).lower()
                        else:
                            example_value = v['declared_value']
                    else:
                        if v['value_datatype'] == 'map':
                            example_value = '{...}'
                        elif v['value_datatype'] == 'list':
                            item_key = k + '[0]'
                            example_value = '[ %s ]' % determine_example(item_key, self.keyMap[item_key])
                        elif v['value_datatype'] == 'null':
                            example_value = 'null'
                    return example_value

            # add examples column
                row.append(determine_example(key, value))
                
            # add additional conditions
                conditions = ''
                for k, v in value.items():
                    extra_integer = False
                    if k == 'integer_data' and syntax == 'javascript':
                        extra_integer = True
                    if k not in ('example_values', 'value_datatype', 'required_field', 'declared_value') or extra_integer:          
                        additional_conditions = True
                        if conditions:
                            conditions += '<br>'
                        condition_value = v
                        if isinstance(v, str):
                            condition_value = '"%s"' % v
                        elif isinstance(v, bool):
                            condition_value = str(v).lower()
                        conditions += '%s: %s' % (k, condition_value)
                row.append(conditions)

                rows.append(row)

    # eliminate unused columns
        if not additional_conditions:
            headers.pop()
        if not default_values:
            headers.pop(3)
        for row in rows:
            if not additional_conditions:
                row.pop()
            if not default_values:
                row.pop(3)
    
    # construct table html
        table_html = tabulate(rows, headers, tablefmt='html')
    
    # add links to urls in text
        url_regex = re.compile('\[(.*?)\]\((.*)\)')
        table_html = url_regex.sub(_replace_url, table_html)

        print(self.keyMap)

        return table_html
        
    setattr(json_model, 'document', _document.__get__(json_model, types.MethodType))

    return json_model

if __name__ == '__main__':
    
    from jsonmodel import __module__
    from jsonmodel.loader import jsonLoader
    from jsonmodel.validators import jsonModel
    
    model_rules = jsonLoader(__module__, 'models/model-rules.json')
    del model_rules['components']
    rules_model = jsonModel(model_rules)
    rules_model = document(rules_model)
    
    
    documentation = rules_model.document(syntax='javascript')
    with open('../docs/extensions.md', 'wt') as f:
        f.write(documentation)
        f.close()
