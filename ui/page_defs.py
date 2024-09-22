"""Common functions to be used for navigation between pages."""

import dataclasses
from enum import StrEnum
from pathlib import Path
import typing as tp

import streamlit as st
from streamlit.navigation.page import StreamlitPage



class PageName(StrEnum):
    """Page names."""

    UPLOAD = 'Upload data'
    """The front page, for uploading data"""
    
    AR6_VETTING = 'IPCC AR6 vetting'
    """Page for running IPCC AR6 vetting checks"""

    GDP_POP_HARMONIZATION = 'GDP and population harmonization'

###END class PageName

PageKey = PageName
"""Enum for keys used for pages in the `pages` dict. For now the keys are 
the same as the page names.
"""

page_folder: tp.Final[Path] = Path(__file__).parent / 'p'

pages: tp.Final[dict[PageKey, StreamlitPage]] = {
    PageKey.UPLOAD: st.Page(
        page_folder / 'Upload_data.py',
        title=PageName.UPLOAD,
        default=True,
    ),
    PageKey.AR6_VETTING: st.Page(
        page_folder / 'IPCC_AR6_vetting.py',
        title=PageName.AR6_VETTING,
    ),
    PageKey.GDP_POP_HARMONIZATION: st.Page(
        page_folder / 'Pop_GDP_harmonization.py',
        title=PageName.GDP_POP_HARMONIZATION,
    ),
}
