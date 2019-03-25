#!/bin/bash

# Install R and Python packages designed just to
# test doppel-cli

TEST_PKG_DIR=$(pwd)/integration_tests/test-packages
R_TEST_PKG_DIR=${TEST_PKG_DIR}/r
PYTHON_TEST_PKG_DIR=${TEST_PKG_DIR}/python

echo ""
echo "installing test R packages..."
echo ""

for pkg in $(ls ${R_TEST_PKG_DIR}); do
    echo ""
    echo "Installing package '${pkg}'"
    echo ""
    pushd ${R_TEST_PKG_DIR}/${pkg}
        Rscript -e "devtools::document()"
        R CMD install \
            --no-docs \
            --clean \
            --no-multiarch \
            .
    popd
    echo ""
    echo "Done"
    echo ""
done

echo ""
echo "installing test python packages..."
echo ""

for pkg in $(ls ${PYTHON_TEST_PKG_DIR}); do
    echo ""
    echo "Installing package '${pkg}'"
    echo ""
    pushd ${PYTHON_TEST_PKG_DIR}/${pkg}
        python setup.py install --user
    popd
    echo ""
    echo "Done"
    echo ""
done
