.. _getting-started:

Installation
============

The library requires Python 3.5.

The simplest way to install the package is to obtain it from the PyPi
repository::

    $ pip install axelrod

If you want to have access to the manual Human strategy for interactive play, use the following command to also install `prompt_toolkit`::

    $ pip install axelrod[Human]

You can also build it from source if you would like to::

    $ git clone https://github.com/Axelrod-Python/Axelrod.git
    $ cd Axelrod
    $ python setup.py install
