#! /usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup


with open('./requirements.txt') as f:
    install_requires = [l for l in f]

with open('./requirements-test.txt') as f:
    test_requires = [l for l in f]

setup(
    name="deadalus",
    version='0.1.0',
    url='https://bitbucket.org/blurrcat/daedalus',
    author='blurrcat',
    author_email='blurrcat@gmail.com',
    license='MIT',
    packages=['daedalus'],
    install_requires=install_requires,
    tests_require=test_requires,
)
