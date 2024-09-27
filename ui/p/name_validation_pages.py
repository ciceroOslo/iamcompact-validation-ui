import typing as tp

import pandas as pd
import pyam
import streamlit as st

from nomenclature import DataStructureDefinition

from iamcompact_nomenclature import get_dsd

from common_elements import (
    check_data_is_uploaded,
    common_setup,
)
from common_keys import SSKey
from page_ids import PageName



def make_name_validation_dim_page(
        dim_name: str,
        run_validation_page_name: tp.Optional[str] = None,
        header: tp.Optional[str] = None,
        intro_message: tp.Optional[str] = None,
        second_message: tp.Optional[str] = None,
        extra_message: tp.Optional[str] = None,
        invalid_names_dict_key: tp.Optional[SSKey] = None,
        dsd: tp.Optional[DataStructureDefinition] = None,
) -> None:

    common_setup()

    if invalid_names_dict_key is None:
        invalid_names_dict_key = SSKey.VALIDATION_INVALID_NAMES_DICT

    if run_validation_page_name is None:
        run_validation_page_name = PageName.NAME_VALIDATION_SUMMARY

    if header is not None:
        st.header(header)
    else:
        st.header(f'Validation of {dim_name} names')

    check_data_is_uploaded(display_message=True, stop=True)

    if invalid_names_dict_key not in st.session_state:
        st.info(
            'The name validation check has not been run yet. Please go to the '
            f'page "{run_validation_page_name}" in the navigation bar '
            'to the left to run it.',
            icon='⛔',
        )
        st.stop()

    if intro_message is not None:
        st.write(intro_message)
    else:
        st.write(
            f'The first tab below shows a list of all {dim_name} names that '
            'were not recognized. If the list is empty, all names should be '
            'valid.'
        )

    if second_message is not None:
        st.write(second_message)
    else:
        st.write(
            f'In the second tab, you can find a list of all valid {dim_name} '
            'names for reference, sorted alphabetically.'
        )

    if extra_message is not None:
        st.write(extra_message)

###END def make_name_validation_page


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
                dsd = get_dsd(force_reload=force_load)
        else:
            dsd = get_dsd(force_reload=force_load)
        st.session_state[SSKey.VALIDATION_DSD] = dsd
    return dsd
###END def get_validation_dsd
