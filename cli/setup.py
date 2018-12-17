from setuptools import setup

with open('../README.md', 'r') as f:
    readme = f.read()

with open('VERSION', 'r') as f:
    version = f.read().strip()

setup(
    name='doppel',
    description='an integration testing framework for testing API similarity across languages.',
    long_description=readme,
    version=version,
    url='http://github.com/jameslamb/doppel',
    license='Apache 2.0',
    maintainer='James Lamb',
    maintainer_email='jaylamb20@gmail.com',
    install_requires=[
        'click',
        'tabulate'
    ],
    packages=['doppel'],
    package_data={
        'doppel': ['bin/analyze.R', 'bin/analyze.py']
    },
    entry_points={
        'console_scripts': [
            'doppel-describe = doppel.describe:main',
            'doppel-test = doppel.cli:main'
        ]
    }
)
