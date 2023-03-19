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

The instance starts with a copy of the class's classifier dictionary, but is
allowed to change this classifier dictionary at any point, and many
strategies do so upon initialization.

In addition to the classifier dictionary, each classifier is defined with
some logic that maps classifier definitions to values.  To learn the
classification of a strategy, we first look in the strategy's classifier
dictionary, then if the key is not present, then we refer to this logic.
This logic must be defined for a class, and not specific instances.

To lookup the classifier of a strategy, using the classifier dict, or the
strategy's logic as default, we use :code:`Classifiers[<classifier>](
<strategy>)`::

    >>> from axelrod import Classifiers
    >>> Classifiers['memory_depth'](axl.TitForTat())
    1
    >>> Classifiers['stochastic'](axl.Random())
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
    88

Or, to find out how many strategies only use 1 turn worth of memory to
make a decision::

    >>> filterset = {
    ...     'memory_depth': 1
    ... }
    >>> strategies = axl.filtered_strategies(filterset)
    >>> len(strategies)
    33

Multiple filters can be specified within the filterset dictionary. To specify a
range of memory_depth values, we can use the 'min_memory_depth' and
'max_memory_depth' filters::

    >>> filterset = {
    ...     'min_memory_depth': 1,
    ...     'max_memory_depth': 4
    ... }
    >>> strategies = axl.filtered_strategies(filterset)
    >>> len(strategies)
    57

We can also identify strategies that make use of particular properties of the
tournament. For example, here is the number of strategies that  make use of the
length of each match of the tournament::

    >>> filterset = {
    ...     'makes_use_of': ['length']
    ... }
    >>> strategies = axl.filtered_strategies(filterset)
    >>> len(strategies)
    22

Note that in the filterset dictionary, the value for the 'makes_use_of' key
must be a list. Here is how we might identify the number of strategies that use
both the length of the tournament and the game being played::

    >>> filterset = {
    ...     'makes_use_of': ['length', 'game']
    ... }
    >>> strategies = axl.filtered_strategies(filterset)
    >>> len(strategies)
    15

Some strategies have been classified as having a particularly long run time::

    >>> filterset = {
    ...     'long_run_time': True
    ... }
    >>> strategies = axl.filtered_strategies(filterset)
    >>> len(strategies)
    18

Strategies that :code:`manipulate_source`, :code:`manipulate_state`
and/or :code:`inspect_source` return :code:`False` for the
:code:`Classifier.obey_axelrod` function::

    >>> s = axl.Darwin()
    >>> axl.Classifiers.obey_axelrod(s)
    False
    >>> s = axl.TitForTat()
    >>> axl.Classifiers.obey_axelrod(s)
    True
