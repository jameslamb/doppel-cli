#!/bin/bash

# failure is a natural part of life
set -e

conda config --set always_yes yes --set changeps1 no
conda update -q conda
conda info -a

# Set up R (gulp)
conda install \
    -c conda-forge \
    --yes \
    'r-base>=4.1.0'

conda install \
    -c r \
    --quiet \
    --yes \
    r-assertthat \
    r-jsonlite \
    r-r6 \
    r-roxygen2 \
    r-testthat

conda install \
    -c conda-forge \
    --quiet \
    --yes \
    r-covr \
    r-argparse \
    r-futile.logger

# Get Python packages for testing
pip install \
    argparse \
    click \
    coverage \
    codecov \
    requests \
    sphinx \
    sphinx_autodoc_typehints \
    sphinx_rtd_theme \
    tabulate \
    wheel

conda install \
    -y \
        pytest \
        pytest-cov
