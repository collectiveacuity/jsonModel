''' a package of helper functions for extensions.py '''
__author__ = 'rcj1492'
__created__ = '2018.03'
__license__ = 'MIT'

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

def _add_links(text_string):

    import re
    url_parts = re.compile('(([A-Za-z]{3,9}:(?://)?)(?:[\-;:&=\+\$,\w]+@)?[A-Za-z0-9.\-]+(:[0-9]+)?|(?:www.|[\-;:&=\+\$,\w]+@)[A-Za-z0-9.\-]+)((?:/[\+~%/.\w\-_]*)?\??(?:[\-\+,=&;%@.\w_]*)#?(?:[\w]*))?')
    url_pattern = re.compile('((([A-Za-z]{3,9}:(?://)?)(?:[\-;:&=\+\$,\w]+@)?[A-Za-z0-9.\-]+(:[0-9]+)?|(?:www.|[\-;:&=\+\$,\w]+@)[A-Za-z0-9.\-]+)((?:/[\+~%/.\w\-_]*)?\??(?:[\-\+,=&;%@.\w_]*)#?(?:[\w]*))?)')

    def _replace_url(x):
        url_string = x.group(0)
        if not url_parts.findall(url_string)[0][1]:
            return url_string
        url_text = '<a href="%s">%s</a>' % (url_string, url_string)
        return url_text

    return url_pattern.sub(_replace_url, text_string)

def tabulate(self, format='html', syntax=''):

    '''
        a function to create a table from the class model keyMap

    :param format: string with format for table output
    :param syntax: [optional] string with linguistic syntax
    :return: string with table
    '''

    from tabulate import tabulate as _tabulate
    
# define headers
    headers = ['Field', 'Datatype', 'Required', 'Default', 'Examples', 'Conditionals', 'Description']
    rows = []
    default_values = False
    additional_conditions = False
    field_description = False

# construct rows
    for key, value in self.keyMap.items():

        key_segments = _segment_path(key)

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
                        example_value = '[...]'
                    elif v['value_datatype'] == 'null':
                        example_value = 'null'
                return example_value

        # add examples column
            row.append(determine_example(key, value))

        # add additional conditions
            conditions = ''
            description = ''
            for k, v in value.items():
                extra_integer = False
                if k == 'integer_data' and syntax == 'javascript':
                    extra_integer = True
                if k not in ('example_values', 'value_datatype', 'required_field', 'declared_value', 'default_value', 'field_position', 'field_metadata') or extra_integer:
                    add_extra = False
                    if k == 'extra_fields':
                        if v:
                            add_extra = True
                    if k in ('field_description', 'field_title'):
                        field_description = True
                        if k == 'field_description':
                            description = v
                        elif not description:
                            description = v
                    elif k != 'extra_fields' or add_extra:
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
            row.append(description)

        # add row to rows
            rows.append(row)

# add rows for top field
    top_dict = self.keyMap['.']
    if top_dict['extra_fields']:
        rows.append(['<i>**extra fields allowed</i>', '', '', '', '', '', ''])
    if 'max_bytes' in top_dict.keys():
        rows.append(['<i>**max bytes: %s</i>' % top_dict['max_bytes'], '', '', '', '', '', ''])

# eliminate unused columns
    if not field_description:
        headers.pop()
    if not additional_conditions:
        headers.pop()
    if not default_values:
        headers.pop(3)
    for row in rows:
        if not field_description:
            row.pop()
        if not additional_conditions:
            row.pop()
        if not default_values:
            row.pop(3)

# construct table html
    table_html = _tabulate(rows, headers, tablefmt='html')

# add links to urls in text
    # markdown_url = re.compile('\[(.*?)\]\((.*)\)')
    table_html = _add_links(table_html)

    return table_html