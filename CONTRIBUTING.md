# Contributing

Contributions are welcome! If you find a bug or have an idea for an improvement,
please [open an issue](https://github.com/jllorencetti/pytest-deadfixtures/issues)
before starting work on a larger change. For small fixes, you can open a pull
request directly.

## Development setup

The project requires Python 3.10 or later and uses [Hatch](https://hatch.pypa.io/)
to manage its development environments. Install Hatch, then clone the repository:

```console
pipx install hatch
git clone https://github.com/jllorencetti/pytest-deadfixtures.git
cd pytest-deadfixtures
```

## Tests and checks

Run the test suite with coverage:

```console
hatch test --cover
```

To run tests for one Python and pytest version, for example Python 3.13 and
pytest 9.2:

```console
hatch test -i py=3.13 -i pytest=9.2 --cover
```

Check lint and formatting before submitting your changes:

```console
hatch check code
hatch check fmt
```

The CI workflow runs these checks and tests across the supported Python
implementations and pytest versions.

## Pull requests

- Keep changes focused and explain the user-visible reason for the change.
- Add or update tests when changing behavior.
- Update the README or changelog when the user-facing behavior or supported
  versions change.
- Make sure the tests and checks above pass, and describe the validation in
  your pull request.
