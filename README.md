# Axelrod

[![Join the chat at https://gitter.im/drvinceknight/Axelrod](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/drvinceknight/Axelrod?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

A repository to reproduce Axelrod's iterated prisoner's dilemma.
**Please contribute strategies via pull request (or just get in touch with me).**

For an overview of how to use and contribute to this repository, see the documentation: http://axelrod.readthedocs.org/

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

You can also run the tournament in parallel (below will run 4 parallel processes):

```
$ python run_tournament.py -p 4
```

You can run with all available CPUs with:

```
$ python run_tournament.py -p 0
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
