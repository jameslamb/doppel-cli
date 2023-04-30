#!/bin/bash

# [description]
#     Lint python code in a directory for style
#     problems
# [usage]
#     ./.ci/lint-py.sh $(pwd)

# failure is a natural part of life
set -eou pipefail

SOURCE_DIR=${1}

MAX_LINE_LENGTH=100

echo ""
echo "Checking code for python style problems..."
echo ""
    
    echo ""
    echo "###############"
    echo "#    black    #"
    echo "###############"
    echo ""
    black \
        --line-length ${MAX_LINE_LENGTH} \
        --check \
        --diff \
        ${SOURCE_DIR} \
    || exit  -1

    echo ""
    echo "###############"
    echo "#   flake8    #"
    echo "###############"
    echo ""
    flake8 \
        --max-line-length ${MAX_LINE_LENGTH} \
        ${SOURCE_DIR} \
    || exit -1

    echo ""
    echo "###############"
    echo "#   pylint    #"
    echo "###############"
    echo ""
    #
    # disables:
    #     * C0103: Variable doesn't conform to snake_case
    #     * E1120: No value for argument in function call
    #     * R0801: Similar lines in 2 files
    #     * R0903: Too few public methods
    #     * R0914: Too many local variable
    #     * W1202: Use lazy % formatting in logging functions
    #
    pushd ${SOURCE_DIR}/doppel
        pylint \
            --disable=C0103,E1120,R0801,R0903,R0914,W1202 \
            . \
        || exit -1
    popd

    echo ""
    echo "###############"
    echo "#    mypy     #"
    echo "###############"
    echo ""
    mypy \
        --explicit-package-bases \
        --ignore-missing-imports \
        ${SOURCE_DIR}/doppel \
    || exit  -1

echo ""
echo "Done checking code for style problems."
echo ""
