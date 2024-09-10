import pandas as pd
import pyam
import streamlit as st

from common_elements import (
    check_data_is_uploaded,
    common_instructions,
)
from common_keys import (
    PAGE_RUN_NAME,
    SSKey,
)


def main():
    
    st.header('Vetting checks for IPCC AR6')

    check_data_is_uploaded(stop=True, display_message=True)
    df: pyam.IamDataFrame = st.session_state[SSKey.IAM_DF_UPLOADED]


###END def main

if __name__ == PAGE_RUN_NAME:
    main()
