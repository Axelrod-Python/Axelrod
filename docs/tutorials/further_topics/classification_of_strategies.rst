.. _classification-of-strategies:

Classification of strategies
============================

Due to the large number of strategies, every class and instance of the class has
a :code:`classifier` attribute which classifies that strategy according to
various dimensions.

Here is the :code:`classifier` for the :code:`Cooperator` strategy::

    >>> import axelrod as axl
    >>> expected_dictionary = {'manipulates_state': False, 'makes_use_of': set([]), 'stochastic': False, 'manipulates_source': False, 'inspects_source': False, 'memory_depth': 0}  # Order of this dictionary might be different on your machine
    >>> axl.Cooperator.classifier == expected_dictionary
    True

Note that instances of the class also have this classifier::

    >>> s = axl.Cooperator()
    >>> s.classifier == expected_dictionary
    True

This allows us to, for example, quickly identify all the stochastic
strategies::

    >>> len([s for s in axl.strategies if s().classifier['stochastic']])
    39

Or indeed find out how many strategy only use 1 turn worth of memory to
make a decision::

    >>> len([s for s in axl.strategies if s().classifier['memory_depth']==1])
    18

We can also identify strategies that make use of particular properties of the
tournament. For example, here is the number of strategies that  make use of the
length of each match of the tournament::

    >>> len([s() for s in axl.strategies if 'length' in s().classifier['makes_use_of']])
    10

Here are how many of the strategies that make use of the particular game being
played (whether or not it's the default Prisoner's dilemma)::

    >>> len([s() for s in axl.strategies if 'game' in s().classifier['makes_use_of']])
    21

Similarly, strategies that :code:`manipulate_source`, :code:`manipulate_state`
and/or :code:`inspect_source` return :code:`False` for the :code:`obey_axelrod`
function::

    >>> s = axl.MindBender()
    >>> axl.obey_axelrod(s)
    False
    >>> s = axl.TitForTat()
    >>> axl.obey_axelrod(s)
    True
