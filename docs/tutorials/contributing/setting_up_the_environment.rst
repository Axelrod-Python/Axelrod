Setting up the environment
==========================

Installing all dependencies
---------------------------

All dependencies can be installed by running::

  $ pip install -r requirements.txt

It is recommended to do this using a virtual environment tool of your choice.

For example, when using the virtual environment library :code:`venv`::

  $ python -m venv axelrod_development
  $ source axelrod_development/bin/activate
  $ pip install -r requirements.txt

The git workflow
----------------

There are two important branches in this repository:

- :code:`dev`: The most up to date branch with no failing tests.
  This is the default branch on github.
- :code:`release`: The latest release.

When working on a new contribution branch from the latest :code:`dev` branch and
open a Pull Request on github from your branch to the :code:`dev` branch.

The procedure for a new release (this is carried out by one of core maintainers):

1. Create a Pull Request from :code:`dev` to :code:`release` which should
   include an update to :code:`axelrod/version.py` and :code:`CHANGES.md`
2. Create a git tag.
3. Push to github.
4. Create a release on github.
5. Push to PyPi: :code:`python setup.py sdist bdist_wheel upload`
