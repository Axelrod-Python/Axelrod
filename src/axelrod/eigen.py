"""
Compute the principal eigenvector of a matrix using power iteration.

See also numpy.linalg.eig which calculates all the eigenvalues and
eigenvectors.
"""

from typing import Tuple

import numpy as np


def _normalise(nvec: np.ndarray) -> np.ndarray:
    """Normalises the given numpy array."""
    with np.errstate(invalid="ignore"):
        result = nvec / np.sqrt((nvec @ nvec))
    return result


def _squared_error(vector_1: np.ndarray, vector_2: np.ndarray) -> float:
    """Computes the squared error between two numpy arrays."""
    diff = vector_1 - vector_2
    s = diff @ diff
    return np.sqrt(s)


def _power_iteration(mat: np.array, initial: np.ndarray) -> np.ndarray:
    """
    Generator of successive approximations.

    Params
    ------
    mat: numpy.array
        The matrix to use for multiplication iteration
    initial: numpy.array, None
        The initial state. Will be set to np.array([1, 1, ...]) if None

    Yields
    ------
    Successive powers (mat ^ k) * initial
    """

    vec = initial
    while True:
        vec = _normalise(np.dot(mat, vec))
        yield vec


def principal_eigenvector(
    mat: np.array, maximum_iterations=1000, max_error=1e-3
) -> Tuple[np.ndarray, float]:
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
        Eigenvalue corresponding to the returned eigenvector
    """

    mat_ = np.array(mat)
    size = mat_.shape[0]
    initial = np.ones(size)

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
