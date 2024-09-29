"""Common strings and keys used throughout the app."""

from enum import StrEnum
import typing as tp

from iamcompact_vetting.output.iamcompact_outputs import (
    CTCol,
    IamCompactMultiTargetRangeOutput,
)



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
    IAM_DF_REGIONMAPPED = 'regionmapped_iam_df'
    """"""
    IAM_DF_TIMESERIES = 'uploaded_iam_df_timeseries'
    """A generated timeseries table of the uploaded IamDataFrame."""

    DO_INSPECT_DATA = 'inspect_data'
    """Whether to display a table with the uploaded data, on the upload page."""

    VALIDATION_DSD = 'validation_dsd'
    """Datastructure definition object to use for name validation."""
    VALIDATION_INVALID_NAMES_DICT = 'validation_invalid_names_dict'
    """Dictionary with invalid names per dimension.

    Contains the output from the name check if performed, or is unset or None
    if the name validation has not been run yet.
    """
    VALIDATION_INVALID_UNIT_COMBOS_DF = 'validation_invalid_unit_combos_df'
    """DataFrame with invalid unit combinations

    Contains a DataFrame with invalid variable/unit combinations and valid units
    for the same variables if the unit combo check has been run, or is unset or
    None otherwise.
    """

    REGION_MAPPING_EXCLUDE_INVALID_REGIONS = 'region_mapping_exclude_invalid_regions'
    """Whether to exclude invalid regions from the region-mapping step, and thus
    avoid letting the processing crash. This is the last state of the checkbox
    on the region-mapping page.
    """
    REGION_MAPPING_EXCLUDE_INVALID_VARIABLES = 'region_mapping_exclude_invalid_variables'
    """Whether to exclude invalid variables from the region-mapping step, and thus
    avoid letting the processing crash. This is the last state of the checkbox
    on the region-mapping page.
    """

    AR6_CRITERIA_OUTPUT_DFS = 'ar6_criteria_output_dfs'
    """Output DataFrame from `.prepare_output` method of the AR6 criteria."""
    AR6_CRITERIA_ALL_PASSED = 'ar6_criteria_all_passed'
    """Whether all assessed AR6 vetting checks passed for all assessed
    models/scenarios.
    """
    AR6_CRITERIA_ALL_INCLUDED = 'ar6_criteria_all_included'
    """Whether all models/scenarios were assessed for all AR6 vetting checks."""
    AR6_EXCEL_DOWNLOAD_PATH = 'ar6_excel_download_path'
    """Path to the Excel file to be downloaded with AR6 vetting results. None
    if no download file has been prepared yet.
    """

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
    GDP_POP_EXCEL_DOWNLOAD_PATH = 'gdp_pop_excel_download_path'
    """Path to the Excel file to be downloaded with GDP and population
    harmonization results. None if no download file has been prepared yet.
    """

    DISMISSED_WARNING = 'dismissed_warning'
    """Whether the warning about not using browser navigation buttons has been
    dismissed.
    """

###END class SSKey

data_file_upload_clear_keys: tp.Final[tp.List[SSKey]] = [
    SSKey.IAM_DF_UPLOADED,
    SSKey.DO_INSPECT_DATA,
    SSKey.IAM_DF_TIMESERIES,
    SSKey.IAM_DF_REGIONMAPPED,
    SSKey.VALIDATION_INVALID_NAMES_DICT,
    SSKey.VALIDATION_INVALID_UNIT_COMBOS_DF,
    SSKey.AR6_CRITERIA_OUTPUT_DFS,
    SSKey.AR6_CRITERIA_ALL_PASSED,
    SSKey.AR6_CRITERIA_ALL_INCLUDED,
    SSKey.AR6_EXCEL_DOWNLOAD_PATH,
    SSKey.GDP_POP_OUTPUT_DFS,
    SSKey.GDP_POP_ALL_PASSED,
    SSKey.GDP_POP_ALL_INCLUDED,
]


class CriterionColumn(StrEnum):
    """Column names used in output from criterion `.prepare_output` methods."""

    INRANGE = CTCol.INRANGE
    """Column name for in-range/not-in-range status, i.e., pass/fail."""

    VALUE = CTCol.VALUE
    """Column name for values returned by each criterion."""

###END class CriterionColumn

class Ar6CriterionOutputKey(StrEnum):
    """Keys used in output from AR6 criterion `.prepare_output` methods."""

    INRANGE = \
        IamCompactMultiTargetRangeOutput._default_summary_keys[CTCol.INRANGE]
    """Key for DataFrame with in-range/not-in-range status, i.e., pass/fail."""

    VALUE = \
        IamCompactMultiTargetRangeOutput._default_summary_keys[CTCol.VALUE]
    """Key for DataFrame with values returned by each criterion."""

###END class CriterionOutputKey


PAGE_RUN_NAME: tp.Final[str] = '__page__'
"""Value of the `__name__` attribute of a page being run."""
