# v1.15.0, 2016-11-03

Mutation in Moran process, players track state pairs, save all plots method,
new strategies and PEP8.

- Mutation in Moran processes:
  https://github.com/Axelrod-Python/Axelrod/pull/754
- Save all plots to file method:
  https://github.com/Axelrod-Python/Axelrod/pull/753
- Players track state pairs:
  https://github.com/Axelrod-Python/Axelrod/pull/752
- New strategies:
      - StochasticCooperator (re introduced):
        https://github.com/Axelrod-Python/Axelrod/pull/755
      - SpitefulTitForTat
        https://github.com/Axelrod-Python/Axelrod/pull/749
- PEP8:
  https://github.com/Axelrod-Python/Axelrod/pull/750

Here are all the commits for this PR:
https://github.com/Axelrod-Python/Axelrod/compare/v1.14.0...v1.15.0

# v1.14.0, 2016-10-24

Two new strategies.

- Adding Negative strategy
  https://github.com/Axelrod-Python/Axelrod/pull/748
- Adding Doubler strategy
  https://github.com/Axelrod-Python/Axelrod/pull/747

Here are all the commits for this PR:
https://github.com/Axelrod-Python/Axelrod/compare/v1.13.0...v1.14.0

# v1.13.0, 2016-10-16

New strategy, state distribution and documentation

- Adding Prober4 strategy
  https://github.com/Axelrod-Python/Axelrod/pull/743
- Adding state distribution to results set
  https://github.com/Axelrod-Python/Axelrod/pull/742
- More references for strategies
  https://github.com/Axelrod-Python/Axelrod/pull/745

Here are all the commits for this PR:
https://github.com/Axelrod-Python/Axelrod/compare/v1.12.0...v1.13.0

# v1.12.0, 2016-10-13

Human interactive player, new strategy, under the hood improvements and
documentation.

- You can play against an instance of `axelrod.Human`
  https://github.com/Axelrod-Python/Axelrod/pull/732
- Improved efficiency of result set from memory
  https://github.com/Axelrod-Python/Axelrod/pull/737
- Documentation improvements
  https://github.com/Axelrod-Python/Axelrod/pull/741
  https://github.com/Axelrod-Python/Axelrod/pull/736
  https://github.com/Axelrod-Python/Axelrod/pull/735
  https://github.com/Axelrod-Python/Axelrod/pull/727
- New strategy CyclerCCCDCD:
  https://github.com/Axelrod-Python/Axelrod/pull/379

Here are all the commits for this PR:
https://github.com/Axelrod-Python/Axelrod/compare/v1.11.0...v1.12.0

# v1.12.0, 2016-10-13

Human interactive player, new strategy, under the hood improvements and
documentation.

- You can play against an instance of `axelrod.Human`
  https://github.com/Axelrod-Python/Axelrod/pull/732
- Improved efficiency of result set from memory
  https://github.com/Axelrod-Python/Axelrod/pull/737
- Documentation improvements
  https://github.com/Axelrod-Python/Axelrod/pull/741
  https://github.com/Axelrod-Python/Axelrod/pull/736
  https://github.com/Axelrod-Python/Axelrod/pull/735
  https://github.com/Axelrod-Python/Axelrod/pull/727
- New strategy CyclerCCCDCD:
  https://github.com/Axelrod-Python/Axelrod/pull/379

Here are all the commits for this PR:
https://github.com/Axelrod-Python/Axelrod/compare/v1.11.0...v1.12.0

# v1.11.0, 2016-09-28

State distribution functions, new strategies and minor test fix.

- Matches have a method to give state distribution:
  https://github.com/Axelrod-Python/Axelrod/pull/717
- Two new strategies: Worse and Worse and Knowledgeable Worse and Worse.
  https://github.com/Axelrod-Python/Axelrod/pull/724
- Minor fix of a test that would sometimes fail due to floating point error.
  https://github.com/Axelrod-Python/Axelrod/pull/725


Here are all the commits for this PR:
https://github.com/Axelrod-Python/Axelrod/compare/v1.10.0...v1.11.0

# v1.10.0, 2016-09-22

Windows support! Summarise method for results, new strategies, and code of
conduct as well as minor fixes.

- Various fixes to windows bugs (thanks to the PyConUK sprint!):
  https://github.com/Axelrod-Python/Axelrod/pull/711
  https://github.com/Axelrod-Python/Axelrod/pull/714
  https://github.com/Axelrod-Python/Axelrod/pull/721
- The result set has a summary:
  https://github.com/Axelrod-Python/Axelrod/pull/707
- Three new strategies (Gradual killer, easy go, Grudger alternator):
  https://github.com/Axelrod-Python/Axelrod/pull/715
- Code of conduct:
  https://github.com/Axelrod-Python/Axelrod/pull/705
- Fix of some tests:
  https://github.com/Axelrod-Python/Axelrod/pull/716
- Fix of link in docs:
  https://github.com/Axelrod-Python/Axelrod/pull/722


Here are all the commits for this PR:
https://github.com/Axelrod-Python/Axelrod/compare/v1.9.0...v1.10.0

# v1.9.0, 2016-09-09

