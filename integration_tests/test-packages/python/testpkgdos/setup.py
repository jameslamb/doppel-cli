from setuptools import setup
from setuptools import find_packages

setup(
    name='testpkgdos',
    packages=find_packages(),
    description="""
    Second package for testing doppel-cli. This
    is used to test the behavior of doppel-cli on
    a functions-only package.
    """,
    version='0.0.1',
    maintainer='James Lamb',
    maintainer_email='jaylamb20@gmail.com',
    install_requires=[],
    extras_require={}
)
