from collections.abc import Mapping

import pandas as pd
import pyam
import streamlit as st

from iamcompact_vetting.iamcompact_outputs import \
    gdp_pop_harmonization_output

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

    st.header('GDP and population harmonization assessment')

    check_data_is_uploaded(stop=True, display_message=True)
    uploaded_iamdf: pyam.IamDataFrame = st.session_state[SSKey.IAM_DF_UPLOADED]

    status_area = st.empty()

    if st.session_state.get(SSKey.GDP_POP_OUTPUT_DFS, None) is None:
        status_area.info('Computing GDP and population harmonization checks...', icon='⏳')
        _dfs: Mapping[str, pd.DataFrame] = \
            compute_gdp_pop_harmonization_check(uploaded_iamdf)
        st.session_state[SSKey.GDP_POP_ALL_PASSED] = \
            _dfs[CriterionOutputKey.IN_RANGE].all(axis=None, skipna=True)
        st.session_state[SSKey.GDP_POP_ALL_INCLUDED] = \
            _dfs[CriterionOutputKey.IN_RANGE].all(axis=None, skipna=False)
        st.session_state[SSKey.GDP_POP_OUTPUT_DFS] = _dfs
        status_area.empty()
        del _dfs

    gdp_pop_harmonization_output_dfs: Mapping[str, pd.DataFrame] = \
        st.session_state[SSKey.GDP_POP_OUTPUT]

    status_area.markdown(
        make_passed_status_message(
            all_passed=st.session_state[SSKey.GDP_POP_ALL_PASSED],
            all_included=st.session_state[SSKey.GDP_POP_ALL_INCLUDED],
        )
    )


    summary_tab, deviation_tab, descriptions_tab = st.tabs(
        ['Statuses', 'Deviations', 'Descriptions']
    )
    with summary_tab:
        st.markdown(
            'Agreement with harmonization data within threshold, per '
            'model, scenario and region:'
        )
        st.dataframe(
            gdp_pop_harmonization_output_dfs[CriterionOutputKey.IN_RANGE]
        )
    with deviation_tab:
        st.markdown(
            'Relative deviation from harmonization data, normalized to 1.0 '
            '(i.e., 0.0 means identical with harmonization data, 0.5 means '
            '50% higher, and -0.5 means 50% lower):'
        )
        st.dataframe(
            gdp_pop_harmonization_output_dfs[CriterionOutputKey.VALUES] - 1.0
        )
    with descriptions_tab:
        st.info('Still to be added...', icon='🚧')

###END def mail


def compute_gdp_pop_harmonization_check(
    iamdf: pyam.IamDataFrame
) -> Mapping[str, pd.DataFrame]:
    return gdp_pop_harmonization_output(iamdf)
###END def compute_gdp_pop_harmonization_check


if __name__ == PAGE_RUN_NAME:
    main()
