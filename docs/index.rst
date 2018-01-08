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

Using some level of verbosity will also print the doc string of each fixture::

    $ pytest --dead-fixtures -v

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

.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`@jllorencetti`: https://github.com/jllorencetti
.. _`MIT`: http://opensource.org/licenses/MIT
.. _`cookiecutter-pytest-plugin`: https://github.com/pytest-dev/cookiecutter-pytest-plugin
.. _`file an issue`: https://github.com/jllorencetti/pytest-deadfixtures/issues
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`tox`: https://tox.readthedocs.io/en/latest/
.. _`pip`: https://pypi.python.org/pypi/pip/
.. _`PyPI`: https://pypi.python.org/pypi
