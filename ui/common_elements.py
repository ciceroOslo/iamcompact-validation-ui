"""Elements and navigation functions used across multiple pages."""
from collections.abc import (
    Iterable,
    Mapping,
)
from pathlib import Path
import typing as tp

import iamcompact_nomenclature as icnom
from iamcompact_vetting.output.base import (
    CriterionTargetRangeOutput,
    MultiCriterionTargetRangeOutput,
)
from iamcompact_vetting.output.timeseries import \
    TimeseriesRefComparisonAndTargetOutput
from nomenclature import (
    CodeList,
    DataStructureDefinition,
)
import pandas as pd
from pandas.io.formats.style import Styler as PandasStyler
import streamlit as st

from common_keys import SSKey
from excel import write_excel_targetrange_output
from page_ids import PageName



def check_data_is_uploaded(
        *,
        stop: bool = True,
        display_message: bool = True,
) -> bool:
    """Check whether data has been uploaded, and optionally stop if not.
    
    The function checks whether the session state `SSKey.IAM_DF_UPLOADED` has a
    exists and has a non-None value. If not, the function by default displays
    a message telling the user to go back to the upload page, and by deafult
    stops execution.

    Parameters
    ----------
    stop : bool, optional
        Whether to stop execution if `SSKey.IAM_DF_UPLOADED` does not exist.
        Note that the function will not return if `stop` is True and no uploaded
        data is found. Optional, by default True.
    display_message : bool, optional
        Whether to display a message telling the user to go back to the upload
        page. Optional, by default True.

    Returns
    -------
    bool
        Whether uploaded data was found.
    """
    if st.session_state.get(SSKey.IAM_DF_UPLOADED, None) is None:
        if display_message:
            st.info(
                'No data uploaded yet. Please go to the upload page '
                    f'("{PageName.UPLOAD}") and upload data first.',
                icon="⛔"
            )
        if stop:
            st.stop()
        return False
    return True
###END def check_data_is_uploaded


def common_setup() -> None:
    """Common setup for all pages."""
    pass
###END def common_setup

def common_instructions() -> None:
    """Display common instructions for all pages.
    
    Note that some content may be displayed in the sidebar, and some may be
    displayed directly in the page body. This may also change over time. For
    that reason, the function should always be called at a point in the page
    code where any calls to `st.write`, `st.info` or similar methods are
    appropriate.
    """
    @st.dialog(title='NB!', width='large')
    def _dismissable_warnings():
        st.info(
            'Do not use browser back/forward buttons, or reload the page '
                'unless you wish to reset the data and start over.',
            icon="⚠️",
        )
        st.session_state[SSKey.DISMISSED_WARNING] = st.checkbox(
            'Do not show again until next run',
            value=True,
        )
    if not st.session_state.get(SSKey.DISMISSED_WARNING, False):
        _dismissable_warnings()
###END def common_instructions


def make_passed_status_message(all_passed: bool, all_included: bool) -> str:
    """Make an HTML message to display whether all checks have passed.

    Also makes a message to display whether all models/scenarios have been
    assessed for all checks.
    """
    all_passed_message: str
    all_included_message: str
    if all_passed:
        all_passed_message = '<p style="font-weight: bold">Status: ' \
            '<span style="color: green">All AR6 checks passed</span></p>'
    else:
        all_passed_message = '<p style="font-weight: bold">Status: ' \
            '<span style="color: red">Some AR6 checks failed</span></p>'
    if all_included:
        all_included_message = '<p style="font-weight: bold">Coverage: ' \
            '<span style="color: green">All models/scenarios assessed for ' \
            'all checks</span></p>'
    else:
        all_included_message = '<p style="font-weight: bold">Coverage: ' \
            '<span style="color: red">Some models/scenarios not assessed ' \
            'for some or all checks</span></p>'
    return '\n'.join([all_passed_message, all_included_message])
###END def make_status_message


