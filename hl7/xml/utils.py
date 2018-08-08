import collections


def isinstance_all(iterable, class_or_tuple):
    """
    Check if all items of an iterable are instance of
    a class ou tuple of classes

    >>> isinstance_all(['Hello', 'World'], str)
    True
    >>> isinstance_all([1, 'Hello'], (str, int))
    True
    >>> isinstance_all([True, 'Hello', 5], int)
    False
    """
    return all(
        isinstance(obj, class_or_tuple)
        for obj in iterable
    )


def iter_without(iterable, without=None):
    """
    Returns iterable without certain value

    >>> iter_without([1, None, 2, 3, None, 4])
    [1, 2, 3, 4]
    >>> iter_without(['a', 'x', 'b', 'c'], without='x')
    ['a', 'b', 'c']
    """
    return type(iterable)(
        i for i in iterable
        if i is not without
    )


def len_without(iterable, without=None):
    """
    Returns a length of a iterable without certain value
    
    >>> len_without([1, None, 2, 3, None, 4])
    4
    """
    return len(iter_without(iterable, without))


def is_matrix(iterable):
    """
    Check if a iterable is an matrix (iterable of iterables)

    >>> is_recursive_iter([[1, 2, 3], [5, 6], [9, 10]])
    True
     >>> is_recursive_iter([1, 2, 3])
    False
    """
    if isinstance(iterable, (list, tuple)):
        return all(
            isinstance(i, (list, tuple))
            for i in iterable
        )
    return False


def flatten_matrix(iterable):
    """
    Generator flattening for matrix structures

    >>> list(flatten_matrix([[1, 2, 3], [4, 5, 6], [[7, 8, 9], [10, 11, 12]]]))
    [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]
    """

    for i in iterable:
      if is_matrix(i):
          yield from flatten_matrix(i)
      else:
          yield i