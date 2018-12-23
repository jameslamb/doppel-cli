#!/bin/bash

# Failure is a natural part of life
set -e

PYPI_REPO=$1

VERSION=$(cat VERSION)
python setup.py sdist
twine upload dist/doppel-cli-${VERSION}.tar.gz -r ${PYPI_REPO}

# References
# [1] https://blog.jetbrains.com/pycharm/2017/05/how-to-publish-your-package-on-pypi/
# [2] https://packaging.python.org/guides/using-testpypi/