@st.fragment
def download_excel_targetrange_output_button(
    output_data: pd.DataFrame|PandasStyler \
        | dict[str, pd.DataFrame|PandasStyler],
    outputter: CriterionTargetRangeOutput | MultiCriterionTargetRangeOutput \
        | TimeseriesRefComparisonAndTargetOutput,
    download_path_key: SSKey,
    download_file_name: str = 'download.xlsx',
    use_prepare_button: bool = True,
    download_button_text: str = 'Download xlsx',
    prepare_button_text: str = 'Prepare download',
    download_data_text: tp.Optional[str] = None,
    prepare_download_text: tp.Optional[str] = 'Press the button to prepare ' \
        'an Excel file for download.',
) -> None:
    """Download the output data as an Excel file.

    Parameters
    ----------
    output_data : pandas DataFrame, pandas Styler, or dict
        The output data to be downloaded.
    outputter : CriterionTargetRangeOutput or MultiCriterionTargetRangeOutput
        The outputter object to be used to write the data. Should be the same
        object that was used to generate `output_data` using its
        `prepare_output` or `prepare_styled_output` method.
    download_path_key : SSKey
        The session state key to use to store the path of the downloaded file.
    download_file_name : str, optional
        The name of the file to be downloaded. Optional, 'download.xlsx' by
        default.
    use_prepare_button : bool, optional
        Whether to present the user with a button that needs to be clicked
        before the output data is prepared. If True, rather than presenting the
        user directly with a download button, there will first be a button that
        the user must press, which will write the Excel data to a temporary
        file, and then replace the prepare button with a download button. This
        avoids having to spend time and disk space to write a file that might
        not get downloaded at all. If False, the function will prepare an Excel
        file for download immediately, and present a download button directly.
        Optional, True by default.
    download_button_text : str, optional
        The text to use for the download button. Optional, 'Download' by
        default.
    prepare_button_text : str, optional
        The text to use for the prepare button. Optional, 'Prepare download' by
        default.
    download_data_text : str or None, optional
        Text to display below the download button (after having prepared the
        download data). If None, no text element is displayed. Optional, None by
        default.
    prepare_download_text : str or None, optional
        Text to display below the prepare data button. Will only be displayed if
        `prepare_button` is True. Afer the download has been prepared and the
        download button is displayed, this text will be hidden. If None, no text
        element is displayed. Optional, None by default.
    """
    button_element = st.empty()
    text_element = st.empty()
    download_file_path: Path|None \
        = st.session_state.get(download_path_key, None)
    if download_file_path is None or not download_file_path.exists():
        if use_prepare_button:
            prepare_button = button_element.button(prepare_button_text)
            if prepare_download_text is not None:
                text_element.markdown(prepare_download_text)
            if not prepare_button:
                return
        download_file_path = write_excel_targetrange_output(
            output_data=output_data,
            outputter=outputter,
            file=None,
        )
        st.session_state[download_path_key] = download_file_path
    with open (download_file_path, 'rb') as _f:
        download_button = button_element.download_button(
            label=download_button_text,
            data=_f,
            file_name=download_file_name,
        )
    if download_data_text is not None:
        text_element.markdown(download_data_text)
    else:
        text_element.empty()
###END def download_excel_output_button


@tp.overload
def get_validation_dsd(
    allow_load: tp.Literal[False],
    force_load: bool = False,
    show_spinner: bool = True,
) -> DataStructureDefinition|None:
    ...
@tp.overload
def get_validation_dsd(
    allow_load: bool = True,
    force_load: bool = False,
    show_spinner: bool = True,
) -> DataStructureDefinition:
    ...
def get_validation_dsd(
    allow_load: bool = True,
    force_load: bool = False,
    show_spinner: bool = True,
) -> DataStructureDefinition|None:
    """Get the DataStructureDefinition object for the validation checks.
    
    Parameters
    ----------
    allow_load : bool, optional
        Whether to allow loading the DataStructureDefinition object from the
        source (the `iamcompact_nomenclature.get_dsd` method) if it has not
        already been loaded. If False and the DataStructureDefinition object
        has not already been loaded, the function will return None.
    force_load : bool, optional
        Whether to force loading of the DataStructureDefinition object, i.e.,
        don't obtain it from the session state even if it is available.
        Optional, by default False.
    show_spinner : bool, optional
        Whether to show a spinner while loading. Optional, by default True.

    Returns
    -------
    DataStructureDefinition or None
        The DataStructureDefinition object for the validation checks if already
        loaded into session state or if `allow_load` is True. None if it has
        not been loaded and `allow_load` is False.
    """
    dsd: DataStructureDefinition|None = st.session_state.get(
        SSKey.VALIDATION_DSD, None)
    if (dsd is None and allow_load) or force_load:
        if show_spinner:
            with st.spinner('Loading datastructure definition...'):
                dsd = icnom.get_dsd(force_reload=force_load)
        else:
            dsd = icnom.get_dsd(force_reload=force_load)
        st.session_state[SSKey.VALIDATION_DSD] = dsd
    return dsd
###END def get_validation_dsd


def make_attribute_df(
        codelist: CodeList,
        attr_names: tp.Optional[Iterable[str]] = None,
        column_names: tp.Optional[Mapping[str, str]] = None,
        use_filler: bool|tp.Any = False,
) -> pd.DataFrame:
    """Make a DataFrame with the specified attributes of a CodeList.

    Parameters
    ----------
    codelist : CodeList
        The CodeList object to get the attributes from.
    attr_names : Iterable[str]
        The names of the attributes to include. Optional, by default
        `['name', 'description']`.
    column_names : Mapping[str, str]
        A mapping from attribute name to column name. Optional, by default uses
        the attribute names directly as column names.
    use_filler : bool or any
        Whether to use filler values for items that miss the given attributes
        (as opposed to raising an `AttributeError`). If `False` (bool literal),
        no filler will be used, and `AttributeError` will be most likely be
        raised if any of `attr_names` is missing for any of the code items. If
        any other value, that value will be used as for any attributes that are
        not found.

    Returns
    -------
    pd.DataFrame
        A DataFrame with the specified attributes listed in columns.
    """
    if attr_names is None:
        attr_names = ['name', 'description']
    if column_names is None:
        column_names = dict(zip(attr_names, attr_names))
    return_df: pd.DataFrame = pd.DataFrame(
        data=[
            [getattr(_code, _attr_name) for _attr_name in attr_names]
            if use_filler==False else
            [getattr(_code, attrname, use_filler) for attrname in attr_names]
            for _code in codelist.values()
        ],
        columns=list(column_names.values()),
        dtype=str,
    )
    if use_filler is not False:
        return_df = return_df.fillna(use_filler)
    return return_df
###END def make_attribute_df
