# -*- coding: utf-8 -*-
"""
checks.py

Each function in here should

- Take a DataFrame as its first argument, maybe optional arguments
- Makes its assert on the result
- Return the original DataFrame
"""
import numpy as np
import pandas as pd
import pandas.util.testing as tm
import six

from engarde import generic
from engarde.generic import verify_df, verify_columns


def none_missing(df, columns=None):
    """
    Asserts that there are no missing values (NaNs) in the DataFrame.

    Parameters
    ----------
    df : DataFrame
    columns : list
      list of columns to restrict the check to

    Returns
    -------
    df : DataFrame
      same as the original
    """
    if columns is None:
        columns = df.columns
    try:
        assert not df[columns].isnull().any().any()
    except AssertionError as e:
        missing = df[columns].isnull()
        msg = generic.bad_locations(missing)
        e.args = msg
        raise
    return df

def is_monotonic(df, items=None, increasing=None, strict=False):
    """
    Asserts that the DataFrame is monotonic.

    Parameters
    ==========

    df : Series or DataFrame
    items : dict
        mapping columns to conditions (increasing, strict)
    increasing : None or bool
        None is either increasing or decreasing.
    strict : whether the comparison should be strict

    Returns
    =======
    df : DataFrame
    """
    if items is None:
        items = {k: (increasing, strict) for k in df}

    for col, (increasing, strict) in items.items():
        s = pd.Index(df[col])
        if increasing:
            good = getattr(s, 'is_monotonic_increasing')
        elif increasing is None:
            good = getattr(s, 'is_monotonic') | getattr(s, 'is_monotonic_decreasing')
        else:
            good = getattr(s, 'is_monotonic_decreasing')
        if strict:
            if increasing:
                good = good & (s.to_series().diff().dropna() > 0).all()
            elif increasing is None:
                good = good & ((s.to_series().diff().dropna() > 0).all() |
                               (s.to_series().diff().dropna() < 0).all())
            else:
                good = good & (s.to_series().diff().dropna() < 0).all()
        if not good:
            raise AssertionError
    return df

def is_shape(df, shape):
    """
    Asserts that the DataFrame is of a known shape.

    Parameters
    ==========

    df : DataFrame
    shape : tuple
      (n_rows, n_columns). Use None or -1 if you don't care
      about a dimension.

    Returns
    =======
    df : DataFrame
    """
    try:
        check = np.all(np.equal(df.shape, shape) | (np.equal(shape, [-1, -1]) |
                                                    np.equal(shape, [None, None])))
        assert check
    except AssertionError as e:
        msg = ("Expected shape: {}\n"
               "\t\tActual shape:   {}".format(shape, df.shape))
        e.args = (msg,)
        raise
    return df


def is_unique(df, columns=None):
    """
    Asserts that columns in the DataFrame only have unique values.

    Parameters
    ----------
    df : DataFrame
    columns : list or None
      list of columns to restrict the check to. If None, check all columns.

    Returns
    -------
    df : DataFrame
      same as the original
    """
    if columns is None:
        columns = df.columns
    for col in columns:
        if not df[col].is_unique:
            raise AssertionError("Column {!r} contains non-unique values".format(col))
    return df


def unique_index(df):
    """
    Assert that the index is unique

    Parameters
    ==========
    df : DataFrame

    Returns
    =======
    df : DataFrame
    """
    try:
        assert df.index.is_unique
    except AssertionError as e:
        e.args = df.index.get_duplicates()
        raise
    return df


def within_set(df, items=None):
    """
    Assert that df is a subset of items

    Parameters
    ==========
    df : DataFrame
    items : dict
      mapping of columns (k) to array-like of values (v) that
      ``df[k]`` is expected to be a subset of

    Returns
    =======
    df : DataFrame
    """
    for k, v in items.items():
        if not df[k].isin(v).all():
            bad = df.loc[~df[k].isin(v), k]
            raise AssertionError('Not in set', bad)
    return df

def within_range(df, items=None):
    """
    Assert that a DataFrame is within a range.

    Parameters
    ==========
    df : DataFame
    items : dict
      mapping of columns (k) to a (low, high) tuple (v)
      that ``df[k]`` is expected to be between.

    Returns
    =======
    df : DataFrame
    """
    for k, (lower, upper) in items.items():
        if (lower > df[k]).any() or (upper < df[k]).any():
            bad = (lower > df[k]) | (upper < df[k])
            raise AssertionError("Outside range", bad)
    return df

