from distutils.core import setup

setup(
    name='Axelrod',
    version='0.0.6',
    author='Vince Knight, Owen Campbell, Karol Langner',
    author_email=('axelrod-python@googlegroups.com'),
    packages=['axelrod', 'axelrod.strategies', 'axelrod.tests'],
    scripts=['run_axelrod'],
    url='http://axelrod.readthedocs.org/',
    license='The MIT License (MIT)',
    description='Reproduce the Axelrod iterated prisoners dilemma tournament',
    install_requires=[
        "matplotlib >= 1.4.2",
    ],
)
