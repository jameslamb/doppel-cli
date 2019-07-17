#!/bin/bash

# failure is a natural part of life
set -e

PYTHON_VERSIONS="
    3.5
    3.6
    3.7
"

PLATFORMS="
    osx-64
    linux-64
    win-64
"

BUILD_SYSTEM_OS="osx-64"

for py_version in ${PYTHON_VERSIONS}; do
    for platform in ${PLATFORMS}; do

        echo "Building conda package: Python ${py_version} (${platform})"

        # if it's osx-64, build the package

    done
done
