#!/bin/bash

# failure is a natural part of life
set -e

for pkg in uptasticsearch; do

    # The R package
    doppel-describe \
        -p ${pkg} \
        --language R \
        --data-dir $(pwd)/test_data

    # The python package
    doppel-describe \
        -p ${pkg} \
        --language python \
        --data-dir $(pwd)/test_data

    # test
    doppel-test \
        --files $(pwd)/test_data/python_${pkg}.json,$(pwd)/test_data/r_${pkg}.json \
        | tee ${pkg}.log \
        | cat

done
