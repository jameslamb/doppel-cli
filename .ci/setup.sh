
# Failure is a natural part of life
set -e

# Set up environment variables
export CRAN_MIRROR=http://cran.rstudio.com
export CONDA_DIR=${HOME}/miniconda3

# Install conda
wget ${MINICONDA_INSTALLER} -O miniconda.sh;
bash miniconda.sh -b -p ${CONDA_DIR}
export PATH="${CONDA_DIR}/bin:$PATH"
echo "export PATH=${CONDA_DIR}/bin:$PATH" >> ${HOME}/.bashrc

hash -r
${CONDA_DIR}/bin/conda config --set always_yes yes --set changeps1 no
${CONDA_DIR}/bin/conda update -q conda
${CONDA_DIR}/bin/conda info -a

# Set up R (gulp)
${CONDA_DIR}/bin/conda install -c r \
    r \
    r-argparse \
    r-jsonlite \
    r-r6 

# Get packages for testing
Rscript -e "install.packages('futile.logger', repos = '${CRAN_MIRROR}')"
pip install \
    --user \
    argparse \
    click \
    coverage \
    codecov \
    pycodestyle \
    sphinx \
    sphinx_autodoc_typehints \
    sphinx_rtd_theme \
    tabulate
