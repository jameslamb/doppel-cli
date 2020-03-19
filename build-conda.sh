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

CONDA_ARTIFACT_DIR="$(dirname $(dirname $(which conda)))"

echo "Cleaning out old artifacts"
conda build purge
echo "Done cleaning out old artifacts"

for py_version in ${PYTHON_VERSIONS}; do

    mkdir -p tmp-${py_version}

    echo ""
    echo "====================================="
    echo "= Building conda package: Python ${py_version} ="
    echo "====================================="
    echo ""

    conda build --python ${py_version} conda-recipe/

    echo ""
    echo "==========================================="
    echo "= Converting for all platforms: Python ${py_version} ="
    echo "==========================================="
    echo ""
    conda convert \
        --platform all \
        -o uploads-python${py_version}

done
