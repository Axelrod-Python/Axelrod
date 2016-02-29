Adding the new strategy
=======================

To get the strategy to be recognised by the library we need to add it to the
files that initialise when someone types :code:`import axelrod`.  This is done
in the :code:`axelrod/strategies/_strategies.py` file.

If you have added your strategy to a file that already existed (perhaps you
added a new variant of :code:`titfortat` to the :code:`titfortat.py` file),
add a line similar to::

    from <file_name> import *

Where :code:`file_name.py` is the name of the file you created.  So for the
:code:`TitForTat` strategy which is written in the :code:`titfortat.py` file we
have::

    from titfortat import *

Once you have done that (**and you need to do this even if you have added a
strategy to an already existing file**), you need to add the class itself to
the :code:`strategies` list.

Finally, if you have created a new module (a new :code:`<strategy.py>` file)
please add it to the `docs/references/all_strategies.rst` file so that it will
automatically be documented.
