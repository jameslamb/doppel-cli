#!/bin/bash

# [description]
#     Run all of the tests for this repo
# [usage]
#     ./.ci/test.sh

# Failure is a natural part of life
set -e

# Set up environment variables
CI_TOOLS=$(pwd)/.ci

# Test coverage stuff
MIN_UNIT_TEST_COVERAGE=95
MIN_ANALYZE_R_TEST_COVERAGE=100
MIN_ANALYZE_PY_TEST_COVERAGE=90

# Make sure we're living in conda land
export PATH="$HOME/miniconda/bin:$PATH"

${CI_TOOLS}/lint_py.sh $(pwd)
Rscript ${CI_TOOLS}/lint_r_code.R $(pwd)
${CI_TOOLS}/check_docs.sh $(pwd)/docs
${CI_TOOLS}/run_unit_tests.sh ${MIN_UNIT_TEST_COVERAGE}
${CI_TOOLS}/run_smoke_tests.sh $(pwd)/test_data

${CI_TOOLS}/install_test_packages.sh
${CI_TOOLS}/run_integration_tests.sh $(pwd)/test_data

Rscript ${CI_TOOLS}/test-analyze-r-coverage.R \
    --source-dir $(pwd) \
    --fail-under ${MIN_ANALYZE_R_TEST_COVERAGE}

${CI_TOOLS}/run_analyze_py_coverage.sh ${MIN_ANALYZE_PY_TEST_COVERAGE}

# If all is good, we did it!
exit 0
