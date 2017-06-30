# -*- coding: utf-8 -*-
"""
Module for useful generic functions.
"""
from itertools import chain, cycle

import numpy as np
import pandas as pd


# --------------
# Generic verify_df
# --------------

def verify_df(df, check, *args, **kwargs):
    """
    Verify dataframe. Assert that ``check(df, *args, **kwargs)`` is
    true.

    Parameters
    ==========
    df : DataFrame
    check : function
        Should take DataFrame and **kwargs. Returns bool

    Returns
    =======
    df : DataFrame
        same as the input.
    """
    result = check(df, *args, **kwargs)
    try:
        assert result
    except AssertionError as e:
        msg = '{} is not true'.format(check.__name__)
        e.args = (msg, df)
        raise
    return df

# -----------------------
# Generic verify_columns
# -----------------------

def verify_columns(df, func, *args, axis=0, how='all', **kwargs):
    """
    Verify that ``df.agg(func, axis, *args, **kwargs)`` are ``True``.

    Parameters
    ==========
    df : DataFrame
    func : callable, string, dictionary, or list of string/callable.
        Callables should take df, *args, and **kwargs as arguments and
        return a bool.
    axis : int
        Axis 0 or axis 1.
    how: str
        ``'all'`` means the check is only passed if all column checks evaluate to True.
        ``'any'`` means the check is passed if any column check evaluates to True.

    Returns
    =======
    df : DataFrame
        same as the input.
    """
    result = df.agg(func, axis, *args, **kwargs)
    if how == 'all':
        bool_result = result.all()
    elif how == 'any':
        bool_result = result.any()
    else:
        msg = "Parameter 'how' must be either 'all' or 'any', was {!r}"
        raise ValueError(msg.format(how))

    msg = "These columns don't pass the validation: {!r}"
    assert bool_result, msg.format(result[result == False].index.tolist())

    return df

# ---------------
# Error reporting
# ---------------

def bad_locations(df):
    columns = df.columns
    all_locs = chain.from_iterable(zip(df.index, cycle([col])) for col in columns)
    bad = pd.Series(list(all_locs))[np.asarray(df).ravel(1)]
    msg = bad.values
    return msg

__all__ = ['verify_df', 'verify_columns', 'bad_locations']

