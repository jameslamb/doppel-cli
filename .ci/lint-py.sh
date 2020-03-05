#!/bin/bash

# [description]
#     Lint python code in a directory for style
#     problems
# [usage]
#     ./.ci/lint_py.sh $(pwd)

SOURCE_DIR=${1}

# failure is a natural part of life
set -e

echo ""
echo "Checking code for python style problems..."
echo ""

    pycodestyle \
        --show-pep8 \
        --show-source \
        --verbose \
        ${SOURCE_DIR}

echo ""
echo "Done checking code for style problems."
echo ""
