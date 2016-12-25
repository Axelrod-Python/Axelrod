import pkg_resources

def load_data(filename, directory="data"):
    """Load comma separated values."""
    path = '/'.join((directory, filename))
    data = pkg_resources.resource_string(__name__, path)
    data = data.decode('UTF-8', 'replace')
    parsed = list(map(float, str(data).strip().split(', ')))
    return parsed

def load_lookerup_tables(filename="lookup_tables.csv", directory="data"):
    """Load lookup tables."""
    path = '/'.join((directory, filename))
    data = pkg_resources.resource_string(__name__, path)
    data = data.decode('UTF-8', 'replace')
    d = dict()
    for line in data.split('\n'):
        if line.startswith('#') or len(line) == 0:
            continue
        a, b, c, pattern = line.split(', ')
        d[(int(a), int(b), int(c))] = pattern
    return d
