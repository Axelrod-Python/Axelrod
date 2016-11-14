.. _fingerprinting:

Fingerprinting
==============

In [Ashlock2010] a methodology for obtaining visual representation of a
a strategy's behaviour is given...

[A couple more details]

Here is how to create a fingerprint of :code:`WinStayLoseShift` using
:code:`TitForTat` as a probe::

    >>> import axelrod as axl
    >>> axl.seed(0)  # Fingerprinting is a random process
    >>> strategy = axl.WinStayLoseShift
    >>> probe = axl.TitForTat
    >>> af = axl.AshlockFingerprint(strategy, probe)
    >>> af.fingerprint(turns=10, repetitions=2, step=0.2)
    {Point(x=0.8..., y=0.2...): 2.75, ...

The :code:`fingerprint` method returns a dictionary mapping ...

We can also create a plot::

    >>> 2 + 2
    4

[INCLUDE THE PLOT obtained with the above code]


Ashlock's fingerprint is currently the only fingerprint implemented in the
library.
