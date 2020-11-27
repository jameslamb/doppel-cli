#!/bin/bash

# [description]
#     Lint all code for TODO comments
# [usage]
#     ./.ci/lint_todo.sh $(pwd)

# failure is a natural part of life
set -eu

echo ""
echo "Checking code for TODO comments..."
echo ""
todo_count=$(git grep -i -E '#+ *todo' | wc -l)
echo "TODOs found: ${todo_count}"
exit ${todo_count}

echo ""
echo "Done checking code for TODO comments."
echo ""
