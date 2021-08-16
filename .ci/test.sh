#!/bin/bash

# [description]
#     Run all of the tests for this repo
# [usage]
#     ./.ci/test.sh

# failure is a natural part of life
set -eou pipefail

# Set up environment variables
CI_TOOLS=$(pwd)/.ci

# Test coverage stuff
MIN_UNIT_TEST_COVERAGE=100
MIN_ANALYZE_R_TEST_COVERAGE=100
MIN_ANALYZE_PY_TEST_COVERAGE=100

if [[ $TASK == "lint" ]]; then
    conda install -c conda-forge \
        'r-lintr>=2.0.0'
    # Get Python packages for testing
    pip install \
        --upgrade \
        --user \
            black \
            flake8 \
            mypy \
            pycodestyle \
            pylint \
            types-requests \
            types-setuptools \
            types-tabulate
    make lint
    Rscript ${CI_TOOLS}/lint-r-code.R $(pwd)
    ${CI_TOOLS}/lint-todo.sh
    exit 0
fi

if [[ $OS_NAME == "macOS-latest" ]]; then
    conda create -q -n testenv python=3.6 nose pytest pytest-cov
    source activate testenv
    pip install argparse requests
fi

python setup.py install

${CI_TOOLS}/check-docs.sh $(pwd)/docs
${CI_TOOLS}/run-unit-tests.sh ${MIN_UNIT_TEST_COVERAGE}
${CI_TOOLS}/run-smoke-tests.sh $(pwd)/test_data

${CI_TOOLS}/install-test-packages.sh
${CI_TOOLS}/run-integration-tests.sh $(pwd)/test_data

Rscript --vanilla ${CI_TOOLS}/test-analyze-r-coverage.R \
    --source-dir $(pwd) \
    --fail-under ${MIN_ANALYZE_R_TEST_COVERAGE}

${CI_TOOLS}/run-analyze-py-coverage.sh ${MIN_ANALYZE_PY_TEST_COVERAGE}

# If all is good, we did it!
exit 0
