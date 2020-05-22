Other games
===========

The Axelrod library was originally built to support playing the iterated
prisoner's dilemma.  But there is work underway to expand this to other games,
for example, the Ultimatum game.

This document explains what work needs to be done to add a new game to the
Axelrod library.

Adding a game
-------------

You should first create a folder in axelrod/ with the name of the game.

Then you need to build the following objects within that folder:

- A player class which inherits from BasePlayer.  Every strategy that will
  compete in your game should inherit from this class, so you should include
  stubs of any function that you expect this function to have.  Player class
  should have class variables of name (a text field specific to a strategy), and
  classifiers dict, which should at least include a "stochastic" key with a
  boolean value indicating if the strategy includes any random components.
- Specific strategies, inheriting from your player class.
- A scorer class which inherits from BaseScorer and implements the score method,
  which returns the Scores resulting from a tuple of Actions.
- Position enumeration (if not symmetric 2-player).  This indicates all the
  possible positions for a game.  Every round of the game should be played with
  exactly one player filling each position.
- A GameParams instance, which includes:

    - game_type: A short string identifying your new game.
    - generate_play_params: An iterator which describes how to choose players
      for each position, from a pool of players, for each round of play.
    - play_round: A function which, given players/positions, plays a round of
      the game, returning Actions.
