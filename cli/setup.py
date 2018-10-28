from setuptools import setup

setup(
    name='doppel',
    version='0.0.1',
    install_requires=[
        'click'
    ],
    packages=['doppel'],
    entry_points={
        'console_scripts': [
            'doppel = doppel.cli:main',
        ]
    }
)
