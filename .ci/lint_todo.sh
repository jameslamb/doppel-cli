#!/bin/bash

# [description]
#     Lint all code for TODO comments
# [usage]
#     ./.ci/lint_todo.sh $(pwd)

SOURCE_DIR=${1}

# failure is a natural part of life
set -e

echo ""
echo "Checking code for TODO comments..."
echo ""

todo_count=$(git grep -i -E '(#|(/\*))+\s*todo[\s|:|$]?' | wc -l)
exit ${todo_count}

echo ""
echo "Done checking code for TODO comments."
echo ""
