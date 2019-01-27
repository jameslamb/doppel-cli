
# Failure is a natural part of life
set -e

# Set up environment variables
CRAN_MIRROR=http://cran.rstudio.com

# Install conda
wget ${MINICONDA_INSTALLER} -O miniconda.sh;
bash miniconda.sh -b -p $HOME/miniconda
export PATH="$HOME/miniconda/bin:$PATH"
hash -r
conda config --set always_yes yes --set changeps1 no
conda update -q conda
conda info -a

# Set up R (gulp)
conda install -c r \
    r \
    r-argparse \
    r-jsonlite \
    r-r6 

# Get packages for testing
Rscript -e "install.packages('futile.logger', repos = '${CRAN_MIRROR}')"
pip install \
    argparse \
    coverage \
    codecov \
    pycodestyle \
    sphinx \
    sphinx_autodoc_typehints
