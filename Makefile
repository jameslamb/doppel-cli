.PHONY: format
format:
	black --line-length 100 .

.PHONY: lint
lint:
	./.ci/lint-py.sh $$(pwd)
	./.ci/lint-shell-scripts.sh
