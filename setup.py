from distutils.core import setup

setup(
    name='Axelrod',
    version='0.1dev',
    packages=['axelrod', 'axelrod.strategies', 'axelrod.tests'],
    scripts=['run_tournament.py'],
    license='The MIT License (MIT)',
    long_description=open('README.md').read(),
)
