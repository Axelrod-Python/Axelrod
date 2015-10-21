Noisy tournaments
=================

A common variation on iterated prisoner’s dilemma tournaments is to add
stochasticity in the choice of plays, simply called noise. This noise is
introduced by flipping plays between ‘C’ and ‘D’ with some probability that is
applied to all plays after they are delivered by the player.

The presence of this persistant bakground noise causes some strategies to
behave substantially differently. For example, TitForTat can fall into
defection loops with itself when there is noise. While TitForTat would usually
cooperate well with itself::

    C C C C C ...
    C C C C C ...

Noise can cause a C to flip to a D (or vice versa), disrupting the cooperative
chain::

    C C C D C D C D D D ...
    C C C C D C D D D D ...

To create a noisy tournament you simply need to add the `noise` argument::

    >>> import axelrod as axl
    >>> strategies = [axl.Cooperator(), axl.Defector(),
    ...               axl.TitForTat(), axl.Grudger()]
    >>> noise = 0.1
    >>> tournament = axl.Tournament(strategies, noise=noise)
    >>> results = tournament.play()
    >>> plot = axl.Plot(results)
    >>> p = plot.boxplot()
    >>> p.show()

.. image:: _static/visualising_results/demo_strategies_noisy_boxplot.svg
   :width: 50%
   :align: center

Here is how the distribution of wins now looks::

    >>> p = plot.winplot()
    >>> p.show()

.. image:: _static/visualising_results/demo_strategies_noisy_winplot.svg
   :width: 50%
   :align: center