def within_n_std(df, n=3):
    """
    Assert that every value is within ``n`` standard
    deviations of its column's mean.

    Parameters
    ==========
    df : DataFame
    n : int
      number of standard devations from the mean

    Returns
    =======
    df : DatFrame
    """
    means = df.mean()
    stds = df.std()
    inliers = (np.abs(df - means) < n * stds)
    if not np.all(inliers):
        msg = generic.bad_locations(~inliers)
        raise AssertionError(msg)
    return df


def has_dtypes(df, items):
    """
    Assert that a DataFrame has ``dtypes`` as described in ``items``.

    Parameters
    ==========
    df: DataFrame
    items: dict
      A mapping of column names to:
      - functions (but **not** other  callables!) that take a pandas.Series.dtype instance as input, and
        return ``True`` if the ``dtype`` is of the correct dtype and ``False`` otherwise, and/or
      - strings, corresponding to the possible output values of ``pd.api.types.infer_dtype``, and/or
      - dtypes, or strings that can be converted to dtypes. For example, ``'int32'`` turns into
        np.dtype('int32')``.
      Instead of a mapping, items may also be a single value from above. For example, ``'int32'``
      check that all columns have dtype ``int32``.

    Returns
    =======
    df : DataFrame

    Examples
    =========

    .. code:: python
      import numpy as np
      import pandas as pd
      import engarde.checks as ck
      df = pd.DataFrame({'A': np.random.randint(0, 10, 10),
                         'B': np.random.randn(10)})
      df = df.pipe(ck.has_dtypes, items={'A': np.int32,
                                         'B': pd.api.types.is_float_dtype})
    """
    import types
    import typing
    from pandas.api.types import is_dtype_equal, infer_dtype

    if not isinstance(items, typing.Mapping):  # check all columns for items
        items = {col_name: items for col_name in df.columns}

    infer_strings = {
                    'string', 'unicode', 'bytes',
                    'floating', 'integer', 'mixed-integer',
                    'mixed-integer-float', 'complex,', 'categorical',
                    'boolean', 'datetime64', 'datetime',
                    'date', 'timedelta64', 'timedelta',
                    'time', 'period', 'mixed',
                    }
    for k, v in items.items():
        dtype = df.dtypes[k]
        if isinstance(v, (types.FunctionType, types.BuiltinFunctionType)):
            result = v(dtype)
            if not isinstance(result, bool):
                msg = "The function for key  {!r} must return a boolean, returned type {!r}"
                raise AssertionError(msg.format(k, type(result)))
            if not result:
                msg = "Column {!r} has the wrong dtype ({!r}) for function {!r}"
                raise AssertionError(msg.format(k, dtype, v.__name__))
        elif v in infer_strings:
            inferred_dtype_str = infer_dtype(df[k])
            if not inferred_dtype_str == v:
                msg = "Column {!r} expected {!r} for infer_dtype, got {!r}"
                raise AssertionError(msg.format(k, v, inferred_dtype_str))
        elif not is_dtype_equal(dtype, v):
            msg = "Column {!r} is checked for dtype {!r}, had dtype {!r}"
            raise AssertionError(msg.format(k, v, dtype))
    return df


def one_to_many(df, unitcol, manycol):
    """
    Assert that a many-to-one relationship is preserved between two
    columns. For example, a retail store will have have distinct
    departments, each with several employees. If each employee may
    only work in a single department, then the relationship of the
    department to the employees is one to many.

    Parameters
    ==========
    df : DataFrame
    unitcol : str
        The column that encapulates the groups in ``manycol``.
    manycol : str
        The column that must remain unique in the distict pairs
        between ``manycol`` and ``unitcol``

    Returns
    =======
    df : DataFrame

    """
    subset = df[[manycol, unitcol]].drop_duplicates()
    for many in subset[manycol].unique():
        if subset[subset[manycol] == many].shape[0] > 1:
            msg = "{} in {} has multiple values for {}".format(many, manycol, unitcol)
            raise AssertionError(msg)

    return df


def is_same_as(df, df_to_compare, **kwargs):
    """
    Assert that two pandas dataframes are the equal

    Parameters
    ==========
    df : pandas DataFrame
    df_to_compare : pandas DataFrame
    **kwargs : dict
        keyword arguments passed through to panda's ``assert_frame_equal``

    Returns
    =======
    df : DataFrame

    """
    try:
        tm.assert_frame_equal(df, df_to_compare, **kwargs)
    except AssertionError as exc:
        six.raise_from(AssertionError("DataFrames are not equal"), exc)
    return df


__all__ = ['is_monotonic', 'is_same_as', 'is_shape', 'none_missing',
           'unique_index', 'within_n_std', 'within_range', 'within_set',
           'has_dtypes', 'verify_df', 'verify_columns']

