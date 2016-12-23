import pkg_resources

def load_data(filename, directory="data"):
    path = '/'.join((directory, filename))
    data = pkg_resources.resource_string(__name__, path)
    data = data.decode('UTF-8', 'replace')
    return data
