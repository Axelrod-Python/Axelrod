Writing the new strategy
========================

Identify a new strategy
-----------------------

If you're not sure if you have a strategy that has already been implemented
please get in touch: `via the gitter room
<https://gitter.im/Axelrod-Python/Axelrod>`_ or `open an issue
<https://github.com/Axelrod-Python/Axelrod/issues>`_.

Several strategies are special cases of other strategies. For example, both
`Cooperator` and `Defector` are special cases of `Random`, `Random(1)` and
`Random(0)` respectively. While we could eliminate `Cooperator` in its current
form, these strategies are intentionally left as is as simple examples for new
users and contributors. Nevertheless, please feel free to update the docstrings
of strategies like `Random` to point out such cases.

The code
--------

There are a couple of things that need to be created in a strategy.py file.  Let
us take a look at the :code:`TitForTat` class (located in the
:code:`axelrod/strategies/titfortat.py` file)::

    class TitForTat(Player):
        """
        A player starts by cooperating and then mimics previous move by
        opponent.

        Note that the code for this strategy is written in a fairly verbose
        way. This is done so that it can serve as an example strategy for
        those who might be new to Python.
        """

        # These are various properties for the strategy
        name = 'Tit For Tat'
        classifier = {
            'memory_depth': 1,  # Four-Vector = (1.,0.,1.,0.)
            'stochastic': False,
            'inspects_source': False,
            'manipulates_source': False,
            'manipulates_state': False
        }

        def strategy(self, opponent):
            """This is the actual strategy"""
            # First move
            if len(self.history) == 0:
                return C
            # React to the opponent's last move
            if opponent.history[-1] == D:
                return D
            return C

The first thing that is needed is a docstring that explains what the strategy
does::

    """A player starts by cooperating and then mimics previous move by opponent."""

After that simply add in the string that will appear as the name of the
strategy::

    name = 'Tit For Tat'

Note that this is mainly used in plots by :code:`matplotlib` so you can use
LaTeX if you want to.  For example there is strategy with :math:`\pi` as a
name::

    name = '$\pi$'

Following that you can add in the :code:`classifier` dictionary::

        classifier = {
            'memory_depth': 1,  # Four-Vector = (1.,0.,1.,0.)
            'stochastic': False,
            'inspects_source': False,
            'manipulates_source': False,
            'manipulates_state': False
        }

This helps classify the strategy as described in
:ref:`classification-of-strategies`.

After that the only thing required is to write the :code:`strategy` method
which takes an opponent as an argument. In the case of :code:`TitForTat` the
strategy checks if it has any history (:code:`if len(self.history) == 0`). If
it does not (ie this is the first play of the match) then it returns :code:`C`.
If not, the strategy simply repeats the opponent's last move (:code:`return
opponent.history[-1]`)::

    def strategy(opponent):
        """This is the actual strategy"""
        # First move
        if len(self.history) == 0:
            return C
        # Repeat the opponent's last move
        return opponent.history[-1]

The variables :code:`C` and :code:`D` represent the cooperate and defect actions respectively.

If your strategy creates any particular attribute along the way you need to make
sure that there is a :code:`reset` method that takes account of it.  An example
of this is the :code:`ForgetfulGrudger` strategy.

You can also modify the name of the strategy with the `__repr__` method, which
is invoked when `str` is applied to a player instance. For example, the `Random`
strategy takes a parameter `p` for how often it cooperates, and the `__repr__`
method adds the value of this parameter to the name::

    def __repr__(self):
        return "%s: %s" % (self.name, round(self.p, 2))

Now we have separate names for different instantiations::

    >>> import axelrod
    >>> player1 = axelrod.Random(p=0.5)
    >>> player2 = axelrod.Random(p=0.1)
    >>> player1
    Random: 0.5
    >>> player2
    Random: 0.1

This helps distinguish players in tournaments that have multiple instances of the
same strategy. If you modify the `__repr__` method of player, be sure to add an
appropriate test.

Similarly, if your strategy's `__init__` method takes any parameters other than
`self`, you can decorate it with `@init_args` to ensure that when it is cloned that
the correct parameter values will be applied. (This will trip a test if ommitted.)

There are various examples of helpful functions and properties that make
writing strategies easier. Do not hesitate to get in touch with the
Axelrod-Python team for guidance.
