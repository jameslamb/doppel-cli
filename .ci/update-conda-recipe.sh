#!/bin/bash

# [description]
#    Update the recipe for building doppel-cli on
#    conda-forge
# [usage]
#     GITHUB_USER="jameslamb"
#     ./.ci/update-conda-recipe.sh ${GITHUB_USER}

GITHUB_USER=${1}
DOPPEL_VERSION=$(cat doppel/VERSION)

TMP_DIR=$(pwd)/conda-install

pushd "${TMP_DIR}" || exit 1

    git "clone git@github.com:${GITHUB_USER}/doppel-cli-feedstock.git"

    cd doppel-cli-feedstock/recipe || exit 1

    RELEASE_BRANCH="release/v${DOPPEL_VERSION}"
    git checkout -b "${RELEASE_BRANCH}"
    grayskull pypi \
        --maintainers jameslamb \
        --output "$(pwd)" \
        doppel-cli

    mv doppel-cli/meta.yaml .
    rm -r doppel-cli

    git commit -m "Updated conda recipe to version ${DOPPEL_VERSION}"
    git push origin "${RELEASE_BRANCH}"

    echo "Done updating recipe! Changes are on branch '${RELEASE_BRANCH}'"

popd || exit 1
