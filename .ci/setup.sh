
# Failure is a natural part of life
set -e

# Set up environment variables
export CRAN_MIRROR=http://cran.rstudio.com

if [[ $TRAVIS_OS_NAME == "osx" ]]; then
    export MINICONDA_INSTALLER=https://repo.continuum.io/miniconda/Miniconda3-4.3.21-MacOSX-x86_64.sh
elif [[ $TRAVIS_OS_NAME == "linux" ]]; then
    export MINICONDA_INSTALLER=https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
fi

# Install conda
wget ${MINICONDA_INSTALLER} -O miniconda.sh;
bash miniconda.sh -b -p ${CONDA_DIR}

${CONDA_DIR}/bin/conda config --set always_yes yes --set changeps1 no
${CONDA_DIR}/bin/conda update -q conda
${CONDA_DIR}/bin/conda info -a

# Set up R (gulp)
${CONDA_DIR}/bin/conda install -c r \
    r-assertthat \
    r-jsonlite \
    r-r6 \
    r-roxygen2 \
    r-testthat

${CONDA_DIR}/bin/conda install -c conda-forge \
    r-covr \
    r-argparse \
    r-futile.logger \
    r-lintr>=2.0.0

# Per https://github.com/ContinuumIO/anaconda-issues/issues/9423#issue-325303442,
# packages that require compilation may fail to find the
# gcc bundled with conda

export PATH=${PATH}:${CONDA_DIR}/bin

# Get Python packages for testing
${CONDA_DIR}/bin/pip install \
    --user \
    argparse \
    click \
    coverage \
    codecov \
    pycodestyle \
    requests \
    sphinx \
    sphinx_autodoc_typehints \
    sphinx_rtd_theme \
    tabulate

export PIP_INSTALL_OPTS="--no-color"
if [[ $TRAVIS_OS_NAME == "osx" ]]; then
    export PIP_INSTALL_OPTS="--user"
fi

${CONDA_DIR}/bin/pip install \
    ${PIP_INSTALL_OPTS} \
        pytest \
        pytest-cov
