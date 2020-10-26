#!/bin/bash

# [description]
#     Run doppel-cli integration tests. These are
#     primarily intended to test the analyze.* scripts
#     in doppel/bin. Their responsibility is to confirm
#     that the correct file content is generated by running
#     doppel-describe.
# [usage]
#     ./.ci/install_tests_packages.sh
#     ./.ci/run_integration_tests.sh $(pwd)/test_data

export TEST_DATA_DIR=${1}

# failure is a natural part of life
set -e

mkdir -p "${TEST_DATA_DIR}"

echo ""
echo "Running python integration tests"
echo ""

    pushd "$(pwd)/integration_tests/python_tests"
        pytest \
            --cache-clear \
            -vv
    popd || exit 1

echo ""
echo "Done running python integration tests"
echo ""

echo ""
echo "Running R integration tests"
echo ""
    
    DOPPEL_DESCRIBE_LOC=$(which doppel-describe)
    export DOPPEL_DESCRIBE_LOC
    pushd "$(pwd)/integration_tests/r_tests"
        Rscript --vanilla -e "testthat::test_dir('.', stop_on_failure = TRUE)"
    popd || exit 1

echo ""
echo "Done running R integration tests"
echo ""


TEST_PKG_DIR="$(pwd)/integration_tests/test-packages"
R_TEST_PKG_DIR="${TEST_PKG_DIR}/r"

# All other tests in this file only make sense if
# the Python and R test packages are equivalent.
# This block of code down here tests that they are
for pkg in $(ls "${R_TEST_PKG_DIR}"); do

    echo ""
    echo "Checking API similarity of package '${pkg}' with doppel-test"
    echo ""

        doppel-test \
            --files "${TEST_DATA_DIR}/r_${pkg}.json,${TEST_DATA_DIR}/python_${pkg}.json" \
            --errors-allowed 0

    echo ""
    echo "Done checking similarity"
    echo ""
done
