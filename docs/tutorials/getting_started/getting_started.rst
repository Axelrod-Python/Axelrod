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

If you do this you will need to also install the dependencies::

    $ pip install -r requirements.txt

Creating and running a simple tournament
----------------------------------------

The following lines of code create a simple list of strategies::

    >>> import axelrod as axl
    >>> strategies = [axl.Cooperator(), axl.Defector(),
    ...               axl.TitForTat(), axl.Grudger()]
    >>> strategies
    [Cooperator, Defector, Tit For Tat, Grudger]

We can now create a tournament, play it, saving the results and viewing the
ranks of each player::

    >>> tournament = axl.Tournament(strategies)
    >>> results = tournament.play()
    >>> results.ranked_names
    ['Defector', 'Tit For Tat', 'Grudger', 'Cooperator']

We can also plot these results (which helps visualise the stochastic effects)::

    >>> plot = axl.Plot(results)
    >>> p = plot.boxplot()
    >>> p.show()

.. image:: _static/getting_started/demo_deterministic_strategies_boxplot.svg
   :width: 50%
   :align: center
