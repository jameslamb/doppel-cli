
# Failure is a natural part of life
set -e

# Set up environment variables
CRAN_MIRROR=http://cran.rstudio.com
CONDA_DIR=$HOME/miniconda

# Install conda
wget ${MINICONDA_INSTALLER} -O miniconda.sh;
bash miniconda.sh -b -p ${CONDA_DIR}
export PATH="${CONDA_DIR}/bin:$PATH"

alias conda=${CONDA_DIR}/bin/conda
hash -r
conda config --set always_yes yes --set changeps1 no
conda update -q conda
conda info -a

# Set up R (gulp)
${CONDA_DIR}/bin/conda install -c r \
    r \
    r-argparse \
    r-jsonlite \
    r-r6 

# Get packages for testing
Rscript -e "install.packages('futile.logger', repos = '${CRAN_MIRROR}')"
pip install \
    argparse \
    click \
    coverage \
    codecov \
    pycodestyle \
    sphinx \
    sphinx_autodoc_typehints \
    sphinx_rtd_theme \
    tabulate
