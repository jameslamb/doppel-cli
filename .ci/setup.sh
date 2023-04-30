#!/bin/bash

# failure is a natural part of life
set -e

conda config --set always_yes yes --set changeps1 no
conda update -q conda
conda info -a

# Set up R (gulp)
conda install \
    -c conda-forge \
    r-argparse \
    r-assertthat \
    r-covr \
    r-futile.logger \
    r-jsonlite \
    r-r6 \
    r-roxygen2 \
    r-testthat

# Get Python packages for testing
pip install \
    argparse \
    click \
    coverage \
    pytest \
    pytest-cov \
    requests \
    sphinx \
    sphinx_autodoc_typehints \
    sphinx_rtd_theme \
    tabulate \
    types-setuptools \
    types-tabulate \
    wheel
