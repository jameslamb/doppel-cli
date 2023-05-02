.PHONY: build
build:
	rm -r ./dist || true
	rm -r ./doppel/doppel_cli.egg-info || true
	pipx run build --wheel

.PHONY: check-wheels
check-dists:
	gunzip -t dist/*.tar.gz
	zip -T dist/*.whl
	check-wheel-contents dist/*.whl
	pydistcheck dist/*
	pyroma --min=10 dist/*.tar.gz
	twine check --strict dist/*

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
