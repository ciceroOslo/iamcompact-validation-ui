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
    st.info(
        '**NB!** Do not use browser back/forward buttons, or reload the page '
            'unless you wish to reset the data and start over.',
        icon="⚠️",
    )
