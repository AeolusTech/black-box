# -*- coding: utf-8 -*-


from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='isoml',
    version='0.0.1',
    description='ISOML package',
    long_description=readme,
    author='Alef Aviation Sp. z o.o.',
    author_email='kamil.kuczaj@gmail.com',
    url='https://github.com/AeolusTech/BlackBox',
    license=license,
    packages=find_packages(exclude=('docs'))
)
