from collections.abc import Mapping

import pandas as pd
import pyam
import streamlit as st

from iamcompact_vetting.iamcompact_outputs import \
    ar6_vetting_target_range_output

from common_elements import (
    check_data_is_uploaded,
    common_instructions,
    make_passed_status_message,
)
from common_keys import (
    PAGE_RUN_NAME,
    SSKey,
    CriterionOutputKey,
)


def main():
    
    st.header('Vetting checks for IPCC AR6')

    check_data_is_uploaded(stop=True, display_message=True)
    uploaded_iamdf: pyam.IamDataFrame = st.session_state[SSKey.IAM_DF_UPLOADED]

    status_area = st.empty()

    if st.session_state.get(SSKey.AR6_CRITERIA_OUTPUT_DFS, None) is None:
        status_area.info('Computing IPCC AR6 vetting checks...', icon='⏳')
        _dfs: Mapping[str, pd.DataFrame] = \
            compute_ar6_vetting_checks(uploaded_iamdf)
        st.session_state[SSKey.AR6_CRITERIA_ALL_PASSED] = \
            _dfs[CriterionOutputKey.IN_RANGE].all(axis=None, skipna=True)
        st.session_state[SSKey.AR6_CRITERIA_ALL_INCLUDED] = \
            _dfs[CriterionOutputKey.IN_RANGE].all(axis=None, skipna=False)
        st.session_state[SSKey.AR6_CRITERIA_OUTPUT_DFS] = _dfs
        status_area.empty()
        del _dfs

    ar6_vetting_output_dfs: Mapping[str, pd.DataFrame] = \
        st.session_state[SSKey.AR6_CRITERIA_OUTPUT]

    status_area.markdown(
        '\n\n'.join([
            make_passed_status_message(
                all_passed=st.session_state[SSKey.AR6_CRITERIA_ALL_PASSED],
                all_included=st.session_state[SSKey.AR6_CRITERIA_ALL_INCLUDED],
            ),
            'Note: In AR6, only the checks on historical values were grounds '
            'for exclusion. The checks on future values (post-2020) were only '
            'a flag for possible issues.',
        ]),
        unsafe_allow_html=True,
    )

    in_range_tab, values_tab, descriptions_tab = st.tabs(
        ['Statuses', 'Values', 'Descriptions']
    )
    with in_range_tab:
        st.markdown(
            'Pass status per model and scenario. `True` for passed, `False` '
            'for not passed:'
        )
        st.dataframe(ar6_vetting_output_dfs[CriterionOutputKey.IN_RANGE])
    with values_tab:
        st.markdown('Values calculated for the vetting criteria per model and '
                    'scenario:')
        st.dataframe(ar6_vetting_output_dfs[CriterionOutputKey.VALUES])
    with descriptions_tab:
        st.markdown('Descriptions of each vetting criterion: ')
        st.info('Still to be added...', icon='🚧')

###END def main


def compute_ar6_vetting_checks(
    iamdf: pyam.IamDataFrame
) -> Mapping[str, pd.DataFrame]:
    """Compute vetting checks on the IAM DataFrame."""
    return ar6_vetting_target_range_output.prepare_output(iamdf)
###END def compute_ar6_vetting_checks


if __name__ == PAGE_RUN_NAME:
    main()
