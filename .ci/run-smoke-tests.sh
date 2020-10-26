#!/bin/bash

# [description]
#     Run doppel-cli smoke tests. These
#     tests are intended to just ensure that
#     all the CLI entrypoints run AT ALL
#     on packages guaranteed to be installed
#     in any environment with the languages
#     supported by doppel-cli.
#
#     Correctness of results is not tested here,
#     but is left to unit tests and integration
#     tests.
# [usage]
#     ./.ci/run_smoke_tests.sh $(pwd)/test_data

TEST_DATA_DIR=${1}
R_TEST_PACKAGE="argparse"
PYTHON_TEST_PACKAGE="argparse"
TEST_FILES_TO_COMPARE="${TEST_DATA_DIR}/python_${PYTHON_TEST_PACKAGE}.json,${TEST_DATA_DIR}/r_${R_TEST_PACKAGE}.json"

# failure is a natural part of life
set -e

echo ""
echo "Running smoke tests"
echo ""

    mkdir -p "${TEST_DATA_DIR}"

    doppel-describe \
        -p ${PYTHON_TEST_PACKAGE} \
        --language python \
        --data-dir "${TEST_DATA_DIR}"
    doppel-describe \
        -p ${R_TEST_PACKAGE} \
        --language r \
        --data-dir "${TEST_DATA_DIR}"
    doppel-test \
        --files "${TEST_FILES_TO_COMPARE}" \
        --errors-allowed 100

echo ""
echo "Done running smoke tests"
echo ""
