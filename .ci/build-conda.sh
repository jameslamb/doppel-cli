#!/bin/bash

# failure is a natural part of life
set -e

PYTHON_VERSIONS="
    3.5
    3.6
    3.7
    3.8
"

BUILD_SYSTEM_OS="osx-64"

CONDA_ARTIFACT_DIR="$(dirname $(dirname $(which conda)))/conda-bld"

LOCAL_ARTIFACT_DIR=$(pwd)/conda-uploads
mkdir -p ${LOCAL_ARTIFACT_DIR}

echo "Cleaning out old artifacts"
conda build purge
echo "Done cleaning out old artifacts"

for py_version in ${PYTHON_VERSIONS}; do

    echo ""
    echo "====================================="
    echo "= Building conda package: Python ${py_version} ="
    echo "====================================="
    echo ""

    conda build --python ${py_version} conda-recipe/

    echo ""
    echo "============================================"
    echo "= Converting for all platforms: Python ${py_version} ="
    echo "============================================"
    echo ""

    SHORT_VERSION=$(echo ${py_version} | tr -d '.')
    TARBALL_BASENAME="doppel-cli-$(cat VERSION)-py${SHORT_VERSION}.tar.bz2"
    FULL_PACKAGE_PATH=${CONDA_ARTIFACT_DIR}/${BUILD_SYSTEM_OS}/${TARBALL_NAME}
    conda-convert \
        --platform all \
        --output-dir ${LOCAL_ARTIFACT_DIR} \
        ${FULL_PACKAGE_PATH}

    # the package for the build system won't be converted, just copy it
    mkdir -p ${LOCAL_ARTIFACT_DIR}/${BUILD_SYSTEM_OS}
    cp ${FULL_PACKAGE_PATH} ${LOCAL_ARTIFACT_DIR}/${BUILD_SYSTEM_OS}/

done
