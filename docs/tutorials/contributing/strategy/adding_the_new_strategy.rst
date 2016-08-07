Adding the new strategy
=======================

To get the strategy to be recognised by the library we need to add it to the
files that initialise when someone types :code:`import axelrod`.  This is done
in the :code:`axelrod/strategies/_strategies.py` file.

If you have added your strategy to a file that already existed (perhaps you
added a new variant of :code:`titfortat` to the :code:`titfortat.py` file),
simply add your strategy to the list of strategies already imported from
:code:`<file_name>.py`::

    from <file_name> import <list-of-strategies>

If you have added your strategy to a new file then simply add a line similar to
above with your new strategy.

Once you have done that, you need to add the class itself to the
:code:`all_strategies` list (in `axelrod/strategies/_strategies.py`).

Finally, if you have created a new module (a new :code:`<strategy.py>` file)
please add it to the `docs/references/all_strategies.rst` file so that it will
automatically be documented.
