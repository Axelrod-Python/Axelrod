from setuptools import setup

# Read in the requirements.txt file
with open('requirements.txt') as f:
    requirements = []
    for library in f.read().splitlines():
        if "hypothesis" not in library:  # Skip: used only for dev
            requirements.append(library)

# Read in long description
with open("README.rst", "r") as f:
    long_description = f.read()

# Read in the version number
exec(open('axelrod/version.py', 'r').read())

setup(
    name='Axelrod',
    version=__version__,
    install_requires=requirements,
    author='Vince Knight, Owen Campbell, Karol Langner, Marc Harper',
    author_email=('axelrod-python@googlegroups.com'),
    packages=['axelrod', 'axelrod.strategies', 'axelrod.data'],
    url='http://axelrod.readthedocs.org/',
    license='The MIT License (MIT)',
    description='Reproduce the Axelrod iterated prisoners dilemma tournament',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    include_package_data=True,
    package_data={
        '': ['axelrod/data/*.csv'],
    },
    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
        ],
    python_requires='>=3.5',
)
