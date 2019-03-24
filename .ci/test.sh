#!/bin/bash

# Failure is a natural part of life
set -e

# Set up environment variables
CI_TOOLS=$(pwd)/.ci
MIN_TEST_COVERAGE=95

# Make sure we're living in conda land
export PATH="$HOME/miniconda/bin:$PATH"

${CI_TOOLS}/lint_py.sh $(pwd)
${CI_TOOLS}/lint_r.sh $(pwd)
${CI_TOOLS}/check_docs.sh $(pwd)/docs
${CI_TOOLS}/run_unit_tests.sh ${MIN_TEST_COVERAGE}
${CI_TOOLS}/run_smoke_tests.sh $(pwd)/test_data

${CI_TOOLS}/install_test_packages.sh
${CI_TOOLS}/run_integration_tests.sh

# If all is good, we did it!
exit 0
