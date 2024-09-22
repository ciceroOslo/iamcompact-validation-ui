"""Main app runner."""

import streamlit as st
from streamlit.navigation.page import StreamlitPage

from page_defs import (
    PageKey,
    pages,
)



page: StreamlitPage = st.navigation(
    {
        'Start': [
            pages[PageKey.UPLOAD],
        ],
        'Validation': [],
        'Vetting': [
            pages[PageKey.AR6_VETTING],
            pages[PageKey.GDP_POP_HARMONIZATION],
        ],
    }
)
page.run()
