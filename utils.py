__author__ = 'rcj1492'
__created__ = '2017.06'
__license__ = 'MIT'


def inject_init(init_path, readme_path, setup_kwargs):
    '''
        a method to add arguments to setup.py from module init file

    :param init_path: string with path to module __init__ file
    :param readme_path: string with path to module README.rst file
    :param setup_kwargs: dictionary with existing setup keyword arguments
    :return: dictionary with injected keyword arguments
    '''

    import re
    from os import path
    from copy import deepcopy

    # retrieve init text
    init_text = ''
    if not path.exists(init_path):
        raise ValueError('%s is not a valid path' % init_path)
    init_text = open(init_path).read()

    # retrieve init settings
    init_kwargs = {
        'version': '',
        'author': '',
        'url': '',
        'description': '',
        'license': '',
    }
    for key in init_kwargs.keys():
        key_regex = re.compile("__%s__\s?\=\s?'(.*?)'" % key)
        key_search = key_regex.findall(init_text)
        if key_search:
            init_kwargs[key] = key_search[0]

            # retrieve modifiable settings
    mod_kwargs = {
        'module': '',
        'email': '',
        'entry': '',
        'authors': ''
    }
    for key in mod_kwargs.keys():
        key_regex = re.compile("__%s__\s?\=\s?'(.*?)'" % key)
        key_search = key_regex.findall(init_text)
        if key_search:
            mod_kwargs[key] = key_search[0]
    if mod_kwargs['module']:
        init_kwargs['name'] = mod_kwargs['module']
    if mod_kwargs['entry']:
        init_kwargs['entry_points'] = {"console_scripts": [mod_kwargs['entry']]}
    if mod_kwargs['email']:
        init_kwargs['author_email'] = mod_kwargs['email']
        init_kwargs['maintainer_email'] = mod_kwargs['email']
    if mod_kwargs['authors']:
        del init_kwargs['author']
        init_kwargs['author_list'] = mod_kwargs['authors'].split(' ')

    # add readme
    if not path.exists(readme_path):
        raise ValueError('%s is not a valid path' % readme_path)
    try:
        readme_text = open(readme_path).read()
        init_kwargs['long_description'] = str(readme_text)
    except:
        raise ValueError('%s is not a valid text file.' % readme_path)

    # merge kwargs
    setup_kwargs.update(**init_kwargs)
    updated_kwargs = deepcopy(setup_kwargs)
    for key, value in updated_kwargs.items():
        if not value:
            del setup_kwargs[key]

    return setup_kwargs
