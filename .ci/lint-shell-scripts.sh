#!/bin/bash

set -euo pipefail

echo "linting shell scripts with shellcheck"

shell_scripts=$(
    git ls-files \
    | grep -E "\.sh$"
)

# shellcheck disable=SC2086
shellcheck \
    --color=never \
    --format=gcc \
    $shell_scripts

echo "done running shellcheck"
