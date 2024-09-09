"""Common functions to be used for navigation between pages."""

from enum import StrEnum

import streamlit as st
from streamlit_extras.switch_page_button import switch_page



class PageName(StrEnum):
    """Page names."""

    UPLOAD = 'Upload data'
    """The front page, for uploading data"""
    
    AR6_VETTING = 'IPCC AR6 vetting'
    """Page for running IPCC AR6 vetting checks"""

###END class PageName

page_order: list[PageName] = [PageName.UPLOAD, PageName.AR6_VETTING]
"""The order of appearance of the pages, starting with the front page."""
