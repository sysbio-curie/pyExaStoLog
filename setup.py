from setuptools import setup, find_packages

setup(name='exastolog',
    version="1.0.0a0",
    author="Vincent Noel",
    author_email="contact@vincent-noel.fr",
    description="A library for the exact calculation of stationary states of MaBoSS models",
	install_requires = ['numpy', 'scipy', 'boolean.py', 'networkx'],
	packages=['exastolog'],
)