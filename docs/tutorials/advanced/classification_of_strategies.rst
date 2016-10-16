.. _classification-of-strategies:

Classification of strategies
============================

Due to the large number of strategies, every class and instance of the class has
a :code:`classifier` attribute which classifies that strategy according to
various dimensions.

Here is the :code:`classifier` for the :code:`Cooperator` strategy::

    >>> import axelrod as axl
    >>> expected_dictionary = {
    ...    'manipulates_state': False,
    ...    'makes_use_of': set([]),
    ...    'long_run_time': False,
    ...    'stochastic': False,
    ...    'manipulates_source': False,
    ...    'inspects_source': False,
    ...    'memory_depth': 0
    ... }  # Order of this dictionary might be different on your machine
    >>> axl.Cooperator.classifier == expected_dictionary
    True

Note that instances of the class also have this classifier::

    >>> s = axl.Cooperator()
    >>> s.classifier == expected_dictionary
    True

and that we can retrieve individual entries from that :code:`classifier` dictionary::

    >>> s = axl.TitForTat
    >>> s.classifier['memory_depth']
    1
    >>> s = axl.Random
    >>> s.classifier['stochastic']
    True

We can use this classification to generate sets of strategies according to
filters which we define in a 'filterset' dictionary and then pass to the
'filtered_strategies' function. For example, to identify all the stochastic
strategies::

    >>> filterset = {
    ...     'stochastic': True
    ... }
    >>> strategies = axl.filtered_strategies(filterset)
    >>> len(strategies)
    37


Or, to find out how many strategies only use 1 turn worth of memory to
make a decision::

    >>> filterset = {
    ...     'memory_depth': 1
    ... }
    >>> strategies = axl.filtered_strategies(filterset)
    >>> len(strategies)
    24

Multiple filters can be specified within the filterset dictionary. To specify a
range of memory_depth values, we can use the 'min_memory_depth' and
'max_memory_depth' filters::

    >>> filterset = {
    ...     'min_memory_depth': 1,
    ...     'max_memory_depth': 4
    ... }
    >>> strategies = axl.filtered_strategies(filterset)
    >>> len(strategies)
    41

We can also identify strategies that make use of particular properties of the
tournament. For example, here is the number of strategies that  make use of the
length of each match of the tournament::

    >>> filterset = {
    ...     'makes_use_of': ['length']
    ... }
    >>> strategies = axl.filtered_strategies(filterset)
    >>> len(strategies)
    5

Note that in the filterset dictionary, the value for the 'makes_use_of' key
must be a list. Here is how we might identify the number of strategies that use
both the length of the tournament and the game being played::

    >>> filterset = {
    ...     'makes_use_of': ['length', 'game']
    ... }
    >>> strategies = axl.filtered_strategies(filterset)
    >>> len(strategies)
    0

Some strategies have been classified as having a particularly long run time::

    >>> filterset = {
    ...     'long_run_time': True
    ... }
    >>> strategies = axl.filtered_strategies(filterset)
    >>> len(strategies)
    10

Strategies that :code:`manipulate_source`, :code:`manipulate_state`
and/or :code:`inspect_source` return :code:`False` for the :code:`obey_axelrod`
function::

    >>> s = axl.MindBender()
    >>> axl.obey_axelrod(s)
    False
    >>> s = axl.TitForTat()
    >>> axl.obey_axelrod(s)
    True
