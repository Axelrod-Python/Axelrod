from distutils.core import setup

setup(
    name='Axelrod'
    version='0.1dev'
    packages=['axelrod'],
    scripts=['run_tournament.py'],
    license='The MIT License (MIT)'
    long_description=open(’README.md’).read(),
)
