clear:
	rm -rf dist/
	rm -rf *.egg-info

format:
	black .

lint:
	pre-commit run -a -v

test:
	pip install .
	pytest

test-release: clear
	python setup.py sdist bdist_wheel upload -r pypitest

release: clear
	git tag `python setup.py -q version`
	git push origin `python setup.py -q version`
	python setup.py sdist bdist_wheel upload -r pypi

setup:
	pip install -U -r requirements-dev.txt
