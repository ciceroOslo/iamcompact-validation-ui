"""Common functions to be used for navigation between pages."""

import dataclasses
from enum import StrEnum
from pathlib import Path
import typing as tp

import streamlit as st



class PageName(StrEnum):
    """Page names."""

    UPLOAD = 'Upload data'
    """The front page, for uploading data"""
    
    AR6_VETTING = 'IPCC AR6 vetting'
    """Page for running IPCC AR6 vetting checks"""

###END class PageName

PageKey = PageName
"""Enum for keys used for pages in the `pages` dict. For now the keys are 
the same as the page names.
"""

page_folder: tp.Final[Path] = Path(__file__).parent / 'pages'

pages: tp.Final[dict[PageKey, tp.Any]] = {
    PageKey.UPLOAD: st.Page(
        page_folder / '1_Upload_data.py',
        title=PageName.UPLOAD,
        default=True,
    ),
    PageKey.AR6_VETTING: st.Page(
        page_folder / '2_IPCC_AR6_vetting.py',
        title=PageName.AR6_VETTING,
    ),
}
