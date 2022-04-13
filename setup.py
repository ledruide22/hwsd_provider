# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    my_license = f.read()

setup(
    name='hwsd_provider',
    version='0.2.0',
    description='hwsd soil data provider',
    long_description=readme,
    author='Dauloudet Olivier',
    url='https://github.com/Smeaol22/hwsd_provider.git',
    license=my_license,
    install_requires=[
        "gdal>=3.0,<3.5",
        "pyodbc>=4.0,<4.1",
        "rasterio>=1.1,<1.3",
        "jaydebeapi>=1.2,<1.3"
    ],
    tests_require=[
        "pytest",
        "pytest-mock",
    ],
    package_dir={'': 'src'},
    packages=find_packages('src')
)
