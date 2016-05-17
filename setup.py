import re
from setuptools import setup, find_packages

'''
References:
https://python-packaging-user-guide.readthedocs.org/en/latest/
https://docs.python.org/3.5/distutils/index.html
https://github.com/jgehrcke/python-cmdline-bootstrap
http://www.pyinstaller.org/

Installation Packages:
pip install wheel
pip install twine

Build Distributions:
python setup.py sdist --format=gztar,zip bdist_wheel

Upload Distributions to PyPi:
twine register dist/*
twine upload dist/[module-version]*

Installation:
pip install [module]
python setup.py develop  # for local on-the-fly file updates
python setup.py install  # when possessing distribution files

Uninstall:
pip uninstall [module]
python setup.py develop --uninstall # for removing symbolic link
# remove command line tool in ../Python/Python35-32/Scripts/

CLI Installation:
command = 'name of command'
module = 'name of module'
    entry_points = {
        "console_scripts": ['%s = %s.cli:cli' % (command, module)]
    },

System Installation:
# http://www.pyinstaller.org/

Old Methods:
python setup.py sdist bdist_wheel upload  # for PyPi
pip wheel --no-index --no-deps --wheel-dir dist dist/*.tar.gz
'''

config_file = open('jsonmodel/__init__.py').read()
version = re.search("^__version__\s*=\s*'(.*)'", config_file, re.M).group(1)
license = re.search("^__license__\s*=\s*'(.*)'", config_file, re.M).group(1)
# command = re.search("^__command__\s*=\s*'(.*)'", config_file, re.M).group(1)
module = re.search("^__module__\s*=\s*'(.*)'", config_file, re.M).group(1)
author = re.search("^__author__\s*=\s*'(.*)'", config_file, re.M).group(1)
email = re.search("^__email__\s*=\s*'(.*)'", config_file, re.M).group(1)
# author_list = re.search("^__authors__\s*=\s*'(.*)'", config_file, re.M).group(1)

setup(
    name=module,
    version=version,
    author=author,
    maintainer_email=email,
    include_package_data=True,  # Checks MANIFEST.in for explicit rules
    packages=find_packages(exclude=['cred','keys','docs','tests','models','notes']),  # Needed for bdist
    license=license,
    description="A Collection of Methods for Validating JSON Structured Data",
    long_description=open('README.rst').read(),
    install_requires=[],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5'
    ]
)