.PHONY: format
format:
	black --line-length 100 .

.PHONY: lint
lint:
	./.ci/lint-py.sh $$(pwd)

.PHONY: test
test:
	./.ci/test.sh
