===================
pytest-deadfixtures
===================

.. image:: https://travis-ci.org/jllorencetti/pytest-deadfixtures.svg?branch=master
    :target: https://travis-ci.org/jllorencetti/pytest-deadfixtures
    :alt: See Build Status on Travis CI

A simple plugin to list unused fixtures in a pytest suite.

----

Features
--------

* List unused fixtures in your tests


Installation
------------

You can install "pytest-deadfixtures" via `pip`_ from `PyPI`_::

    $ pip install pytest-deadfixtures

Usage
-----

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
