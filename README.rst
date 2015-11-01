.. image:: https://badge.waffle.io/Axelrod-Python/Axelrod.svg?label=ready&title=Ready
    :target: https://waffle.io/Axelrod-Python/Axelrod

.. image:: https://coveralls.io/repos/Axelrod-Python/Axelrod/badge.svg
    :target: https://coveralls.io/r/Axelrod-Python/Axelrod

.. image:: https://img.shields.io/pypi/v/Axelrod.svg
    :target: https://pypi.python.org/pypi/Axelrod

.. image:: https://travis-ci.org/Axelrod-Python/Axelrod.svg?branch=packaging
    :target: https://travis-ci.org/Axelrod-Python/Axelrod

|Join the chat at https://gitter.im/Axelrod-Python/Axelrod|

Axelrod
=======

A repository with the following goals:

1. To enable the reproduction of previous Iterated Prisoner's Dilemma research as easily as possible.
2. To produce the de-facto tool for any future Iterated Prisoner's Dilemma research.
3. To provide as simple a means as possible for anyone to define and contribute
   new and original Iterated Prisoner's Dilemma strategies.

**Please contribute strategies via pull request (or just get in touch
with us).**

For an overview of how to use and contribute to this repository, see the
documentation: http://axelrod.readthedocs.org/

If you do use this library for your personal research we would love to hear
about it: please do add a link at the bottom of this README file (PR's welcome
or again, just let us know) :) If there is something that is missing in this
library and that you would like implemented so as to be able to carry out a
project please open an issue and let us know!

Installation
============

The simplest way to install is::

    $ pip install axelrod

Otherwise::

    $ git clone https://github.com/Axelrod-Python/Axelrod.git
    $ cd Axelrod
    $ python setup.py install

You might need to install the libraries in `requirements.txt`::

    pip install -r requirements.txt

Note that on Ubuntu [some
users](https://github.com/Axelrod-Python/Axelrod/issues/309) have had problems
installing matplotlib. This seems to help with that::

    sudo apt-get install libfreetype6-dev
    sudo apt-get install libpng12-0-dev

Usage
-----

The full documentation can be found here:
`axelrod.readthedocs.org/ <http://axelrod.readthedocs.org/>`__.

The documentation includes details of how to setup a tournament but here is an
example showing how to create a tournament with all stochastic strategies::

    import axelrod
    strategies = [s() for s in axelrod.ordinary_strategies if s().classifier['stochastic']]
    tournament = axelrod.Tournament(strategies)
    results = tournament.play()

The :code:`results` object now contains all the results we could need::

    print(results.ranked_names)

gives::

    ['Meta Hunter', 'Inverse', 'Forgetful Fool Me Once', 'GTFT: 0.33', 'Champion', 'ZD-GTFT-2', 'Eatherley', 'Math Constant Hunter', 'Random Hunter', 'Soft Joss: 0.9', 'Meta Majority', 'Nice Average Copier', 'Feld', 'Meta Minority', 'Grofman', 'Stochastic WSLS', 'ZD-Extort-2', 'Tullock', 'Joss: 0.9', 'Arrogant QLearner', 'Average Copier', 'Cautious QLearner', 'Hesitant QLearner', 'Risky QLearner', 'Random: 0.5', 'Meta Winner']


Results
=======

A tournament with the full set of strategies from the library can be found at
https://github.com/Axelrod-Python/tournament. Here is the latest graphical
version of the results:

.. image:: http://axelrod-python.github.io/tournament/assets/strategies_boxplot.svg

.. image:: http://axelrod-python.github.io/tournament/assets/strategies_winplot.svg

See the [tournament repository](https://github.com/Axelrod-Python/tournament)
for many additional plots.

Contributing
============

All contributions are welcome, with a particular emphasis on
contributing further strategies.

You can find helpful instructions about contributing in the
documentation:
http://axelrod.readthedocs.org/en/latest/tutorials/contributing/index.html

.. image:: https://graphs.waffle.io/Axelrod-Python/Axelrod/throughput.svg
 :target: https://waffle.io/Axelrod-Python/Axelrod/metrics
  :alt: 'Throughput Graph'

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

.. |Join the chat at https://gitter.im/Axelrod-Python/Axelrod| image:: https://badges.gitter.im/Join%20Chat.svg
   :target: https://gitter.im/Axelrod-Python/Axelrod?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge
