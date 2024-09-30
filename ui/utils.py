"""Utility functions for the app."""
import inspect

import pyam
import pandas as pd


def clean_triple_textblock(textblock: str) -> str:
    """Dedents a triple-quoted string in the same way that Python typically
    does for docstrings.
    """
    return inspect.cleandoc(textblock)


def get_empty_iam_df() -> pyam.IamDataFrame:
    """Get an empty IAM DataFrame.
    
    Returns an IamDataFrame with index columns and a single year column
    (year `0`), but no rows.
    """
    return pyam.IamDataFrame(
        pd.DataFrame(columns=pyam.IAMC_IDX+[0])
    )
