#!/bin/bash

# [description]
#     Run doppel-cli unit tests using
#     unittest
# [usage]
#     ./.ci/run_unit_tests.sh 50

# failure is a natural part of life
set -eou pipefail

MIN_TEST_COVERAGE=${1}

echo ""
echo "Running unit tests"
echo ""

    pytest \
        --cov \
        --cov-fail-under=${MIN_TEST_COVERAGE} \
        tests/

echo ""
echo "Done running unit tests"
echo ""
