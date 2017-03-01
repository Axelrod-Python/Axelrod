Writing docstrings
==================

The project takes pride in its documentation for the strategies
and its corresponding bibliography. The docstring is a string 
which describes a method, module or class. The docstrings help 
the user in understanding the working of the strategy 
and the source of the strategy. The docstring must be written in
the following way, i.e.::

    """This is a docstring.

   It can be written over multiple lines.

   """
 
Sections
--------

The Sections of the docstring are:

1. **Working of the strategy**

   A brief summary on how the strategy works, E.g.::

        class TitForTat(Player):
        """
        A player starts by cooperating and then mimics the 
        previous action of the opponent.
        """

2. **Bibliography/Source of the strategy**

   A section to mention the source of the strategy
   or the paper from which the strategy was taken.
   The section must start with the Names section.
   For E.g.::
    
        class TitForTat(Player):
        """
        A player starts by cooperating and then mimics the 
        previous action of the opponent.
    
        Names:
        - Rapoport's strategy: [Axelrod1980]_
        - TitForTat: [Axelrod1980]_
        """
    
   Here, the info written under the Names section
   tells about the source of the TitforTat strategy.
   `[Axelrod1980]_` corresponds to the bibliographic item in 
   `docs/reference/bibliography.rst`. If you are using a source 
   that is not in the bibliography please add it. 
