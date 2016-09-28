.. image:: https://coveralls.io/repos/Axelrod-Python/Axelrod/badge.svg
    :target: https://coveralls.io/r/Axelrod-Python/Axelrod

.. image:: https://img.shields.io/pypi/v/Axelrod.svg
    :target: https://pypi.python.org/pypi/Axelrod

.. image:: https://travis-ci.org/Axelrod-Python/Axelrod.svg?branch=packaging
    :target: https://travis-ci.org/Axelrod-Python/Axelrod

.. image:: https://zenodo.org/badge/19509/Axelrod-Python/Axelrod.svg
    :target: https://zenodo.org/badge/latestdoi/19509/Axelrod-Python/Axelrod

|Join the chat at https://gitter.im/Axelrod-Python/Axelrod|

Axelrod
=======

A library with the following principles and goals:

1. Enabling the reproduction of previous Iterated Prisoner's Dilemma research
   as easily as possible.
2. Creating the de-facto tool for future Iterated Prisoner's Dilemma
   research.
3. Providing as simple a means as possible for anyone to define and contribute
   new and original Iterated Prisoner's Dilemma strategies.
4. Emphasizing readability along with an open and welcoming community that
   is accommodating for developers and researchers of a variety of skill levels.

Currently the library contains well over 100 strategies and can perform a
variety of tournament types (RoundRobin, Noisy, Spatially-distributed, and
probabilistically ending) and population dynamics while taking advantage
of multi-core processors.

**Please contribute via pull request (or just get in touch with us).**

For an overview of how to use and contribute to this repository, see the
documentation: http://axelrod.readthedocs.org/

If you do use this library for your personal research we would love to hear
about it: please do add a link at the bottom of this README file (PR's welcome
or again, just let us know) :) If there is something that is missing in this
library and that you would like implemented so as to be able to carry out a
project please open an issue and let us know!

**Note: this library will be dropping support for python 2 on the 1st of
December 2017.**

Installation
============

The simplest way to install is::

    $ pip install axelrod

Otherwise::

    $ git clone https://github.com/Axelrod-Python/Axelrod.git
    $ cd Axelrod
    $ python setup.py install

Note that on Ubuntu `some
users <https://github.com/Axelrod-Python/Axelrod/issues/309>`_ have had problems
installing matplotlib. This seems to help with that::

    sudo apt-get install libfreetype6-dev
    sudo apt-get install libpng12-0-dev

Usage
-----

The full documentation can be found here:
`axelrod.readthedocs.org/ <http://axelrod.readthedocs.org/>`__.

The documentation includes details of how to setup a tournament but here is a
brief example showing how to get a simple tournament::

    >>> import axelrod as axl
    >>> axl.seed(0)  # Set a seed
    >>> players = [s() for s in axl.demo_strategies]  # Create players
    >>> tournament = axl.Tournament(players)  # Create a tournament
    >>> results = tournament.play()  # Play the tournament
    >>> results.ranked_names
    ['Defector', 'Grudger', 'Tit For Tat', 'Cooperator', 'Random: 0.5']


There is also a `notebooks repository
<https://github.com/Axelrod-Python/Axelrod-notebooks>`_ which shows further
examples of using the library.

Results
=======

A tournament with the full set of strategies from the library can be found at
https://github.com/Axelrod-Python/tournament. These results can be easily viewed
at http://axelrod-tournament.readthedocs.org.


Contributing
============

All contributions are welcome!

You can find helpful instructions about contributing in the
documentation:
http://axelrod.readthedocs.org/en/latest/tutorials/contributing/index.html

Example notebooks
=================

https://github.com/Axelrod-Python/Axelrod-notebooks contains a set of example
Jupyter notebooks.

Projects that use this library
==============================

If you happen to use this library for anything from a blog post to a research
paper please list it here:

- `A 2015 pedagogic paper on active learning
  <https://github.com/drvinceknight/Playing-games-a-case-study-in-active-learning>`_
  by `drvinceknight <https://twitter.com/drvinceknight>`_ published in `MSOR
  Connections <https://journals.gre.ac.uk/index.php/msor/about>`_: the library
  is mentioned briefly as a way of demonstrating repeated games.
- `A repository with various example tournaments and visualizations of strategies
  <https://github.com/marcharper/AxelrodExamples>`_
  by `marcharper <https://github.com/marcharper>`_.
- `Axelrod-Python related blog articles
  <http://www.thomascampbell.me.uk/category/axelrod.html>`_
  by `Uglyfruitcake <https://github.com/uglyfruitcake>`_.
- `Evolving strategies for an Iterated Prisoner's Dilemma tournament
  <http://mojones.net/evolving-strategies-for-an-iterated-prisoners-dilemma-tournament.html>`_
  by `mojones <https://github.com/mojones>`_.
- `An Exploratory Data Analysis of the Iterated Prisoner's Dilemma, Part I
  <http://marcharper.codes/2015-11-16/ipd.html>`_ and `Part II <http://marcharper.codes/2015-11-17/ipd2.html>`_
  by `marcharper <https://github.com/marcharper>`_.
- `Survival of the fittest: Experimenting with a high performing strategy in
  other environments
  <http://vknight.org/unpeudemath/gametheory/2015/11/28/Experimenting-with-a-high-performing-evolved-strategy-in-other-environments.html>`_
  by `drvinceknight <https://twitter.com/drvinceknight>`_
- `An open reproducible framework for the study of the iterated prisoner's
  dilemma <https://arxiv.org/abs/1604.00896>_`: a pre print of a paper describing this
  library (20 authors).

Contributors
============

The library has had many awesome contributions from many `great
contributors <https://github.com/Axelrod-Python/Axelrod/graphs/contributors>`_.
The Core developers of the project are:

- `drvinceknight`_
- `langner <https://github.com/langner>`_
- `marcharper <https://github.com/marcharper>`_
- `meatballs <https://github.com/meatballs>`_

.. |Join the chat at https://gitter.im/Axelrod-Python/Axelrod| image:: https://badges.gitter.im/Join%20Chat.svg
   :target: https://gitter.im/Axelrod-Python/Axelrod?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge
