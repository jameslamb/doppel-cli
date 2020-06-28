#!/bin/bash

# [description]
#     Lint python code in a directory for style
#     problems
# [usage]
#     ./.ci/lint_py.sh $(pwd)

SOURCE_DIR=${1}

MAX_LINE_LENGTH=100

echo ""
echo "Checking code for python style problems..."
echo ""
    
    echo "checking code style with black"
    black \
        --line-length ${MAX_LINE_LENGTH} \
        .
    || exit  -1

    echo "running pycodestyle checks"
    pycodestyle \
        --show-pep8 \
        --show-source \
        --verbose \
        ${SOURCE_DIR} \
    || exit -1

    echo "running flake8 checks"
    flake8 \
        --max-line-length ${MAX_LINE_LENGTH} \
        ${SOURCE_DIR} \
    || exit -1

    echo "running mypy checks"
    mypy \
        --ignore-missing-imports \
        . \
    || exit  -1

echo ""
echo "Done checking code for style problems."
echo ""
