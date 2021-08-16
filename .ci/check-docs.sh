#!/bin/bash

# [description]
#     Check sphinx docs for issues. Return
#     non-zero exit code if any warnings show up
# [usage]
#     ./.ci/check_docs.sh $(pwd)/docs

# failure is a natural part of life
set -eou pipefail

SOURCE_DIR="${1}"

echo ""
echo "Checking docs for problems"
echo ""

    pushd "${SOURCE_DIR}"
        make html
        NUM_WARNINGS=$(cat warnings.txt | wc -l)
        if [[ ${NUM_WARNINGS} -ne 0 ]]; then
            echo "Found ${NUM_WARNINGS} issues in Sphinx docs in the docs/ folder";
            exit "${NUM_WARNINGS}";
        fi
    popd

echo ""
echo "Done checking docs"
echo ""
