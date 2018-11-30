from setuptools import setup

setup(
    name='doppel',
    version='0.0.1',
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
