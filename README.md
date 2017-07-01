topper-123-Engarde
==================

A fork of [Engarde](https://github.com/TomAugspurger/engarde). The differences are:

* I've added ``is_unique`` to checks and decorators.
* Added three new functions in ``generic``:
  * ``verify_df``. Verifies whole dataframes. Basically same as Engarde's ``verify``.
  * ``verify_columns``. Verifies columns. E.g.
    ``checks.verify_columns(df, lambda x: (x > 0).all())``
  * ``verify_rows``. Verifies rows. E.g.
    ``checks.verify_rows(df, lambda row: row.A > row.B)``
* Deleted ``verify``, ``verify_all`` and ``verify_any``. Basically I consider these
  less useful than ``verify_columns`` and ``verify_rows``.

For details, see doc strings for relevant functions. For a tutorial, see
[Engarde's tutorial](http://engarde.readthedocs.io/en/latest/example.html),
but beware the differences.

