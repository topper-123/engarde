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


def verify_columns(df, items, *args, **kwargs):
    """
    Verify that all checks in items are True.

    Parameters
    ==========
    df : DataFrame
    items : function or dict of columns/functon mapping.
        Functions should take DataFrame, *args, and **kwargs.
        Should returns bool.

    Returns
    =======
    df : DataFrame
        same as the input.
    """
    from types import FunctionType
    msg = "Columns {!r} don't pass the checks."
    if isinstance(items, FunctionType):
        for col_name, column in df.items():
            assert items(column, *args, **kwargs), msg.format(col_name)
    else:
        for col_name, check_function in items.items():
            col = df[col_name]
            assert check_function(col, *args, **kwargs), msg.format(col_name)
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

