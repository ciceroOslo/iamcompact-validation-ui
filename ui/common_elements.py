"""Elements and navigation functions used across multiple pages."""

import typing as tp

import streamlit as st

from common_keys import SSKey
from page_defs import PageName



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
