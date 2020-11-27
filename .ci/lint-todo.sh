#!/bin/bash

# [description]
#     Lint all code for TODO comments
# [usage]
#     ./.ci/lint_todo.sh $(pwd)

# failure is a natural part of life
set -eou pipefail

SOURCE_DIR=${1}

echo ""
echo "Checking code for TODO comments..."
echo ""

todo_count=$(git grep --count -i -E '(#|(/\*))+\s*todo[\s|:|$]?')
echo "found ${todo_count} TODOs"
exit ${todo_count}

echo ""
echo "Done checking code for TODO comments."
echo ""
