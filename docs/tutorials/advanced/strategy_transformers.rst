.. _strategy_transformers:

Strategy Transformers
=====================

What is a Strategy Transformer?
-------------------------------

A strategy transformer is a function that modifies an existing strategy. For
example, :code:`FlipTransformer` takes a strategy and flips the actions from
C to D and D to C::

    >>> import axelrod as axl
    >>> from axelrod.strategy_transformers import *
    >>> FlippedCooperator = FlipTransformer()(axl.Cooperator)
    >>> player = FlippedCooperator()
    >>> opponent = axl.Cooperator()
    >>> player.strategy(opponent)
    D
    >>> opponent.strategy(player)
    C

Our player was switched from a :code:`Cooperator` to a :code:`Defector` when
we applied the transformer. The transformer also changed the name of the
class and player::

    >>> player.name
    'Flipped Cooperator'
    >>> FlippedCooperator.name
    'Flipped Cooperator'

This behavior can be suppressed by setting the :code:`name_prefix` argument::

    >>> FlippedCooperator = FlipTransformer(name_prefix=None)(axl.Cooperator)
    >>> player = FlippedCooperator()
    >>> player.name
    'Cooperator'

Note carefully that the transformer returns a class, not an instance of a class.
This means that you need to use the Transformed class as you would normally to
create a new instance::

    >>> from axelrod.strategy_transformers import NoisyTransformer
    >>> player = NoisyTransformer(0.5)(axl.Cooperator)()

rather than :code:`NoisyTransformer(0.5)(axl.Cooperator())` or just :code:`NoisyTransformer(0.5)(axl.Cooperator)`.

Included Transformers
---------------------

The library includes the following transformers:

* :code:`ApologyTransformer`: Apologizes after a round of :code:`(D, C)`::

    >>> ApologizingDefector = ApologyTransformer([D], [C])(axl.Defector)
    >>> player = ApologizingDefector()

   You can pass any two sequences in. In this example the player would apologize
   after two consequtive rounds of `(D, C)`::

       >>> ApologizingDefector = ApologyTransformer([D, D], [C, C])(axl.Defector)
       >>> player = ApologizingDefector()

* :code:`DeadlockBreakingTransformer`: Attempts to break :code:`(D, C) -> (C, D)` deadlocks by cooperating::

    >>> DeadlockBreakingTFT = DeadlockBreakingTransformer()(axl.TitForTat)
    >>> player = DeadlockBreakingTFT()

* :code:`DualTransformer`: The Dual of a strategy will return the exact opposite set of moves to the original strategy when both are faced with the same history. [Ashlock2008]_::

    >>> DualWSLS = DualTransformer()(axl.WinStayLoseShift)
    >>> player = DualWSLS()

* :code:`FlipTransformer`: Flips all actions::

    >>> FlippedCooperator = FlipTransformer()(axl.Cooperator)
    >>> player = FlippedCooperator()

* :code:`FinalTransformer(seq=None)`: Ends the tournament with the moves in the sequence :code:`seq`, if the tournament_length is known. For example, to obtain a cooperator that defects on the last two rounds::

    >>> FinallyDefectingCooperator = FinalTransformer([D, D])(axl.Cooperator)
    >>> player = FinallyDefectingCooperator()

* :code:`ForgiverTransformer(p)`: Flips defections with probability :code:`p`::

    >>> ForgivinDefector = ForgiverTransformer(0.1)(axl.Defector)
    >>> player = ForgivinDefector()

* :code:`GrudgeTransformer(N)`: Defections unconditionally after more than N defections::

    >>> GrudgingCooperator = GrudgeTransformer(2)(axl.Cooperator)
    >>> player = GrudgingCooperator()

* :code:`InitialTransformer(seq=None)`: First plays the moves in the sequence :code:`seq`, then plays as usual. For example, to obtain a defector that cooperates on the first two rounds::

    >>> InitiallyCooperatingDefector = InitialTransformer([C, C])(axl.Defector)
    >>> player = InitiallyCooperatingDefector()

* :code:`JossAnnTransformer(probability)`: Where :code:`probability = (x, y)`, the Joss-Ann of a strategy is a new strategy which has a probability :code:`x` of choosing the move C, a probability :code:`y` of choosing the move D, and otherwise uses the response appropriate to the original strategy. [Ashlock2008]_::

    >>> JossAnnTFT = JossAnnTransformer((0.2, 0.3))(axl.TitForTat)
    >>> player = JossAnnTFT()

