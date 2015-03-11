Contributing
============

All contributions to this repository are welcome via pull request on the `github repository <https://github.com/drvinceknight/Axelrod>`_.

The project follows the following guidelines:

1. Use the base Python library unless completely necessary.
2. If a non base Python library is deemed necessary, it should not hinder the running or contribution of the package when using the base Python library.
   For example, the `matplotlib library <http://matplotlib.org/>`_ is used in a variety of classes to be able to show results, such as this one:
   This has been done carefully with tests that are skipped if the library is not installed and also without any crashes if something using the library was run.
3. Try as best as possible to follow `PEP8 <https://www.python.org/dev/peps/pep-0008/>`_ which includes *using descriptive variable names*.
4. Testing: the project uses the `unittest <https://docs.python.org/2/library/unittest.html>`_ library and has a nice testing suite that makes some things very easy to write tests for.

The rest of this page will consider two aspects:

1. Contributing strategies
2. Contributing to the library itself
