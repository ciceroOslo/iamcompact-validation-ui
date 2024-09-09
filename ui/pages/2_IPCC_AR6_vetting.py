import pandas as pd
import pyam
import streamlit as st

from common_keys import (
    PAGE_RUN_NAME,
    SSKey,
)
from page_defs import (
    PageKey,
    pages,
)


def main():
    
    st.header('Vetting checks for IPCC AR6')

    df: pyam.IamDataFrame|None = \
        st.session_state.get(SSKey.IAM_DF_UPLOADED, None)
    if df is None:
        st.info('No data uploaded yet. Please go to the upload page and upload '
                'data first.', icon="ℹ️")
        st.stop()

    st.write('We found a file')

###END def main

if __name__ == PAGE_RUN_NAME:
    main()
