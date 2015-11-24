Using the command line tool
===========================

Once :code:`axelrod` is installed you have access to a `run_axelrod` script that
can help run some of the tournaments, including the tournament that involves all
of the strategies from the library. You can view them at `Axelrod-Python/tournament on GitHub <https://github.com/Axelrod-Python/tournament/>`_

To view the help for the :code:`run_axelrod` file run::

    $ run_axelrod.py -h

Note that if you have not installed the package you can still use this script
directly from the repository::

    $ python run_axelrod -h

There is a variety of options that include:

- Excluding certain strategy sets.
- Not running the ecological variant.
- Running the rounds of the tournament in parallel.
- Include background noise

Particular parameters can also be changed:

- The output directory for the plot and csv files.
- The number of turns and repetitions for the tournament.
- The format of created images

Here is a command that will run the whole tournament, excluding the strategies
that do not obey Axelrod's original rules and using all available CPUS (this can
take quite a while!)::

    $ run_axelrod --xc -p 0

Here are some of the plots that are output when running with the latest total number of strategies:

The results from the tournament itself (ordered by median score):

.. raw:: html

   <img src="http://axelrod-python.github.io/tournament/assets/strategies_boxplot.svg" style="width: 50%; align: center">

This is just a brief overview of what the tool can do, take a look at the help
to see all the options.
