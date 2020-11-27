#!/bin/bash

# [description]
#     Measure the test coverage of analyze.py
# [usage]
#     ./.ci/run-analyze-py-coveraage.sh 50

# failure is a natural part of life
set -eou pipefail

MIN_TEST_COVERAGE=${1}

INTEGRATION_TEST_DIR=$(pwd)/.ci/analyze_py_tests
mkdir -p $(pwd)/test_data

# This is a thing ... need to have a copy of the code
# near the tests so we can use a relative import to
# import and call it
echo "copying analyze.py to a location next to the tests"
ANALYZE_PY_SCRIPT=$(pwd)/doppel/bin/analyze.py
ANALYZE_PY_COPY=${INTEGRATION_TEST_DIR}/doppel_analyze.py
cp ${ANALYZE_PY_SCRIPT} ${ANALYZE_PY_COPY}

pushd ${INTEGRATION_TEST_DIR}
    pytest \
        --cov

    coverage report \
        -m \
        --fail-under=${MIN_TEST_COVERAGE}
popd
