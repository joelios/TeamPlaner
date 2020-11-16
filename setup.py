# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in teamplaner/__init__.py
from teamplaner import __version__ as version

setup(
	name='teamplaner',
	version=version,
	description='Frappe App to manage Floorball Teams',
	author='msmr.ch',
	author_email='info@msmr.ch',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
