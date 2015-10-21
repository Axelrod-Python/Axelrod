.. _classification-of-strategies:

Classification of strategies
============================

Due to the large number of strategies, every class and instance of the class has
a :code:`classifier` attribute which classifies that strategy according to
various dimensions.

Here is the :code:`classifier` for the :code:`Cooperator` strategy::

    >>> import axelrod as axl
    >>> expected_dictionary = {'manipulates_state': False, 'stochastic': False, 'manipulates_source': False, 'inspects_source': False, 'memory_depth': 0}  # Order of this dictionary might be different on your machine
    >>> axl.Cooperator.classifier == expected_dictionary
    True

Note that instances of the class also have this classifier::

    >>> s = axl.Cooperator()
    >>> s.classifier == expected_dictionary
    True

This allows us to, for example, quickly identify all the stochastic
strategies::

    >>> len([s for s in axl.strategies if s().classifier['stochastic']])
    31

Or indeed find out how many strategy have only use 1 turn worth of memory to
make a decision:

    >>> len([s for s in axl.strategies if s().classifier['memory_depth']==1])
    15

Similarly, strategies that :code:`manipulate_source`, :code:`manipulate_state`
and/or :code:`inspect_source` return :code:`False` for the :code:`obey_axelrod`
function::

    >>> s = axl.MindBender()
    >>> axl.obey_axelrod(s)
    False
    >>> s = axl.TitForTat()
    >>> axl.obey_axelrod(s)
    True
