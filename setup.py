#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


# noinspection PyPackageRequirements
setup(
    name='pytest-changed',
    version='0.1.4',
    author='Gastrofix GmbH',
    author_email='tech@gastrofix.com',
    maintainer='Gastrofix GmbH',
    maintainer_email='tech@gastrofix.com',
    license='Mozilla Public License 2.0',
    url='https://github.com/gastrofix-gmbh/pytest-changed',
    description='A pytest plugin that finds changed test files based on '
                'git diff and selects only those unctions or classes that '
                'really were changed for the test run.',
    long_description=read('README.rst'),
    py_modules=['pytest_changed'],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
    install_requires=[
        'pytest>=3.5.0',
        'GitPython>=3.0.2'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
    ],
    entry_points={
        'pytest11': [
            'changed = pytest_changed',
        ],
    },
)
