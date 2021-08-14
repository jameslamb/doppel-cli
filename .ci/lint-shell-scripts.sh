#!/bin/bash

set -euo pipefail

shell_scripts=$(
    git ls-files \
    | grep -E "\.sh$"
)

shellcheck \
    --color=never \
    --format=gcc \
    --exclude=SC2002 \
    $shell_scripts
