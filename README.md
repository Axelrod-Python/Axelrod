# Axelrod

A repository to reproduce Axelrod's iterated prisoner's dilemma.
**Please contribute strategies via pull request (or just get in touch with me).**

# History of Axelrod's tournament

In the 1980s, professor of Political Science Robert Axelrod ran a tournament inviting strategies from collaborators all over the world for the **Iterated Prisoner's Dilemma**.
You can read about this more [here](http://en.wikipedia.org/wiki/The_Evolution_of_Cooperation#Axelrod.27s_tournaments).

Another nice write up of Axelrod's work and this tournament on github was put together by [Artem Kaznatcheev](https://plus.google.com/101780559173703781847/posts) [here](https://egtheory.wordpress.com/2015/03/02/ipd/).

## The Prisoner's Dilemma

The [Prisoner's dilemma](http://en.wikipedia.org/wiki/Prisoner%27s_dilemma) is the simple two player game shown below:

          | Cooperate     | Defect        |
--------- | ------------- | ------------- |
Cooperate | (2,2)         | (0,5)         |
Defect    | (5,0)         | (4,4)         |

If both players cooperate they will each go to prison for 2 years.
If one cooperates and the other defects: the defector does not go to prison and the cooperator goes to prison for 5 years.
If both defect: they both go to prison for 4 years.

By simply investigating the best responses against both possible actions of each player it is immediate to see that the Nash equilibrium for this game is for both players to defect.

## The iterated Prisoner's Dilemma

We can use the basic Prisoner's Dilemma as a _stage_ game in a repeated game.
Players now aim to minimise the amount of time spent in prison over a repetition of the game.
Strategies can take in to account both players history and so can take the form:

> I will cooperate unless you defect 3 times in a row at which point I will defect forever.

Axelrod ran such a tournament (twice) and invited strategies from anyone who would contribute.
The tournament was a round robin and the winner was the strategy who had the lowest total amount of time in prison.

This tournament has been used to study how cooperation can evolve from a very simple set of rules.
This is mainly because the winner of both tournaments was 'tit for tat': a strategy that would never defect first (referred to as a 'nice' strategy).

# Results

This repository contains Python (2.7) code that reproduces the tournament.
To run the tournament, you simply need to:

```
$ python run_tournament.py
```

This automatically outputs a `png` file with the results.
You can see the results from the latest run of the tournament here:

![](./assets/strategies_boxplot.png)

As you can see: the 'tit for tat' strategy has not won in this instance, that is mainly because more strategies are needed to get anywhere near Axelrod's tournament.

You can see the results from the latest run of the tournament here with the cheating strategies (which manipulate/read what the opponent does):

![](./assets/all_strategies_boxplot.png)

Please do contribute :)

Note that you can run `python run_tournament.py -h` for further options available: for example, cheating strategies can be excluded for faster results by running:

```
$ python run_tournament.py --xc --xa
```

## Awesome visualisation

[martinjc](https://github.com/martinjc) put together a pretty awesome visualisation of this using d3. Hosted on gh-pages it can be seen here: [drvinceknight.github.io/Axelrod](http://drvinceknight.github.io/Axelrod/).

## Documentation

There is currently a very sparse set of documentation up here: [axelrod.readthedocs.org/](http://axelrod.readthedocs.org/).

To write/render the documenation locally, you will need [sphinx](http://sphinx-doc.org/):

```
$ pip install sphinx sphinx-autobuild
```

Once you have sphinx:

```
$ cd docs
$ make html
```

# Contributing

All contributions are welcome: with a particular emphasis on contributing further strategies.

You can find helpful instructions about contributing in the documentation: [http://axelrod.readthedocs.org/en/latest/contributing.html](http://axelrod.readthedocs.org/en/latest/contributing.html).

# Contributors

- [JasYoung314](https://github.com/JasYoung314)
- [Karlos78](https://github.com/Karlos78)
- [drvinceknight](https://twitter.com/drvinceknight)
- [geraintpalmer](https://github.com/geraintpalmer)
- [hollymarissa](https://github.com/hollymarissa)
- [jomuel](https://github.com/jomuel)
- [langner](https://github.com/langner)
- [marcharper](https://github.com/marcharper)
- [martinjc](https://github.com/martinjc)
- [meatballs](https://github.com/meatballs)
- [theref](https://github.com/theref)
- [timothyf1](https://github.com/timothyf1)
- [uglyfruitcake](https://github.com/uglyfruitcake)
- [pmslavin](https://github.com/pmslavin)
