from pathlib import Path

import pyam
import streamlit as st

from iamcompact_vetting.output.excel import MultiDataFrameExcelWriter

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


###END def main


if __name__ == PAGE_RUN_NAME:
    main()
