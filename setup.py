from setuptools import find_packages
from setuptools import setup

setup(name='algotaf',
	  version='1.0',
	  url='https://github.com/ramasrirama99/AlgoTradeFramework',
	  license='MIT',
	  install_requires=[
	  	'psycopg2',
	  	'pgcopy',
	  	'requests',
	  	'schedule'
	  ],
	  packages=find_packages())
