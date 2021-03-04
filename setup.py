#!/usr/bin/env python
from setuptools import setup

setup(
    name='deisapi',
    version='0.1.0',
    description="Simple python wrapper for Deis's APIs",
    long_description=open('README.rst').read(),
    author='Ilche Bedelovski',
    author_email='ilche.bedelovski@keitaro.info',
    url='https://bitbucket.org/keitaroinc/deisapi',
    download_url='',
    license='LICENSE.txt',
    packages=['deisapi'],
    install_requires=[
        'requests==2.20.0'
    ],
)
