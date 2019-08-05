
# Failure is a natural part of life
set -e

# Set up environment variables
export CRAN_MIRROR=http://cran.rstudio.com

# Install conda
wget ${MINICONDA_INSTALLER} -O miniconda.sh;
bash miniconda.sh -b -p ${CONDA_DIR}
echo "export PATH=${CONDA_DIR}/bin:$PATH" >> ${HOME}/.bashrc

hash -r
${CONDA_DIR}/bin/conda config --set always_yes yes --set changeps1 no
${CONDA_DIR}/bin/conda update -q conda
${CONDA_DIR}/bin/conda info -a

# Set up R (gulp)
${CONDA_DIR}/bin/conda install -c r \
    r-base \
    r-jsonlite \
    r-lintr \
    r-r6

# Per https://github.com/ContinuumIO/anaconda-issues/issues/9423#issue-325303442,
# packages that require compilation may fail to find the
# gcc bundled with conda
export PATH=${PATH}:${CONDA_DIR}/bin

# Get packages for testing
${CONDA_DIR}/bin/Rscript -e "install.packages(c('argparse', 'covr', 'futile.logger', 'roxygen2'), repos = '${CRAN_MIRROR}')"
${CONDA_DIR}/bin/pip install \
    argparse \
    click \
    coverage \
    codecov \
    pycodestyle \
    pytest \
    pytest-cov \
    sphinx \
    sphinx_autodoc_typehints \
    sphinx_rtd_theme \
    tabulate
