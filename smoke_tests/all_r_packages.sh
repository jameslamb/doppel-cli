#!/bin/bash

# failure is a natural part of life
set -e

OUT_DIR=${1:-$(pwd)/smoke_tests/test_data}

# Set up summary file and be sure it's blank
SUMMARY_FILE=${OUT_DIR}/successful_r_packages.txt
echo "" > ${SUMMARY_FILE}

# Function to run doppel-describe
# [usage]
#     run_describe ${LANGUAGE} ${OUT_DIR} ${PKG}
run_describe () {
    doppel-describe \
        --language ${1} \
        --data-dir ${2} \
        -p ${3}
}

R_LIB=$(
    Rscript -e "cat(.libPaths()[1])"
)
ALL_R_PACKAGES=$(ls ${R_LIB})
NUM_PACKAGES=$(echo ${ALL_R_PACKAGES} | wc -w)

echo "You have ${NUM_PACKAGES} R packages installed."

# Randomly select packages and start working through them
RANDOM_PACKAGES=$(
    echo $ALL_R_PACKAGES | tr ' ' "\n" | sort --sort=random
)

for pkg in ${RANDOM_PACKAGES}; do

    echo "Running doppel on package: ${pkg}"

    run_describe R ${OUT_DIR} ${pkg}

    echo ${pkg} >> ${SUMMARY_FILE}
done

open ${SUMMARY_FILE}
