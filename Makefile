noop:
	@true

.PHONY: noop

requirements:
	pip install -r requirements.txt
	pip install -r test_requirements.txt


develop: requirements
	python setup.py develop

pytest:
	py.test --cov nameko test --cov-report term-missing

flake8:
	flake8 nameko test

pylint:
	pylint nameko -E

test: pytest pylint flake8

full-test: requirements test
