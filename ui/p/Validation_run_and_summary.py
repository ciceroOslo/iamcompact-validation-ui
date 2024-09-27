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
from p.name_validation_pages import get_validation_dsd
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
