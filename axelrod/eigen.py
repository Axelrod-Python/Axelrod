"""
Compute the principal eigenvector of a matrix using power iteration.

See also numpy.linalg.eig which calculates all the eigenvalues and
eigenvectors.
"""

import numpy


def normalise(nvec):
    """Normalises the given numpy array."""
    return nvec / numpy.sqrt(numpy.dot(nvec, nvec))


def squared_error(vector_1, vector_2, sqrt=True):
    """Computes the squared error between two numpy arrays."""
    diff = vector_1 - vector_2
    s = numpy.dot(diff, diff)
    if sqrt:
        return numpy.sqrt(s)
    return s


def power_iteration(mat, initial=None):
    """
    Generator of successive approximations.

    Params
    ------
    mat: numpy.matrix
        The matrix to use for multiplication iteration
    initial: numpy.array, None
        The initial state. Will be set to numpy.array([1, 1, ...]) if None

    Yields
    ------
    Successive powers (mat ^ k) * initial
    """

    if initial is None:
        size = mat.shape[0]
        initial = normalise(numpy.ones(size))
    vec = initial
    while True:
        vec = normalise(numpy.dot(mat, vec))
        yield vec


def principal_eigenvector(mat, maximum_iterations=None, max_error=1e-8):
    """
    Computes the (normalised) principal eigenvector of the given matrix.

    Params
    ------
    mat: numpy.matrix
        The matrix to use for multiplication iteration
    initial: numpy.array, None
        The initial state. Will be set to numpy.array([1, 1, ...]) if None
    maximum_iterations: int, None
        The maximum number of iterations of the approximation
    max_error: float, 1e-8
        Exit criterion -- error threshold of the difference of successive steps
    """

    mat_ = numpy.matrix(mat)
    size = mat_.shape[0]
    initial = numpy.ones(size)

    # Power iteration
    if not maximum_iterations:
        maximum_iterations = float('inf')
    last = initial
    for i, vector in enumerate(power_iteration(mat, initial=initial)):
        if i > maximum_iterations:
            break
        if squared_error(vector, last) < max_error:
            break
        last = vector
    # Compute the eigenvalue (Rayleigh quotient)
    eigenvalue = numpy.dot(
        numpy.dot(mat_, vector), vector) / numpy.dot(vector, vector)
    # Liberate the eigenvalue from numpy
    eigenvalue = float(eigenvalue)
    return (vector, eigenvalue)
