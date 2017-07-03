topper-123-Engarde
==================

A fork of [Engarde](https://github.com/TomAugspurger/engarde), 
a python package for defensive data analysis. 

The differences between this fork and Engarde proper are:

* renamed ``verify`` to ``verify_df``.
* Added two new functions in ``generic``:
  * ``verify_columns``. Verifies columns. E.g.
    ``checks.verify_columns(df, lambda x: (x > 0).all())``
  * ``verify_rows``. Verifies rows. E.g.
    ``checks.verify_rows(df, lambda row: row.A > row.B)``
* Deleted ``verify_all`` and ``verify_any``. Basically I consider these
  less useful than ``verify_columns`` and ``verify_rows`` and I like that the API is small.
* ``verify_columns`` and ``verify_rows`` functions are added to ``checks`` and ``decorators``.
* ``has_dtypes`` can accept functions that return ``True`` if the test is passd 
  (typically the ones in ``pd.api.types``, e.g. ``is_integer_dtype``) and strings 
  like string output of ``pd.api.types.infer_dtypes``.

Installation
-------------

```bash
  pip install topper-123-engarde
```

and then in your python code:

```python
  import engarde
```

For details, see doc strings for relevant functions. For a tutorial, see
[Engarde's tutorial](http://engarde.readthedocs.io/en/latest/example.html),
but beware the differences.

