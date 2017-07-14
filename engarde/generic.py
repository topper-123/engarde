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
# Generic verify_df_series
# -----------------------

def verify_df_series(df, func, *args, columns=None, rows=None, axis=0, how='all', **kwargs):
    """
    Verify that ``df.agg(func, axis, *args, **kwargs)`` are ``True``.

    Parameters
    ==========
    df : DataFrame
    func : callable, string or dictionary of callables.
        Callables should take df, *args, and **kwargs as arguments and
        return a bool.
    columns: str, list, slice object etc.
        Same as allowed for df.loc
    rows : str, list, slice object etc.
        Same as allowed for df.loc
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
    rows, columns = rows or slice(None), columns or slice(None)
    check_df = df.loc[rows, columns]

    result_df = check_df.agg(func, axis, *args, **kwargs)
    if how == 'all':
        result = result_df.all()
    elif how == 'any':
        result = result_df.any()
    else:
        msg = "Parameter 'how' must be either 'all' or 'any', was {!r}"
        raise ValueError(msg.format(how))

    if axis == 0:
        msg = "These columns don't pass the validation: {!r}"
    else:
        msg = "These rows don't pass the validation: {!r}"
    not_passed_cols = result_df[result_df == False].index.tolist()
    assert result, msg.format(not_passed_cols)

    return df


def verify_columns(df, func, *args, columns=None, how='all', **kwargs):
    """
    Verify that ``func`` validates for each column in df.

    Parameters
    ==========
    df : DataFrame
    func : callable, string or dictionary of callables.
        Callables should take df, *args, and **kwargs as arguments and
        return a bool.
    columns: str, list, slice object etc.
        Same as allowed for df.loc
    how: str
        ``'all'`` means the check is only passed if all column checks evaluate to True.
        ``'any'`` means the check is passed if any column check evaluates to True.

    Returns
    =======
    df : DataFrame
        same as the input.
    """
    return verify_df_series(df, func, *args, columns=columns, axis=0, how=how, **kwargs)


def verify_rows(df, func, *args, rows=None, how='all', **kwargs):
    """
    Verify that ``func`` validates for rows in df.

    Parameters
    ==========
    df : DataFrame
    func : callable, string or dictionary of callables.
        Callables should take df, *args, and **kwargs as arguments and
        return a bool.
    rows : str, list, slice object etc.
        Same as allowed for df.loc
    how: str
        ``'all'`` means the check is only passed if all column checks evaluate to True.
        ``'any'`` means the check is passed if any column check evaluates to True.

    Returns
    =======
    df : DataFrame
        same as the input.
    """
    return verify_df_series(df, func, *args, rows=rows, axis=1, how=how, **kwargs)


# ---------------
# Error reporting
# ---------------

def bad_locations(df):
    columns = df.columns
    all_locs = chain.from_iterable(zip(df.index, cycle([col])) for col in columns)
    bad = pd.Series(list(all_locs))[np.asarray(df).ravel(1)]
    msg = bad.values
    return msg

__all__ = ['verify_df', 'verify_df_series', 'verify_columns', 'verify_rows', 'bad_locations']

