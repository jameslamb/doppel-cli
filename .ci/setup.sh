#!/bin/bash

# failure is a natural part of life
set -e

# Set up environment variables
export CRAN_MIRROR=http://cran.rstudio.com

# if [[ $OS_NAME == "macOS-latest" ]]; then
#     export MINICONDA_INSTALLER=https://repo.continuum.io/miniconda/Miniconda3-4.3.21-MacOSX-x86_64.sh
# elif [[ $OS_NAME == "ubuntu-latest" ]]; then
#     export MINICONDA_INSTALLER=https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
# fi

# Install conda
# wget ${MINICONDA_INSTALLER} -O miniconda.sh;
# bash miniconda.sh -b -p ${CONDA_DIR}

conda config --set always_yes yes --set changeps1 no
conda update -q conda
conda info -a

# Set up R (gulp)
conda install \
    -c r \
    --quiet \
    r-assertthat \
    r-jsonlite \
    r-r6 \
    r-roxygen2 \
    r-testthat

conda install \
    -c conda-forge \
    --quiet \
    r-covr \
    r-argparse \
    r-futile.logger

# Per https://github.com/ContinuumIO/anaconda-issues/issues/9423#issue-325303442,
# packages that require compilation may fail to find the
# gcc bundled with conda

#export PATH=${PATH}:${CONDA_DIR}/bin

# Get Python packages for testing
pip install \
    --user \
        argparse \
        click \
        coverage \
        codecov \
        requests \
        sphinx \
        sphinx_autodoc_typehints \
        sphinx_rtd_theme \
        tabulate

# export PIP_INSTALL_OPTS="--no-color"
# if [[ $OS_NAME == "macOS-latest" ]]; then
#     export PIP_INSTALL_OPTS="--user"
# fi

pip install \
    --user \
        pytest \
        pytest-cov
