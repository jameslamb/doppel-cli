#!/bin/bash

shell_scripts=$(git ls-files | grep -E '\.sh$')

for f in ${shell_scripts}; do
    echo "checking ${f}..."
    shellcheck \
        --norc \
        --exclude=SC2002,SC2045 \
            ${f} \
    || exit 1
done
