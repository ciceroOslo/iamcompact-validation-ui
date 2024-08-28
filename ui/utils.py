"""Utility functions for the app."""
import inspect



def clean_triple_textblock(textblock: str) -> str:
    """Dedents a triple-quoted string in the same way that Python typically
    does for docstrings.
    """
    return inspect.cleandoc(textblock)