* :code:`MixedTransformer`: Randomly plays a mutation to another strategy (or
  set of strategies. Here is the syntax to do this with a set of strategies::

    >>> strategies = [axl.Grudger, axl.TitForTat]
    >>> probability = [.2, .3]  # .5 chance of mutated to one of above
    >>> player =  MixedTransformer(probability, strategies)(axl.Cooperator)

  Here is the syntax when passing a single strategy::

    >>> strategy = axl.Grudger
    >>> probability = .2
    >>> player =  MixedTransformer(probability, strategy)(axl.Cooperator)

* :code:`NiceTransformer()`: Prevents a strategy from defecting if the opponent
  has not yet defected::

    >>> NiceDefector = NiceTransformer()(axl.Defector)
    >>> player = NiceDefector()


* :code:`NoisyTransformer(noise)`: Flips actions with probability :code:`noise`::

    >>> NoisyCooperator = NoisyTransformer(0.5)(axl.Cooperator)
    >>> player = NoisyCooperator()

* :code:`RetaliationTransformer(N)`: Retaliation N times after a defection::

    >>> TwoTitsForTat = RetaliationTransformer(2)(axl.Cooperator)
    >>> player = TwoTitsForTat()

* :code:`RetaliateUntilApologyTransformer()`: adds TitForTat-style retaliation::

    >>> TFT = RetaliateUntilApologyTransformer()(axl.Cooperator)
    >>> player = TFT()

* :code:`TrackHistoryTransformer`: Tracks History internally in the
  :code:`Player` instance in a variable :code:`_recorded_history`. This allows a
  player to e.g. detect noise.::

    >>> player = TrackHistoryTransformer()(axl.Random)()


Composing Transformers
----------------------

Transformers can be composed to form new composers, in two ways. You can
simply chain together multiple transformers::

    >>> cls1 = FinalTransformer([D,D])(InitialTransformer([D,D])(axl.Cooperator))
    >>> p1 = cls1()

This defines a strategy that cooperates except on the first two and last two
rounds. Alternatively, you can make a new class using
:code:`compose_transformers`::

    >>> cls1 = compose_transformers(FinalTransformer([D, D]), InitialTransformer([D, D]))
    >>> p1 = cls1(axl.Cooperator)()
    >>> p2 = cls1(axl.Defector)()


Usage as Class Decorators
-------------------------

Transformers can also be used to decorate existing strategies. For example,
the strategy :code:`BackStabber` defects on the last two rounds. We can encode this
behavior with a transformer as a class decorator::

    @FinalTransformer([D, D]) # End with two defections
    class BackStabber(Player):
        """
        Forgives the first 3 defections but on the fourth
        will defect forever. Defects on the last 2 rounds unconditionally.
        """

        name = 'BackStabber'
        classifier = {
            'memory_depth': float('inf'),
            'stochastic': False,
            'inspects_source': False,
            'manipulates_source': False,
            'manipulates_state': False
        }

        def strategy(self, opponent):
            if not opponent.history:
                return C
            if opponent.defections > 3:
                return D
            return C


Writing New Transformers
------------------------

To make a new transformer, you need to define a strategy wrapping function with
the following signature::

    def strategy_wrapper(player, opponent, proposed_action, *args, **kwargs):
        """
        Strategy wrapper functions should be of the following form.

        Parameters
        ----------
        player: Player object or subclass (self)
        opponent: Player object or subclass
        proposed_action: an axelrod.Action, C or D
            The proposed action by the wrapped strategy
            proposed_action = Player.strategy(...)
        args, kwargs:
            Any additional arguments that you need.

        Returns
        -------
        action: an axelrod.Action, C or D

        """

        # This example just passes through the proposed_action
        return proposed_action


The proposed action will be the outcome of::

    self.strategy(player)

in the underlying class (the one that is transformed). The strategy_wrapper still
has full access to the player and the opponent objects and can have arguments.

To make a transformer from the :code:`strategy_wrapper` function, use
:code:`StrategyTransformerFactory`, which has signature::

    def StrategyTransformerFactory(strategy_wrapper, name_prefix=""):
        """Modify an existing strategy dynamically by wrapping the strategy
        method with the argument `strategy_wrapper`.

        Parameters
        ----------
        strategy_wrapper: function
            A function of the form `strategy_wrapper(player, opponent, proposed_action, *args, **kwargs)`
            Can also use a class that implements
                def __call__(self, player, opponent, action)
        name_prefix: string, "Transformed "
            A string to prepend to the strategy and class name
        """

So we use :code:`StrategyTransformerFactory` with :code:`strategy_wrapper`::

    TransformedClass = StrategyTransformerFactory(generic_strategy_wrapper)
    Cooperator2 = TransformedClass(*args, **kwargs)(axl.Cooperator)

If your wrapper requires no arguments, you can simply proceed as follows::

    >>> TransformedClass = StrategyTransformerFactory(generic_strategy_wrapper)()
    >>> Cooperator2 = TransformedClass(axl.Cooperator)

For more examples, see :code:`axelrod/strategy_transformers.py`.
