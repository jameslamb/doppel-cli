#!/bin/bash

# [description]
#     Lint python code in a directory for style
#     problems
# [usage]
#     ./.ci/lint_py.sh $(pwd)

SOURCE_DIR=${1}

echo ""
echo "Checking code for python style problems..."
echo ""
    
    echo "running pycodestyle checks"
    pycodestyle \
        --show-pep8 \
        --show-source \
        --verbose \
        ${SOURCE_DIR} \
    || exit -1

    echo "running flake8 checks"
    flake8 \
        --ignore=E501 \
        ${SOURCE_DIR} \
    || exit -1

echo ""
echo "Done checking code for style problems."
echo ""
