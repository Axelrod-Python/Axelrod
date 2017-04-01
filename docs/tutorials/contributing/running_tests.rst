Running tests
=============

Basic test runners
------------------

The project has an extensive test suite which is run each time a new
contribution is made to the repository.  If you want to check that all the tests
pass before you submit a pull request you can run the tests yourself::

    $ python -m unittest discover

If you are developing new tests for the suite, it is useful to run a single test
file so that you don't have to wait for the entire suite each time.  For
example, to run only the tests for the Grudger strategy::

    $ python -m unittest axelrod.tests.strategies.test_grudger

The test suite is divided into three categories: strategy tests, unit tests and integration tests.
Each can be run individually::

    $ python -m unittest discover -s axelrod.tests.strategies
    $ python -m unittest discover -s axelrod.tests.unit
    $ python -m unittest discover -s axelrod.tests.integration


Testing coverage of tests
-------------------------

The library has 100% test coverage. This can be tested using the Python
:code:`coverage` package. Once installed (:code:`pip install coverage`), to run
the tests and check the coverage for the entire library::

    $ coverage run --source=axelrod -m unittest discover

You can then view a report of the coverage::

    $ coverage report -m

You can also run the coverage on a subset of the tests. For example, to run the
tests with coverage for the Grudger strategy::

    $ coverage run --source=axelrod -m unittest axelrod.tests.strategies.test_grudger


Testing the documentation
-------------------------

The documentation is doctested, to run those tests you can run
the script::

    $ python doctests.py

You can also run the doctests on any given file. For example, to run the
doctests for the :code:`docs/tutorials/getting_started/match.rst` file::

    $ python -m doctest docs/tutorials/getting_started/match.rst


Type checking
-------------

The library makes use of type hinting, this can be checked using the Python
:code:`mypy` package. Once installed (:code:`pip install mypy`), to run the type checker::

    $ python run_mypy.py

You can also run the type checker on a given file. For example, to run the type
checker on the Grudger strategy::

    $ mypy --ignore-missing-imports --follow-imports skip axelrod/strategies/grudger.py


Continuous integration
======================

This project is being taken care of by `travis-ci
<https://travis-ci.org/>`_, so all tests will be run automatically when opening
a pull request.  You can see the latest build status `here
<https://travis-ci.org/Axelrod-Python/Axelrod>`_.
