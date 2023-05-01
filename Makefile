.PHONY: format
format:
	isort .
	black .

.PHONY: lint
lint:
	black \
		--check \
		.
	flake8 .
	mypy ./doppel
	pylint ./doppel
