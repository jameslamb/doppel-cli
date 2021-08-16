#!/bin/bash

# [description]
#     Install R and Python packages designed just to
#     test doppel-cli
# [usage]
#    ./.ci/install_test_packages.sh

# failure is a natural part of life
set -eo pipefail

TEST_PKG_DIR="$(pwd)/integration_tests/test-packages"
R_TEST_PKG_DIR="${TEST_PKG_DIR}/r"
PYTHON_TEST_PKG_DIR="${TEST_PKG_DIR}/python"

echo ""
echo "installing test R packages..."
echo ""

if [[ "$OS_NAME" != "windows-latest" ]]; then
    for pkg in $(ls "${R_TEST_PKG_DIR}"); do
        echo ""
        echo "Installing package '${pkg}'"
        echo ""
        pushd "${R_TEST_PKG_DIR}/${pkg}"
            Rscript --vanilla -e "roxygen2::roxygenize()"
            R CMD INSTALL \
                --no-docs \
                --no-multiarch \
                --clean \
                .
        popd
        echo ""
        echo "Done"
        echo ""
    done
else
    echo "R is not installed, skipping installation of R packages"
fi

echo ""
echo "installing test python packages..."
echo ""

for pkg in $(ls "${PYTHON_TEST_PKG_DIR}"); do
    echo ""
    echo "Installing package '${pkg}'"
    echo ""
    pushd "${PYTHON_TEST_PKG_DIR}/${pkg}"
        python setup.py install --user
    popd
    echo ""
    echo "Done"
    echo ""
done
