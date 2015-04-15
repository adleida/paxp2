'''
    PAXP2
    ~~~~~

    PAXP2 is an AdExchange for mobile.

'''

import ast
import os
import os.path
import re
import setuptools


_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('paxp2/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

data_dir = 'paxp2/res'
data = [os.path.join(data_dir, f) for f in os.listdir(data_dir)]

setuptools.setup(
    name='paxp2',
    version=version,
    url='http://git.adleida.com/paxp2/',
    author='adleida',
    author_email='noreply@adleida.com',
    description='an adexchange for mobile',
    long_description=__doc__,
    packages=['paxp2'],
    package_data={'paxp2': data},
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    entry_points='''
        [console_scripts]
        paxp2=paxp2.cli:main
    ''',
    install_requires=[
        'flask',
        'jsonschema',
        'pyyaml',
        'requests',
        'toolz',
    ],
)
