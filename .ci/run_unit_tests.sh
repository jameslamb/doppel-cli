#!/bin/bash

# [description]
#     Run doppel-cli unit tests using
#     unittest
# [usage]
#     ./.ci/run_unit_tests.sh 50

MIN_TEST_COVERAGE=${1}

# failure is a natural part of life
set -e

echo ""
echo "Running unit tests"
echo ""

    coverage run setup.py test
    coverage report -m --fail-under=${MIN_TEST_COVERAGE}

echo ""
echo "Done running unit tests"
echo ""
