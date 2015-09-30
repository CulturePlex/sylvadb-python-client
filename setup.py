#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from setuptools import setup


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

# Dynamically get the constants.
module = __import__('sylvadbclient')

tests_require = []

setup(
    name='sylvadbclient',
    version=module.__version__,
    author=module.__author__,
    author_email=module.__email__,
    url=module.__url__,
    description=module.__description__,
    long_description=read('README.rst') + "\n\n" + read('CHANGES.txt'),
    license=module.__license__,
    keywords='sylvadb graph graphdb graphdatabase database rest client driver',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
    ],
    zip_safe=False,
    packages=[
        "sylvadbclient",
    ],
    include_package_data=True,
    install_requires=read("requirements.txt").split("\n"),
    tests_require=tests_require,
    test_suite='sylvadbclient.tests',
    extras_require={},
)
