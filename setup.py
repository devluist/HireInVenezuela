#!/usr/bin/env python

from setuptools import setup

setup(
    # GETTING-STARTED: set your app name:
    name='buy',
    # GETTING-STARTED: set your app version:
    version='0.5',
    # GETTING-STARTED: set your app description:
    description='App de inicio de HV',
    # GETTING-STARTED: set author name (your name):
    author='Luis Tena',
    # GETTING-STARTED: set author email (your email):
    author_email='example@example.com',
    # GETTING-STARTED: set author url (your url):
    url='',
    # GETTING-STARTED: define required django version:
    install_requires=[
        'Django==1.8.4'
    ],
    dependency_links=[
        'https://pypi.python.org/simple/django/'
    ],
)
