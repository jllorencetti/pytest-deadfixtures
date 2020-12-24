===================
pytest-deadfixtures
===================

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/python/black
    :alt: Black

.. image:: https://travis-ci.org/jllorencetti/pytest-deadfixtures.svg?branch=main
    :target: https://travis-ci.org/jllorencetti/pytest-deadfixtures
    :alt: See Build Status on Travis CI

A simple plugin to list unused or duplicated fixtures in a pytest suite.

----

Features
--------

* List unused fixtures in your tests
* List duplicated fixtures


Installation
------------

You can install "pytest-deadfixtures" via `pip`_ from `PyPI`_::

    $ pip install pytest-deadfixtures

Usage
-----

Important
*********

The `--dead-fixtures` option will not run your tests and it's also sensible for errors in the pytest collection step.
If you are using as part of you CI process the recommended way is to run it after the default test run. For example::

    script:
      - pytest
      - pytest --dead-fixtures


Listing unused fixtures
***********************

Just run 'pytest' with an extra option '--dead-fixtures'::

    $ pytest --dead-fixtures
    ============================= test session starts ==============================
    (hidden for brevity)

    Hey there, I believe the following fixture(s) are not being used:
    Fixture name: some_fixture, location: test_write_docs_when_verbose.py:5

    ========================= no tests ran in 0.00 seconds =========================

Using some level of verbosity will also print the docstring of each fixture::

    $ pytest --dead-fixtures -v
    ============================= test session starts ==============================
    (hidden for brevity)

    Hey there, I believe the following fixture(s) are not being used:
    Fixture name: some_fixture, location: test_write_docs_when_verbose.py:5
        Blabla fixture docs

    ========================= no tests ran in 0.00 seconds =========================

Listing repeated fixtures
*************************

Now that you removed every unused fixture of your test suite, what if you want to go an extra mile?

An important note about this is that it uses the fixture return value to verify if two or more fixtures are equal.

This means **fixtures without a truthy return value will be skipped**.

You should use this as a hint only, verify that the functionality provided by both fixtures are really repeated before deleting one of them.

Just run 'pytest' with an extra option '--dup-fixtures', unlike the '--dead-fixtures' option, it'll normally run you tests::

    $ pytest --dup-fixtures
    ======================================================================================================================== test session starts ========================================================================================================================
    (hidden for brevity)

    tests/test_deadfixtures.py ........

    You may have some duplicate fixtures:
    Fixture name: someclass_fixture, location: test_repeated_fixtures.py:12
    Fixture name: someclass_samefixture, location: test_repeated_fixtures.py:17


Projects using it
-----------------

- `wemake-django-template`_

Contributing
------------
Contributions are very welcome. Tests can be run with `tox`_, please ensure
the coverage at least stays the same before you submit a pull request.

License
-------

Distributed under the terms of the `MIT`_ license, 'pytest-deadfixtures' is free and open source software


Issues
------

If you encounter any problems, please `file an issue`_ along with a detailed description.

.. _`@jllorencetti`: https://github.com/jllorencetti
.. _`MIT`: http://opensource.org/licenses/MIT
.. _`file an issue`: https://github.com/jllorencetti/pytest-deadfixtures/issues
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`tox`: https://tox.readthedocs.io/en/latest/
.. _`pip`: https://pypi.python.org/pypi/pip/
.. _`PyPI`: https://pypi.python.org/pypi
.. _`wemake-django-template`: https://github.com/wemake-services/wemake-django-template
