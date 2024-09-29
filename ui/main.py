"""Main app runner."""

import streamlit as st
from streamlit.navigation.page import StreamlitPage

from page_defs import (
    PageKey,
    pages,
    name_validation_dims,
    name_validation_dim_pagekeys,
)



page: StreamlitPage = st.navigation(
    {
        '1. Start/upload': [
            pages[PageKey.UPLOAD],
        ],
        '2. Validation of names': [
            pages[PageKey.NAME_VALIDATION_SUMMARY],
        ] + [
            pages[name_validation_dim_pagekeys[_pagekey]]
            for _pagekey in name_validation_dims
        ] + [pages[PageKey.NAME_VALIDATION_VARIABLE_UNIT_COMBO]],
        '3. Region mapping': [
            pages[PageKey.REGION_MAPPING],
        ],
        '4. Vetting': [
            pages[PageKey.AR6_VETTING],
            pages[PageKey.GDP_POP_HARMONIZATION],
        ],
    }
)
page.run()
