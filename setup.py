__author__ = 'rcj1492'
__created__ = '2015.10'

from setuptools import setup

# For more examples, see
#   https://the-hitchhikers-guide-to-packaging.readthedocs.org/en/latest/creation.html
setup(
   name="labAWS",
   version="0.1",
   author = __author__,
   packages = ["labAWS"],
   license="LICENSE.txt",
   description="A Collection of Tools for Managing Backend Infrastructure on Amazon Web Services",
   long_description=open('README.rst').read(),
   install_requires=["paramiko >= 1.15.2"]
)