.PHONY: test

test:
	flake8 --max-complexity 5 src
	mypy --ignore-missing-imports src
	bandit -r src
	python -m unittest discover src/kbase_workspace_utils/test/
