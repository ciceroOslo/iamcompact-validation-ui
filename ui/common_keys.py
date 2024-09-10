"""Common strings and keys used throughout the app."""

from enum import StrEnum
import typing as tp



class SSKey(StrEnum):
    """Keys used for the `streamlit.session_state` dictionary."""

    FILE_CURRENT_NAME = 'current_filename'
    """The name of the current uploaded file."""
    FILE_CURRENT_SIZE = 'current_file_size'
    """The size of the current uploaded file."""
    FILE_CURRENT_UPLOADED = 'uploaded_file'
    """The current uploaded file object."""

    IAM_DF_UPLOADED = 'uploaded_iam_df'
    """The IamDataFrame with data from the uploaded file."""
    IAM_DF_TIMESERIES = 'uploaded_iam_df_timeseries'
    """A generated timeseries table of the uploaded IamDataFrame."""

    DO_INSPECT_DATA = 'inspect_data'
    """Whether to display a table with the uploaded data, on the upload page."""

    DISMISSED_WARNING = 'dismissed_warning'

###END class SSKey


PAGE_RUN_NAME: tp.Final[str] = '__page__'
"""Value of the `__name__` attribute of a page being run."""
