#!/bin/bash

# [description]
#     Upload conda packages to Anaconda.org
# [usage]
#     ./.ci/conda-upload.sh $(pwd)/conda-uploads

UPLOAD_ARTIFACT_DIR=${1}

for platform in $(ls ${UPLOAD_ARTIFACT_DIR}); do
    echo "Uploading packages for platform '${platform}'"
    pushd ${UPLOAD_ARTIFACT_DIR}/${platform}
        for pkg_file in $(ls); do
            anaconda upload ${pkg_file}
        done
    popd
    echo "Done uploading packages for platform '${platform}'"
done
