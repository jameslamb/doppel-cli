
# Failure is a natural part of life
set -e

# Set up environment variables
TEST_DATA_DIR=$(pwd)/test_data
MIN_TEST_COVERAGE=20
INTEGRATION_TEST_PACKAGE=argparse


echo "Checking code for style problems..."

    pycodestyle \
        --show-pep8 \
        --show-source \
        --verbose \
        $(pwd)

echo "Done checking code for style problems."

echo "Checking docs for problems"

    pushd $(pwd)/docs
    make html
    NUM_WARNINGS=$(cat warnings.txt | wc -l)
    if [[ ${NUM_WARNINGS} -ne 0 ]]; then
        echo "Found ${NUM_WARNINGS} issues in Sphinx docs in the docs/ folder";
        exit ${NUM_WARNINGS};
    fi
    popd

echo "Done checking docs"

echo "Running unit tests"

    coverage run setup.py test
    coverage report -m --fail-under=${MIN_TEST_COVERAGE}

echo "Done running unit tests"

echo "Running integration tests"
    
    mkdir -p ${TEST_DATA_DIR}
    doppel-describe \
        -p ${INTEGRATION_TEST_PACKAGE} \
        --language python \
        --data-dir ${TEST_DATA_DIR}
    doppel-describe \
        -p ${INTEGRATION_TEST_PACKAGE} \
        --language r \
        --data-dir ${TEST_DATA_DIR}
    doppel-test \
        --files ${TEST_DATA_DIR}/python_argparse.json,${TEST_DATA_DIR}/r_argparse.json \
        --errors-allowed 100

echo "Done running integration tests"

# If all is good, we did it!
exit 0
