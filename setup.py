__author__ = 'rcj1492'
__created__ = '2015.11'

from setuptools import setup, find_packages

# For more examples, see
#   https://the-hitchhikers-guide-to-packaging.readthedocs.org/en/latest/creation.html

setup(
   name="jsonModel",
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