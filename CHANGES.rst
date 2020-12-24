Changelog
---------

3.0.0
~~~~~

* Drop support for Python 3.5
* Add support for Python 3.8 and 3.9

2.2.1
~~~~~

* Support for dinamically generated fixtures

2.2.0
~~~~~

* Group fixtures in report
* Add compatibility with pytest >= 5.4.0

2.1.0
~~~~~

* Ignore fixtures from `dist-packages`
* Fix compatibility with latest pytest version

2.0.1
~~~~~

* Fix duplicated fixtures headline always being printed

2.0.0
~~~~~

* Return non-zero exit code if unused fixtures are detected

1.0.1
~~~~~

* Fix false-positive report of used fixtures caused by a premature return

1.0.0
~~~~~

* Ignore fixtures from third-party packages

0.3.0
~~~~~

* Add an option to list duplicated fixtures

0.2.2
~~~~~

* Remove docs folder, the README file should be enough
* Fix typo in README

0.2.1
~~~~~

* Fix compatibility with pypy

0.2.0
~~~~~

* Extend support to pytest >= 3.0.0
* Use the verbosity arg to decide to print or not the fixtures docstrings
* Remove the green color when logging unused fixtures
* Minor improvements to README

0.1.0
~~~~~

* First release
