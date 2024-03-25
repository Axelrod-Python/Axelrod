Running tests
=============

Basic test runners
------------------

The project has an extensive test suite which is run each time a new
contribution is made to the repository.  If you want to check that all the tests
pass before you submit a pull request you can run the tests yourself::

    $ python -m tox

This will run the entire test suite in an isolated environment for all currently
supported versions of Python.

If you are developing new tests for the suite, it is useful to run a single test
file so that you don't have to wait for the entire suite each time.  For
example, to run only the tests for the Grudger strategy::

    $ python -m pytest axelrod/tests/strategies/test_grudger.py

The test suite is divided into three categories: strategy tests, unit tests and integration tests.
Each can be run individually::

    $ python -m pytest axelrod/tests/strategies/
    $ python -m pytest axelrod/tests/unit/
    $ python -m pytest axelrod/tests/integration/


Testing coverage of tests
-------------------------

The library has 100% test coverage. This can be tested using the Python
:code:`coverage` package. Once installed (:code:`pip install coverage`), to run
the tests and check the coverage for the entire library::

    $ coverage run --source=axelrod -m pytest .

You can then view a report of the coverage::

    $ coverage report -m

You can also run the coverage on a subset of the tests. For example, to run the
tests with coverage for the Grudger strategy::

    $ coverage run --source=axelrod -m pytest axelrod/tests/strategies/test_grudger.py


Testing the documentation
-------------------------

The documentation is doctested, to run those tests you can run
the script::

    $ python doctests.py

You can also run the doctests on any given file. For example, to run the
doctests for the :code:`docs/tutorials/getting_started/match.rst` file::

    $ python -m doctest docs/tutorials/getting_started/match.rst
