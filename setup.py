# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='src',
    version='0.1.0',
    description='Deleware North Take Home Assignment',
    long_description=readme,
    author='Titus Hutchinson',
    author_email='titushutchinson79@gmail.com',
    url='https://github.com/thutchinson1/dn_take-home_Thutchinson.git',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

