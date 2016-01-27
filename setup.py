__author__ = 'rcj1492'
__created__ = '2015.11'

from setuptools import setup, find_packages

'''
References:
https://docs.python.org/3.5/distutils/index.html
https://the-hitchhikers-guide-to-packaging.readthedocs.org/en/latest/creation.html

Commands:
python setup.py sdist --formats=gztar,zip
python setup.py develop  # for local on-the-fly updating
python setup.py install
python setup.py register  # for PyPi
python setup.py sdist upload  # for PyPi
'''

setup(
    name="jsonmodel",
    version="1.0",
    author = __author__,
    include_package_data=True,  # Checks MANIFEST.in for explicit rules
    packages=find_packages(),
    license="LICENSE.txt",
    description="A Collection of Methods for Validating JSON Structured Data",
    long_description=open('README.rst').read(),
    install_requires=[],
    classifiers=[
        'Development Status :: Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4'
    ]
)