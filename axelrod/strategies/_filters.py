from collections import namedtuple
import operator


def passes_operator_filter(strategy, classifier_key, value, operator):
    """
    Tests whether a given strategy passes a filter for a
    given key in its classifier dict using a given inequality operator.

    Parameters
    ----------
        strategy : a descendant class of axelrod.Player
        classifier_key: string
            Defining which entry from the strategy's classifier dict is to be
            tested (e.g. 'memory_depth').
        value: int
            The value against which the strategy's classifier dict entry is to
            be tested.
        operator: operator.le or operator.ge
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
    Tests whether a given value exists in the list returned from the given
    strategy's classifier dict for the given classifier_key.

    Parameters
    ----------
        strategy : a descendant class of axelrod.Player
        classifier_key: string
            Defining which entry from the strategy's classifier dict is to be
            tested (e.g. 'makes_use_of').
        value: string
            The value against which the strategy's classifier dict entry is to
            be tested.

    Returns
    -------
        boolean
    """
    return value in strategy.classifier[classifier_key]


def passes_filterset(strategy, filterset):
    """
    Determines whether a given strategy meets the criteria defined in a
    dictionary of filters.

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
    for filter, filter_function in filter_functions.items():

        if filterset.get(filter, None) is not None:
            kwargs = filter_function.kwargs
            kwargs['strategy'] = strategy
            kwargs['value'] = filterset[filter]
            passes_filters.append(filter_function.function(**kwargs))

    # Return True if the strategy passed all the supplied filters
    return all(passes_filters)
