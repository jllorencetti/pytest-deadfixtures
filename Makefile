.PHONY: clean format lint test build

clean:
	rm -rf dist/ *.egg-info

format:
	hatch run fmt

lint:
	hatch check code

test:
	hatch run pytest

build:
	hatch build
