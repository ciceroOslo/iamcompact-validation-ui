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

    AR6_CRITERIA_OUTPUT_DFS = 'ar6_criteria_output_dfs'
    """Output DataFrame from `.prepare_output` method of the AR6 criteria."""
    AR6_CRITERIA_ALL_PASSED = 'ar6_criteria_all_passed'
    """Whether all assessed AR6 vetting checks passed for all assessed
    models/scenarios.
    """
    AR6_CRITERIA_ALL_INCLUDED = 'ar6_criteria_all_included'
    """Whether all models/scenarios were assessed for all AR6 vetting checks."""

    GDP_POP_OUTPUT_DFS = 'gdp_pop_output_harmonization_dfs'
    """Output DataFrame from `.prepare_output` method of the GDP and population
    harmonization criteria.
    """
    GDP_POP_ALL_PASSED = 'gdp_pop_all_passed'
    """Whether all assessed GDP and population harmonization checks passed for
    all assessed models/scenarios.
    """
    GDP_POP_ALL_INCLUDED = 'gdp_pop_all_included'
    """Whether all models/scenarios were assessed for all GDP and population
    harmonization checks.
    """

    DISMISSED_WARNING = 'dismissed_warning'
    """Whether the warning about not using browser navigation buttons has been
    dismissed.
    """

###END class SSKey


class CriterionOutputKey(StrEnum):
    """Keys used in output from criterion `.prepare_output` methods."""

    IN_RANGE = 'in_range'
    """Key for DataFrame with in-range/not-in-range status, i.e., pass/fail."""

    VALUES = 'values'
    """Key for DataFrame with values returned by each criterion."""

    DISTANCES = 'distances'
    """Key for DataFrame with distance measure values."""

###END class CriterionOutputKey


PAGE_RUN_NAME: tp.Final[str] = '__page__'
"""Value of the `__name__` attribute of a page being run."""
