from setuptools import setup
with open('README','r') as f:
    readme = f.read()
with open('HISTORY','r') as f:
    history = f.read()
packages=[
	'pymgsql'
]
requires=[
	'sqlobject'
]
setup(name='pymgsql',
	version='1.0',
	author='iinitz',
	author_email='hanamiza555@gmail.com',
	description='A python API for manage your SQL database (select, insert, update, delete) like NoSQL',
	long_description=readme+'\n\n'+history,
	packages=packages,
	package_dir={'pymgsql':'pymgsql'},
	install_requires=requires
)