Filtering of strategy classes with a filterset dictionary.

Here are all the commits for this PR:
https://github.com/Axelrod-Python/Axelrod/compare/v1.8.0...v1.9.0

# v1.8.0, 2016-08-28

New strategies:

- Adaptive TitForTat:
  https://github.com/Axelrod-Python/Axelrod/pull/697
- Desperate, Hopeless, Willing:
  https://github.com/Axelrod-Python/Axelrod/pull/686

Here are all the commits for this PR:
https://github.com/Axelrod-Python/Axelrod/compare/v1.7.0...v1.8.0

# v1.7.0, 2016-08-14

Probabilistic ending spatial tournaments, classifier for long run time, style
improvements, documentation improvements (including a bibliography) and bug fix.

- Probabilistic ending spatial tournaments:
  https://github.com/Axelrod-Python/Axelrod/pull/674
- Classifier for strategies that have a long run time:
  https://github.com/Axelrod-Python/Axelrod/issues/690
- Documentation and style
  cleanup:https://github.com/Axelrod-Python/Axelrod/issues/675,
  https://github.com/Axelrod-Python/Axelrod/pull/687,
  https://github.com/Axelrod-Python/Axelrod/pull/685,
  https://github.com/Axelrod-Python/Axelrod/pull/682
- Fix the noise in spatial tournaments:
  https://github.com/Axelrod-Python/Axelrod/pull/679

Here are all the commits for this PR:
https://github.com/Axelrod-Python/Axelrod/compare/v1.6.0...v1.7.0

# v1.6.0, 2016-07-31

Renaming of strategies, big performance improvement for result analysis and bug
fixes

- axelrod.strategies is a list of well behaved (non cheating strategies):
  https://github.com/Axelrod-Python/Axelrod/pull/665
- The results set now has much lower memory footprint and is much faster:
  https://github.com/Axelrod-Python/Axelrod/pull/672
- Correct calculation for mean score diffs:
  https://github.com/Axelrod-Python/Axelrod/pull/671
- Error catching for bug with OSX, virtual envs and matplotlib:
  https://github.com/Axelrod-Python/Axelrod/pull/669

Here are all the commits for this PR:
https://github.com/Axelrod-Python/Axelrod/compare/v1.5.0...v1.6.0

# v1.5.0, 2016-07-19

New tournament type, new strategy, seeding, dev tools, docs + minor/bug fixes

User facing:

- Spatial tournaments: https://github.com/Axelrod-Python/Axelrod/pull/654
- New strategy, slow tit for tat:
  https://github.com/Axelrod-Python/Axelrod/pull/659
- Seed the library: https://github.com/Axelrod-Python/Axelrod/pull/653
- More uniform strategy transformer behaviour:
  https://github.com/Axelrod-Python/Axelrod/pull/657
- Results can be calculated with non default game:
  https://github.com/Axelrod-Python/Axelrod/pull/656

Documentation:

- A community page: https://github.com/Axelrod-Python/Axelrod/pull/656
- An overall results page that replaces the payoff matrix page:
  https://github.com/Axelrod-Python/Axelrod/pull/660

Development:

- A git hook script for commit messages:
  https://github.com/Axelrod-Python/Axelrod/pull/648
- Caching of hypothesis database on travis:
  https://github.com/Axelrod-Python/Axelrod/pull/658

Here are all the commits for this PR:
https://github.com/Axelrod-Python/Axelrod/compare/v1.4.0...v1.5.0

# v1.4.0, 2016-06-22

New strategy.

- contrite TitForTat: https://github.com/Axelrod-Python/Axelrod/pull/639

Here are all the commits for this PR:
https://github.com/Axelrod-Python/Axelrod/compare/v1.3.0...v1.4.0

# v1.3.0, 2016-06-21

New strategy, a bug fix and more explicit copyright notice

- Remorseful Prober: https://github.com/Axelrod-Python/Axelrod/pull/633

Bug fix:

- The finite state machines were not reseting state properly.


Here are all the commits for this PR:
https://github.com/Axelrod-Python/Axelrod/compare/v1.2.0...v1.3.0

# v1.2.0, 2016-06-13

New strategies and some minor improvements

- Naive Prober: https://github.com/Axelrod-Python/Axelrod/pull/629
- Gradual: https://github.com/Axelrod-Python/Axelrod/pull/627
- Soft grudger and reverse pavlov:
  https://github.com/Axelrod-Python/Axelrod/pull/628

Minor improvements include:

- Progress bar for result set reading of data:
  https://github.com/Axelrod-Python/Axelrod/pull/618
- Prob end tournament players do not know match length (this was in essence a
  bug): https://github.com/Axelrod-Python/Axelrod/pull/611
- Doc fixes

Here are all the commits for this PR:
https://github.com/Axelrod-Python/Axelrod/compare/v1.1.1...v1.2.0

# v1.1.1, 2016-06-01

Minor changes, bug fixes.

Here are all the commits for this PR:
https://github.com/Axelrod-Python/Axelrod/compare/v1.1.0...v1.1.1

User facing:

