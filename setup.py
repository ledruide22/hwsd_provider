# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='hwsd_provider',
    version='0.1.0',
    description='hwsd soil data provider',
    long_description=readme,
    author='Dauloudet Olivier',
    url='https://github.com/Smeaol22/hwsd_provider.git',
    license=license,
    packages=find_packages(exclude='tests')
)
