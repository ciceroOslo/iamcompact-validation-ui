from pathlib import Path
import typing as tp

import pandas as pd
import pyam
import streamlit as st

from iamcompact_vetting.output.excel import MultiDataFrameExcelWriter
from iamcompact_nomenclature import (
    get_dsd,
    dimensions,
)
from iamcompact_nomenclature.validation import (
    get_invalid_names,
    get_invalid_variable_units,
)
from nomenclature import DataStructureDefinition

from common_elements import (
    check_data_is_uploaded,
    common_setup,
)
from common_keys import (
    PAGE_RUN_NAME,
    SSKey,
)
from page_defs import PageName


def main():

    common_setup()

    st.header('Run and summarize validation of names used in results')

    st.write(
        'This page runs validation checks for model, region, and variable names '
        'used in the uploaded results file, and variable/unit combinations. '
        'For each dimension, a red cross (❌) will be shown if any '
        'unrecognized names or variable/unit combinations were found, and a '
        'green checkmark (✅) otherwise.'
    )

    check_data_is_uploaded(display_message=True, stop=True) 

    iam_df: pyam.IamDataFrame = st.session_state.get(SSKey.IAM_DF_REGIONMAPPED,
                                                     None)
    if iam_df is None:
        st.info(
            '**NB!** You have not run the region mapping step. If your results '
            'contain model-specific region names, and the file you uploaded '
            'has not already gone through region mapping, you will probably '
            'see unrecognized names or errors in the region name check. Please '
            f'return to the page "{PageName.REGION_MAPPING}" if you need to '
            'remedy this.'
        )
        iam_df = st.session_state[SSKey.IAM_DF_UPLOADED]

    invalid_names_dict: dict[str, list[str]]|None = \
        st.session_state.get(SSKey.VALIDATION_INVALID_NAMES_DICT, None)
    # Print an info message, with an "info" icon
    if invalid_names_dict is None:
        st.info(
            'Name validation has not been run yet. Press the button below to '
            'run.',
            icon='ℹ️',
        )
        button_field = st.empty()
        if button_field.button('Run name checks'):
            button_field.empty()
            with st.spinner('Validating names and units...'):
                dsd: DataStructureDefinition = \
                    get_validation_dsd(allow_load=True, show_spinner=True)
                invalid_names_dict = get_invalid_names(iam_df, dsd)
                invalid_var_unit_combos = get_invalid_variable_units(iam_df, dsd)
                st.session_state[SSKey.VALIDATION_INVALID_NAMES_DICT] = \
                    invalid_names_dict
                st.session_state[SSKey.VALIDATION_INVALID_UNIT_COMBOS_DF] = \
                    invalid_var_unit_combos
            st.rerun()
        else:
            st.stop()
        button_field.empty()
    invalid_var_unit_combos: pd.DataFrame|None = \
        st.session_state[SSKey.VALIDATION_INVALID_UNIT_COMBOS_DF]
    st.write('Did checks.')

###END def main


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


if __name__ == PAGE_RUN_NAME:
    main()
