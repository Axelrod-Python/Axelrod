Getting started
===============

lipsum


Installation
------------

The simplest way to install the package is to obtain it from the PyPi
repository::

    $ pip install axelrod


You can also build it from source if you would like to::

    $ git clone https://github.com/Axelrod-Python/Axelrod.git
    $ cd Axelrod
    $ python setup.py install


Creating and running a simple tournament
----------------------------------------

The following lines of code create a simple list of strategies::

    >>> import axelrod
    >>> strategies = [s() for s in axelrod.demo_strategies]
    >>> strategies
    [Cooperator, Defector, Tit For Tat, Grudger, Random: 0.5]

We can now create a tournament, play it, saving the results and viewing the
ranks of each player::

    >>> tournament = axelrod.Tournament(strategies)
    >>> results = tournament.play()
    >>> results.ranked_names
    ['Defector', 'Grudger', 'Tit For Tat', 'Cooperator', 'Random: 0.5']

We can also plot these results (which helps visualise the stochastic effects)::

    >>> plot = axelrod.Plot(results)
    >>> p = plot.boxplot()
    >>> p.show()

.. image:: _static/getting_started/demo_strategies_boxplot.svg
   :width: 50%
   :align: center
