from distutils.core import setup

setup(
    name='Axelrod',
    version='0.0.2',
    author='Vince Knight',
    author_email='vincent.knight@gmail.com',
    packages=['axelrod', 'axelrod.strategies', 'axelrod.tests'],
    scripts=['run_tournament.py', 'README.rst'],
    url='http://axelrod.readthedocs.org/',
    license='The MIT License (MIT)',
    description='Reproduce the Axelrod iterated prisoners dilemma tournament',
    long_description=open('README.rst').read(),
    install_requires=[
        "matplotlib >= 1.4.2",
    ],
)
