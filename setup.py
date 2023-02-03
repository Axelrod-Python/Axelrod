from collections import defaultdict
import os
import pathlib
from setuptools import setup

# Read in the requirements files.
requirements = defaultdict(list)

requirements_directory = pathlib.Path.cwd() / "requirements"
for filename in requirements_directory.glob("*.txt"):
    variant = filename.stem
    with filename.open() as libraries:
        for library in libraries:
            if len(library) > 0 and (not library.startswith("-r")):
                requirements[variant].append(library.strip())

# Grab the default requirements
install_requires = requirements["requirements"]
# Delete the default from the dictionary for the extra variants.
del requirements["requirements"]
extras_require = dict(requirements)

# Read in long description
with open("README.rst", "r") as f:
    long_description = f.read()

# Read in the version number
exec(open("axelrod/version.py", "r").read())

setup(
    name="Axelrod",
    version=__version__,
    install_requires=install_requires,
    author="Vince Knight, Owen Campbell, Karol Langner, Marc Harper",
    author_email=("axelrod-python@googlegroups.com"),
    packages=["axelrod", "axelrod.strategies", "axelrod.data"],
    url="http://axelrod.readthedocs.org/",
    license="The MIT License (MIT)",
    description="Reproduce the Axelrod iterated prisoners dilemma tournament",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    include_package_data=True,
    package_data={"": ["axelrod/data/*"]},
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3 :: Only",
    ],
    python_requires=">=3.6",
    extras_require=extras_require,
)
