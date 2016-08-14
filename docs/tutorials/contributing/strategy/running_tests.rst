Running tests
=============

The project has an extensive test suite which is run each time a new
contribution is made to the repository.  If you want to check that all the tests
pass before you submit a pull request you can run the tests yourself::

    $ python -m unittest discover

If you are developing new tests for the suite, it is useful to run a single test
file so that you don't have to wait for the entire suite each time.  For
example, to run only the tests for the Grudger strategy::

    $ python -m unittest axelrod.tests.unit.test_grudger

The test suite is divided into two categories: unit tests and integration tests.
Each can be run individually::

    $ python -m unittest discover -s axelrod.tests.unit
    $ python -m unittest discover -s axelrod.tests.integration

Furthermore the documentation is also doctested, to run those tests you can run
the script::

    $ python doctests.py

Note that this project is being taken care of by `travis-ci
<https://travis-ci.org/>`_, so all tests will be run automatically when opening
a pull request.  You can see the latest build status `here
<https://travis-ci.org/Axelrod-Python/Axelrod>`_.
