"""Main app runner."""

import streamlit as st
from streamlit.navigation.page import StreamlitPage

from page_defs import (
    PageKey,
    pages,
)



page: StreamlitPage = st.navigation(
    {
        '1. Start/upload': [
            pages[PageKey.UPLOAD],
        ],
        '2. Region mapping': [],
        '3. Validation of names': [
            pages[PageKey.NAME_VALIDATION_SUMMARY],
        ],
        '4. Vetting': [
            pages[PageKey.AR6_VETTING],
            pages[PageKey.GDP_POP_HARMONIZATION],
        ],
    }
)
page.run()
