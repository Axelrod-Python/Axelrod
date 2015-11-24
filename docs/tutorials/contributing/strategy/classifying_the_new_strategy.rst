Classifying the new strategy
============================

Every class has a classifier dictionary that gives some classification of the
strategy according to certain dimensions::

Let us take a look at :code:`TitForTat`::

    >>> import axelrod
    >>> classifier = axelrod.TitForTat.classifier
    >>> for key in sorted(classifier.keys()):
    ...    print("{}: {}".format(key, classifier[key]))
    inspects_source: False
    makes_use_of: set([])
    manipulates_source: False
    manipulates_state: False
    memory_depth: 1
    stochastic: False

You can read more about this in the :ref:`classification-of-strategies` section
but here are some tips about fill this part in correctly.

Note that when an instance of a class is created it gets it's own copy of the
default classifier dictionary from the class. This might sometimes be modified by
the initialisation depending on input parameters. A good example of this is the
:code:`Joss` strategy::

    >>> joss = axelrod.Joss()
    >>> boring_joss = axelrod.Joss(1)
    >>> joss.classifier['stochastic'], boring_joss.classifier['stochastic']
    (True, False)

Dimensions that are not classified have value `None` in the dictionary.

There are currently three important dimensions that help identify if a strategy
obeys axelrod's original tournament rules.

1. :code:`inspects_source` - does the strategy 'read' any source code that
   it would not normally have access to. An example of this is :code:`Geller`.
2. :code:`manipulates_source` - does the strategy 'write' any source code that
   it would not normally be able to. An example of this is :code:`Mind Bender`.
3. :code:`manipulates_state` - does the strategy 'change' any attributes that
   it would not normally be able to. An example of this is :code:`Mind Reader`.

These dimensions are currently relevant to the `obey_axelrod` strategy which
checks if a strategy obeys Axelrod's original rules.
