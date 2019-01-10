"""
Compute the principal eigenvector of a matrix using power iteration.

See also numpy.linalg.eig which calculates all the eigenvalues and
eigenvectors.
"""

from typing import Tuple

import numpy


def _normalise(nvec: numpy.ndarray) -> numpy.ndarray:
    """Normalises the given numpy array."""
    with numpy.errstate(invalid="ignore"):
        result = nvec / numpy.sqrt((nvec @ nvec))
    return result


def _squared_error(vector_1: numpy.ndarray, vector_2: numpy.ndarray) -> float:
    """Computes the squared error between two numpy arrays."""
    diff = vector_1 - vector_2
    s = diff @ diff
    return numpy.sqrt(s)


def _power_iteration(mat: numpy.array, initial: numpy.ndarray) -> numpy.ndarray:
    """
    Generator of successive approximations.

    Params
    ------
    mat: numpy.array
        The matrix to use for multiplication iteration
    initial: numpy.array, None
        The initial state. Will be set to numpy.array([1, 1, ...]) if None

    Yields
    ------
    Successive powers (mat ^ k) * initial
    """

    vec = initial
    while True:
        vec = _normalise(numpy.dot(mat, vec))
        yield vec


def principal_eigenvector(
    mat: numpy.array, maximum_iterations=1000, max_error=1e-3
) -> Tuple[numpy.ndarray, float]:
    """
    Computes the (normalised) principal eigenvector of the given matrix.

    Params
    ------
    mat: numpy.array
        The matrix to use for multiplication iteration
    maximum_iterations: int, None
        The maximum number of iterations of the approximation
    max_error: float, 1e-8
        Exit criterion -- error threshold of the difference of successive steps

    Returns
    -------
    ndarray
        Eigenvector estimate for the input matrix
    float
        Eigenvalue corresonding to the returned eigenvector
    """

    mat_ = numpy.array(mat)
    size = mat_.shape[0]
    initial = numpy.ones(size)

    # Power iteration
    if not maximum_iterations:
        maximum_iterations = float("inf")
    last = initial
    for i, vector in enumerate(_power_iteration(mat, initial=initial)):
        if i > maximum_iterations:
            break
        if _squared_error(vector, last) < max_error:
            break
        last = vector
    # Compute the eigenvalue (Rayleigh quotient)
    eigenvalue = ((mat_ @ vector) @ vector) / (vector @ vector)
    # Liberate the eigenvalue from numpy
    eigenvalue = float(eigenvalue)
    return vector, eigenvalue
