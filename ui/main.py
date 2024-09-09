"""Main app runner."""

import streamlit as st
from streamlit.navigation.page import StreamlitPage

from page_defs import (
    PageKey,
    pages,
)



page: StreamlitPage = st.navigation(list(pages.values()))
page.run()
