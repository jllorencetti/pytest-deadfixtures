clear:
	rm -rf dist/
	rm -rf *.egg-info

test-release: clear
	python setup.py sdist upload -r pypitest

release: clear
	git tag `python setup.py -q version`
	git push origin `python setup.py -q version`
	python setup.py sdist upload -r pypi
