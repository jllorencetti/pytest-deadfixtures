# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Added support for Python 3.15.
- Added a GitHub Actions workflow to build distributions and publish them to PyPI when a release is published.
- Added Christian Hartung (@hartungstenio) as a project maintainer.

### Changed

- Moved the pytest plugin implementation into `pytest_deadfixtures.plugin`.
- Migrated package building and development environments to Hatch.
- Moved the package implementation into a `src/` layout.
- Set up a Hatch test matrix for pytest 9.0, 9.1, and 9.2 across supported Python versions.
- Replaced the previous linting tools with Ruff.
- Converted the README to Markdown and added project status badges.

### Removed

- Dropped support for Python 3.10.
- Dropped support for pytest 7 and 8.

## [3.1.0] - 2026-01-15

### Added

- Added the `deadfixtures_ignore` decorator to exclude specific fixtures from being reported as unused.

## [3.0.0] - 2025-10-23

### Added

- Added support for Python 3.8 and 3.9.

### Removed

- Dropped support for Python 3.5.

## [2.2.1] - 2020-07-23

### Added

- Added support for dynamically generated fixtures.

## [2.2.0] - 2020-03-14

### Added

- Added compatibility with pytest 5.4 and later.

### Changed

- Grouped fixtures in the report.

## [2.1.0] - 2018-11-05

### Changed

- Ignored fixtures from `dist-packages`.

### Fixed

- Fixed compatibility with the latest pytest version.

## [2.0.1] - 2018-04-27

### Fixed

- Fixed the duplicate fixtures headline always being printed.

## [2.0.0] - 2018-04-26

### Changed

- Return a non-zero exit code when unused fixtures are detected.

## [1.0.1] - 2018-04-04

### Fixed

- Fixed false-positive reports of used fixtures caused by a premature return.

## [1.0.0] - 2018-03-24

### Added

- Ignore fixtures from third-party packages.

## [0.3.0] - 2018-01-17

### Added

- Added an option to list duplicated fixtures.

## [0.2.2] - 2018-01-07

### Removed

- Removed the docs folder; the README is the project documentation.

### Fixed

- Fixed a typo in the README.

## [0.2.1] - 2018-01-07

### Fixed

- Fixed compatibility with PyPy.

## [0.2.0] - 2018-01-07

### Added

- Added compatibility with pytest 3.0 and later.

### Changed

- Use verbosity to decide whether fixture docstrings are printed.
- Removed green coloring when reporting unused fixtures.
- Made minor improvements.

## [0.1.0]

### Added

- First release.

[Unreleased]: https://github.com/jllorencetti/pytest-deadfixtures/compare/3.1.0...HEAD
[3.1.0]: https://github.com/jllorencetti/pytest-deadfixtures/compare/3.0.0...3.1.0
[3.0.0]: https://github.com/jllorencetti/pytest-deadfixtures/compare/2.2.1...3.0.0
[2.2.1]: https://github.com/jllorencetti/pytest-deadfixtures/compare/2.2.0...2.2.1
[2.2.0]: https://github.com/jllorencetti/pytest-deadfixtures/compare/2.1.0...2.2.0
[2.1.0]: https://github.com/jllorencetti/pytest-deadfixtures/compare/2.0.1...2.1.0
[2.0.1]: https://github.com/jllorencetti/pytest-deadfixtures/compare/2.0.0...2.0.1
[2.0.0]: https://github.com/jllorencetti/pytest-deadfixtures/compare/1.0.1...2.0.0
[1.0.1]: https://github.com/jllorencetti/pytest-deadfixtures/compare/1.0.0...1.0.1
[1.0.0]: https://github.com/jllorencetti/pytest-deadfixtures/compare/0.3.0...1.0.0
[0.3.0]: https://github.com/jllorencetti/pytest-deadfixtures/compare/0.2.2...0.3.0
[0.2.2]: https://github.com/jllorencetti/pytest-deadfixtures/compare/0.2.1...0.2.2
[0.2.1]: https://github.com/jllorencetti/pytest-deadfixtures/compare/0.2.0...0.2.1
[0.2.0]: https://github.com/jllorencetti/pytest-deadfixtures/releases/tag/0.2.0
