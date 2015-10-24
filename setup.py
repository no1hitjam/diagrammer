from setuptools import setup
setup(
	name='diagrammer',
	author='Jackson',
	#version="0.0.1",
	packages=['diagrammer'],
	requires=['enum'],
	install_requires=['enum'],
	description='console-based sentence diagrammer',
	entry_points={
		'console_scripts': [
			'diagrammer=diagrammer.__main__:main',
		],
	},
)