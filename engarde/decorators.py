# -*- coding: utf-8 -*-
from __future__ import (unicode_literals, absolute_import, division)

from functools import wraps

import engarde.checks as ck

def none_missing(columns=None):
    """Asserts that no missing values (NaN) are found"""
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            ck.none_missing(result, columns=columns)
            return result
        return wrapper
    return decorate


def is_shape(shape):
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            ck.is_shape(result, shape)
            return result
        return wrapper
    return decorate


def unique(columns=None):
    """
    Asserts that columns in the DataFrame only have unique values.
    """
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            ck.unique(result, columns=columns)
            return result
        return wrapper
    return decorate


def unique_index():
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            ck.unique_index(result)
            return result
        return wrapper
    return decorate

def is_monotonic(items=None, increasing=None, strict=False):
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            ck.is_monotonic(result, items=items, increasing=increasing,
                            strict=strict)
            return result
        return wrapper
    return decorate

def within_set(items):
    """
    Check that DataFrame values are within set.

    >>> @within_set({'A': {1, 3}})
    >>> def f(df):
            return df
    """
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            ck.within_set(result, items)
            return result
        return wrapper
    return decorate


def within_range(items):
    """
    Check that a DataFrame's values are within a range.

    Parameters
    ==========
    items : dict or array-like
        dict maps columss to (lower, upper)
        array-like checks the same (lower, upper) for each column

    """
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            ck.within_range(result, items)
            return result
        return wrapper
    return decorate


def within_n_std(n=3):
    """
    Tests that all values are within 3 standard deviations
    of their mean.
    """
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            ck.within_n_std(result, n=n)
            return result
        return wrapper
    return decorate

def has_dtypes(items):
    """
    Tests that the dtypes are as specified in items.
    """
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            ck.has_dtypes(result, items)
            return result
        return wrapper
    return decorate


def one_to_many(unitcol, manycol):
    """ Tests that each value in ``manycol`` only is associated with
    just a single value in ``unitcol``.
    """
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            ck.one_to_many(result, unitcol, manycol)
            return result
        return wrapper
    return decorate


def verify_df(check, *args, **kwargs):
    """
    Assert that `check(df, *args, **kwargs)` is true.
    """
    def decorate(func):
        @wraps(func)
        def wrapper(*args_inner, **kwargs_inner):
            result = func(*args_inner, **kwargs_inner)
            ck.verify_df(result, check, *args, **kwargs)
            return result
        return wrapper
    return decorate


def verify_columns(items, *args, columns=None, **kwargs):
    """
    Assert that for all keys/values of items, `value(df[key], *args, **kwargs)` is true.
    """
    def decorate(func):
        @wraps(func)
        def wrapper(*args_inner, **kwargs_inner):
            result = func(*args_inner, **kwargs_inner)
            ck.verify_columns(result, items, *args, columns=columns, **kwargs)
            return result
        return wrapper
    return decorate


def verify_rows(items, *args, rows=None, **kwargs):
    """
    Assert ``items`` for for rows in df.
    """
    def decorate(func):
        @wraps(func)
        def wrapper(*args_inner, **kwargs_inner):
            result = func(*args_inner, **kwargs_inner)
            ck.verify_rows(result, items, *args, rows=None, **kwargs)
            return result
        return wrapper
    return decorate


def is_same_as(df_to_compare, **assert_kwargs):
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            ck.is_same_as(result, df_to_compare, **assert_kwargs)
            return result
        return wrapper
    return decorate


__all__ = ['is_monotonic', 'is_same_as', 'is_shape', 'none_missing',
           'unique_index', 'within_range', 'within_set', 'has_dtypes',
           'verify_df', 'verify_columns', 'within_n_std']

