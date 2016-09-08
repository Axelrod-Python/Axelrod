from collections import namedtuple
import operator


def passes_operator_filter(strategy, classifier_key, value, operator):
    """
    Tests whether a given strategy passes a filter for a
    given key in its classifier dict using a given (in)equality operator.

    e.g.

    For the following strategy:

    class ExampleStrategy(Player):
        classifier = {
            'stochastic': True,
            'inspects_source': False,
            'memory_depth': 10,
            'makes_use_of': ['game', 'length']
        }

    passes_operator_filter(ExampleStrategy, 'memory_depth', 10, operator.eq)

    would test whether the 'memory_depth' entry equals 10 and return True

    Parameters
    ----------
        strategy : a descendant class of axelrod.Player
        classifier_key: string
            Defining which entry from the strategy's classifier dict is to be
            tested (e.g. 'memory_depth').
        value: int
            The value against which the strategy's classifier dict entry is to
            be tested.
        operator: operator.le, operator.ge or operator.eq
            Indicating whether a 'less than or equal to' or 'greater than or
            equal to' test should be applied.

    Returns
    -------
        boolean

        True if the value from the strategy's classifier dictionary matches
        the value and operator passed to the function.
    """
    classifier_value = strategy.classifier[classifier_key]
    if (isinstance(classifier_value, str) and
            classifier_value.lower() == 'infinity'):
        classifier_value = float('inf')

    return operator(classifier_value, value)


def passes_in_list_filter(strategy, classifier_key, value):
    """
    Tests whether a given list of values exist in the list returned from the
    given strategy's classifier dict for the given classifier_key.

    e.g.

    For the following strategy:

    class ExampleStrategy(Player):
        classifier = {
            'stochastic': True,
            'inspects_source': False,
            'memory_depth': 10,
            'makes_use_of': ['game', 'length']
        }

    passes_in_list_filter(ExampleStrategy, 'makes_use_of', 'game', operator.eq)

    would test whether 'game' exists in the strategy's' 'makes_use_of' entry
    and return True.

    Parameters
    ----------
        strategy : a descendant class of axelrod.Player
        classifier_key: string
            Defining which entry from the strategy's classifier dict is to be
            tested (e.g. 'makes_use_of').
        value: list
            The values against which the strategy's classifier dict entry is to
            be tested.

    Returns
    -------
        boolean
    """
    result = True
    for entry in value:
        if entry not in strategy.classifier[classifier_key]:
            result = False
    return result


def passes_filterset(strategy, filterset):
    """
    Determines whether a given strategy meets the criteria defined in a
    dictionary of filters.

    e.g.

    For the following strategy:

    class ExampleStrategy(Player):
        classifier = {
            'stochastic': True,
            'inspects_source': False,
            'memory_depth': 10,
            'makes_use_of': ['game', 'length']
        }

    and this filterset dict:

    example_filterset = {
        'stochastic': True,
        'memory_depth': 10
    }

    passes_filterset(ExampleStrategy, example_filterset)

    would test whether both the strategy's 'stochastic' entry is True AND
    that its 'memory_depth' equals 10 and return True.

    Parameters
    ----------
        strategy : a descendant class of axelrod.Player
        filterset : dict
            mapping filter name to criterion.
            e.g.
                {
                    'stochastic': True,
                    'min_memory_depth': 2
                }

    Returns
    -------
        boolean

        True if the given strategy meets all the supplied criteria in the
        filterset, otherwise false.

    """
    FilterFunction = namedtuple('FilterFunction', 'function kwargs')

    # A dictionary mapping filter name (from the supplied filterset) to
    # the relevant function and arguments for that filter.
    filter_functions = {
        'stochastic': FilterFunction(
            function=passes_operator_filter,
            kwargs={
                'classifier_key': 'stochastic',
                'operator': operator.eq
            }),
        'long_run_time': FilterFunction(
            function=passes_operator_filter,
            kwargs={
                'classifier_key': 'long_run_time',
                'operator': operator.eq
            }),
        'manipulates_state': FilterFunction(
            function=passes_operator_filter,
            kwargs={
                'classifier_key': 'manipulates_state',
                'operator': operator.eq
            }),
        'manipulates_source': FilterFunction(
            function=passes_operator_filter,
            kwargs={
                'classifier_key': 'manipulates_source',
                'operator': operator.eq
            }),
        'inspects_source': FilterFunction(
            function=passes_operator_filter,
            kwargs={
                'classifier_key': 'inspects_source',
                'operator': operator.eq
            }),
        'memory_depth': FilterFunction(
            function=passes_operator_filter,
            kwargs={
                'classifier_key': 'memory_depth',
                'operator': operator.eq
            }),
        'min_memory_depth': FilterFunction(
            function=passes_operator_filter,
            kwargs={
                'classifier_key': 'memory_depth',
                'operator': operator.ge
            }),
        'max_memory_depth': FilterFunction(
            function=passes_operator_filter,
            kwargs={
                'classifier_key': 'memory_depth',
                'operator': operator.le
            }),
        'makes_use_of': FilterFunction(
            function=passes_in_list_filter,
            kwargs={'classifier_key': 'makes_use_of'})
    }

    # A list of boolean values to record whether the strategy passed or failed
    # each of the filters in the supplied filterset.
    passes_filters = []

    # Loop through each of the entries in the filter_functions dict and, if
    # that filter is defined in the supplied filterset, call the relevant
    # function and record its result in the passes_filters list.
    for _filter, filter_function in filter_functions.items():

        if filterset.get(_filter, None) is not None:
            kwargs = filter_function.kwargs
            kwargs['strategy'] = strategy
            kwargs['value'] = filterset[_filter]
            passes_filters.append(filter_function.function(**kwargs))

    # Return True if the strategy passed all the supplied filters
    return all(passes_filters)