- The matches can tell the players different match attributes than the ones
  actually being played (helpful for prob end tournaments where players cannot
  know the length of the match for example):
  https://github.com/Axelrod-Python/Axelrod/pull/609
- A progress bar for the result set:
  https://github.com/Axelrod-Python/Axelrod/pull/603

Internal:

- Reducing some test sizes: https://github.com/Axelrod-Python/Axelrod/pull/601
- PEP8 improvements: https://github.com/Axelrod-Python/Axelrod/pull/607
- Refactor of the match generator (noise is an attribute):
  https://github.com/Axelrod-Python/Axelrod/pull/608

# v1.1.0, 2016-05-18

New strategies and minor changes to the test suite

Here are all the commits for this PR:
https://github.com/Axelrod-Python/Axelrod/compare/v1.0.1...v1.1.0

This introduces various new strategies to the library:

- Adaptive
- Handshake
- CyclerDC and CyclerDDC (used in the literature)
- 8 Finite State Machine strategies: Fortress3, Fortress4, Predator,
  Raider, Ripoff, SolutionB1, SolutionB5, Thumper

This version also includes a minor change to the test suite: shortening the size
of the tournaments being run in the integration tests.

Here is the PR that incorporated all of the above:
https://github.com/Axelrod-Python/Axelrod/pull/591

# v1.0.1, 2016-05-15

Bug fix.

Here are all the commits for this PR:
https://github.com/Axelrod-Python/Axelrod/compare/v1.0.0...v1.0.1

During the previous refactor of the Tournament, the ability to create noisy
tournaments was lost. An integration test has been written to catch this in the
future: https://github.com/Axelrod-Python/Axelrod/pull/596

# v1.0.0, 2016-05-14

Internal improvements, progress bar, minor interface change

Here are all the commits for this PR:
https://github.com/Axelrod-Python/Axelrod/compare/v0.0.31...v1.0.0

This release is the first major release stating the stability and maturity of
the library.

There are some user facing improvements:

- A progress bar: https://github.com/Axelrod-Python/Axelrod/pull/578
- Whether or not a tournament is to be run using parallel processing is no
  longer a property of the tournament itself but an argument of the play method:
  https://github.com/Axelrod-Python/Axelrod/pull/582

There were some extensive internal changes:

- The tournament attributes are passed to the players from the matches and not
  the tournament. This should make further things like changing what the players
  know about the tournament more straightforward:
  https://github.com/Axelrod-Python/Axelrod/pull/537
- A huge re write of the actual way the tournament runs. This is the biggest
  such re write to date. The parallel workers now execute repetitions of matches
  which are written to disk as and when they complete. This greatly reduces the
  memory footprint of the tournament. A side effect of the above is a change of
  how the tournament is written to disk: the format is now much clearer (every
  row is a match): https://github.com/Axelrod-Python/Axelrod/pull/572

# v0.0.31, 2016-04-18

Moran processes, better caching architecture and match generator

# v0.0.30, 2016-04-08

Reading and writing tournaments to file, better pickling.

# v0.0.29, 2016-04-04

Bug fix with parallel processing.

# v0.0.28, 2016-03-29

New strategy, enhanced matches and prob end tournaments.

# v0.0.27, 2016-03-06

Minor fixes, rewrite of tournament engine: interactions now available.

# v0.0.26, 2016-02-24

Bug fix and two new strategies based on ThueMorse sequence.

# v0.0.25, 2016-01-26

Minor documentation changes.

# v0.0.24, 2016-01-19

New strategy (FirmButFair) and hypothesis testing

# v0.0.23, 2015-12-14

Mixed strategies (decorator and meta player)

# v0.0.22, 2015-12-07

Including a DOI.

# v0.0.21, 2015-11-29

Match class with sparklines.

# v0.0.20, 2015-11-21

Strategies have 'makes_use_of' attribute, improved docs/doctests,

# v0.0.19, 2015-11-21

Efficiency improvements, new default colour maps

# v0.0.18, 2015-11-04

New strategies

# v0.0.17, 2015-10-30

Strategy transforms and bug fixes

# v0.0.16, 2015-10-25

Tidying strategies, action classes, flip action method and new docs

# v0.0.15, 2015-10-13

Distribution of wins plots, and is_cheater becomes obey_axelrod

# v0.0.14, 2015-09-28

Change to use distutils, mirror strategy and readthedocs bug

# v0.0.13, 2015-09-16

Adding classifier dictionary and dynamic strategy list.

# v0.0.12, 2015-09-02

Further behaviour and more info being passed to players.

# v0.0.11, 2015-08-17

Updating Core team

# v0.0.10, 2015-08-17

Python 3 support and behaviour metrics

# v0.0.9, 2015-06-14

Various improvements including noisy tournaments

# v0.0.8, 2015-04-16

Change default behaviour to maximisation

# v0.0.7, 2015-04-01

Perhaps removes long description

# v0.0.6, 2015-04-01

Removes long description

# v0.0.5, 2015-03-28

Corrects formatting of authors

# v0.0.4, 2015-03-28

Adding all authors

# v0.0.3, 2015-03-27

Minor fix

# v0.0.2, 2015-03-27

Minor fix

# v0.0.1, 2015-03-27

Initial release
