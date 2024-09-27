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

    REGION_MAPPING = 'Run region mapping'
    """Page for running region aggregation and mapping of model-native names"""

    NAME_VALIDATION_SUMMARY = 'Run / summary'
    """Page for running name validation and displaying summary results"""
    
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
    PageKey.REGION_MAPPING: st.Page(
        page_folder / 'Region_mapping.py',
        title=PageName.REGION_MAPPING,
    ),
    PageKey.NAME_VALIDATION_SUMMARY: st.Page(
        page_folder / 'Validation_run_and_summary.py',
        title=PageName.NAME_VALIDATION_SUMMARY,
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
