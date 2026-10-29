# pytest-deadfixtures

[![PyPI - Version](https://img.shields.io/pypi/v/pytest-deadfixtures.svg)](https://pypi.org/project/pytest-deadfixtures)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pytest-deadfixtures.svg)](https://pypi.org/project/pytest-deadfixtures)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/jllorencetti/pytest-deadfixtures/main.svg)](https://results.pre-commit.ci/latest/github/jllorencetti/pytest-deadfixtures/main)

----

A simple plugin to list unused or duplicated fixtures in a pytest suite.

## Features

- List unused fixtures in your tests
- List duplicated fixtures
- Ignore specific fixtures from analysis with `@deadfixtures_ignore`

## Installation

Install `pytest-deadfixtures` from [PyPI](https://pypi.org/project/pytest-deadfixtures/):

```console
pip install pytest-deadfixtures
```

## Usage

### Important

The `--dead-fixtures` option does not run your tests and can also be sensitive to
errors during the pytest collection step. If using it in CI, run it after the
normal test run:

```yaml
script:
  - pytest
  - pytest --dead-fixtures
```

### Listing unused fixtures

Run pytest with the `--dead-fixtures` option:

```console
pytest --dead-fixtures
```

```text
Hey there, I believe the following fixture(s) are not being used:
Fixture name: some_fixture, location: test_write_docs_when_verbose.py:5

no tests ran
```

Use verbosity to include fixture docstrings in the report:

```console
pytest --dead-fixtures -v
```

### Listing repeated fixtures

The `--dup-fixtures` option compares fixture return values to find possible
duplicates. Fixtures without a truthy return value are skipped. Treat the report
as a hint and verify that the fixtures provide the same functionality before
removing one.

Unlike `--dead-fixtures`, this option runs the tests:

```console
pytest --dup-fixtures
```

```text
tests/test_deadfixtures.py ........

You may have some duplicate fixtures:
Fixture name: someclass_fixture, location: test_repeated_fixtures.py:12
Fixture name: someclass_samefixture, location: test_repeated_fixtures.py:17
```

### Ignoring specific fixtures

Use the `@deadfixtures_ignore` decorator to exclude a fixture from the analysis:

```python
import pytest

from pytest_deadfixtures import deadfixtures_ignore


@pytest.fixture
@deadfixtures_ignore
def intentionally_unused_fixture():
    """This fixture won't be reported as unused."""
    return "something"
```

To see which fixtures are ignored, use `--show-ignored-fixtures`:

```console
pytest --dead-fixtures --show-ignored-fixtures
```

```text
No unused fixtures found. Great job!

Ignored fixture(s) 1:
Fixture name: intentionally_unused_fixture, location: conftest.py:10
```

## Projects using it

- [wemake-django-template](https://github.com/wemake-services/wemake-django-template)
- [fands.dev django template](https://github.com/fandsdev/django)

## Contributing

Contributions are welcome. Run the tests with [`hatch test`](https://hatch.pypa.io/latest/cli/reference/#hatch-test)
and check the code with [`hatch check code`](https://hatch.pypa.io/latest/cli/reference/#hatch-check)
before submitting a pull request.

## License

Distributed under the terms of the [MIT License](http://opensource.org/licenses/MIT).
`pytest-deadfixtures` is free and open source software.

## Issues

If you encounter any problems, [file an issue](https://github.com/jllorencetti/pytest-deadfixtures/issues)
with a detailed description.
