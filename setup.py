from setuptools import setup

# Read in the requirements.txt file
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

# Read in the version number
exec(open('axelrod/version.py', 'r').read())

setup(
    name='Axelrod',
    version=__version__,
    install_requires=requirements,
    author='Vince Knight, Owen Campbell, Karol Langner, Marc Harper',
    author_email=('axelrod-python@googlegroups.com'),
    packages=['axelrod', 'axelrod.strategies', 'axelrod.tests'],
    url='http://axelrod.readthedocs.org/',
    license='The MIT License (MIT)',
    description='Reproduce the Axelrod iterated prisoners dilemma tournament',
)
