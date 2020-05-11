from setuptools import setup, find_packages
import sys
sys.path.insert(0, sys.path[0])
from utils import inject_init

init_path = 'jsonmodel/__init__.py'
readme_path = 'README.rst'
setup_kwargs = {
    'include_package_data': True,  # Checks MANIFEST.in for explicit rules
    'packages': find_packages(),
    'install_requires': [],
    'classifiers': [
        # https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5'
    ]
}
setup_kwargs = inject_init(init_path, readme_path, setup_kwargs)
setup(**setup_kwargs)

''' DOCUMENTATION
References:
https://docs.python.org/3.6/distutils/setupscript.html

https://python-packaging-user-guide.readthedocs.org/en/latest/
https://docs.python.org/3.6/distutils/index.html
https://github.com/jgehrcke/python-cmdline-bootstrap
http://www.pyinstaller.org/

Installation Packages:
pip install wheel
pip install twine

Build Distributions:
python setup.py sdist --format=gztar,zip
pip wheel --no-index --no-deps --wheel-dir dist dist/jsonmodel-3.1.tar.gz

Upload (or Register) Distributions to PyPi:
twine upload dist/jsonmodel-3.1*

Upload Documentation to Github:
mkdocs gh-deploy
.gitconfig [credential] helper = wincred

Installation:
pip install [module]
python setup.py develop  # for local on-the-fly file updates
python setup.py install  # when possessing distribution files
pip install dist/jsonmodel-3.1-py3-none-any.whl # when possessing wheel file

Uninstall:
pip uninstall [module]
python setup.py develop --uninstall # for removing symbolic link
# remove command line tool in ../Python/Python3.6/Scripts/

CLI Installation:
command = 'name of command'
module = 'name of module'
entry_points = {
    "console_scripts": ['%s = %s.cli:cli' % (command, module)]
},

System Installation:
# http://www.pyinstaller.org/

Mercurial Dev Setup:
.hgignore (add dist/, *.egg-info/, '.git/')
hgrc [paths] default = ssh://hg@bitbucket.org/collectiveacuity/pocketlab

Git Public Setup:
.gitignore (add dist/, *.egg-info/, dev/, tests_dev/, docs/, docs_dev/, .hg/, .hgignore)
git init
git remote add origin https://github.com/collectiveacuity/pocketLab.git

Git Public Updates:
git add -A
git commit -m 'updates'
git push origin master

Git Remove History: [Run as admin and pause syncing]
git filter-branch --force --index-filter 'git rm -rf --cached --ignore-unmatch dev/*' --prune-empty --tag-name-filter cat -- --all

GitHub.io Documentation:
mkdocs gh-deploy -r origin
'''