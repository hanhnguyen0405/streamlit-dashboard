from setuptools import setup, find_packages
from os import path

pkg_name = 'streamlit-dashboard'
here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), 'r') as f:
    long_description = f.read()

with open(path.join(here, 'requirements.txt')) as f:
    requirements = f.read().splitlines()

__version__ = '0.0.1'

setup(
    name=pkg_name.replace('_', '-'),
    version=__version__,
    description="streamlit-dashboard",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='TN',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    scripts=[],
    install_requires=requirements,
)