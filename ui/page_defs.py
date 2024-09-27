"""Common functions to be used for navigation between pages."""
from enum import StrEnum
import functools
from pathlib import Path
import typing as tp

import streamlit as st
from streamlit.navigation.page import StreamlitPage

from iamcompact_nomenclature import dimensions as name_validation_dims

from p.name_validation_pages import (
    make_name_validation_dim_page,
)



class PageName(StrEnum):
    """Page names."""

    UPLOAD = 'Upload data'
    """The front page, for uploading data"""

    REGION_MAPPING = 'Run region mapping'
    """Page for running region aggregation and mapping of model-native names"""

    NAME_VALIDATION_SUMMARY = 'Run / summary'
    """Page for running name validation and displaying summary results"""

    NAME_VALIDATION_VARIABLE = 'Variable names'
    """Page for displaying name validation results for variable names"""
    
    NAME_VALIDATION_MODEL = 'Model names'
    """Page for displaying name validation results for model names"""
    
    SCENARIO_VALIDATION_SCENARIO = 'Scenario names'
    """Page for displaying name validation results for scenario names"""

    NAME_VALIDATION_REGION = 'Region names'
    """Page for displaying name validation results for region names"""

    NAME_VALIDATION_VARIABLE_UNIT_COMBO = 'Variable/unit combinations'
    """Page for displaying validation results for variable/unit combinations"""
    
    AR6_VETTING = 'IPCC AR6 vetting'
    """Page for running IPCC AR6 vetting checks"""

    GDP_POP_HARMONIZATION = 'GDP and population harmonization'

###END class PageName

PageKey = PageName
"""Enum for keys used for pages in the `pages` dict. For now the keys are 
the same as the page names.
"""

name_validation_dim_pagekeys: tp.Final[dict[str, PageKey]] = {
    'variable': PageKey.NAME_VALIDATION_VARIABLE,
    'model': PageKey.NAME_VALIDATION_MODEL,
    'scenario': PageKey.SCENARIO_VALIDATION_SCENARIO,
    'region': PageKey.NAME_VALIDATION_REGION,
}
name_validation_dim_pagenames: tp.Final[dict[str, PageName]] = {
    'variable': PageName.NAME_VALIDATION_VARIABLE,
    'model': PageName.NAME_VALIDATION_MODEL,
    'scenario': PageName.SCENARIO_VALIDATION_SCENARIO,
    'region': PageName.NAME_VALIDATION_REGION,
}

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
    **{
        name_validation_dim_pagekeys[_dim]: st.Page(
            functools.partial(
                make_name_validation_dim_page,
                dim_name=_dim,
                run_validation_page_name=name_validation_dim_pagenames[_dim],
            ),
            title=name_validation_dim_pagenames[_dim],
        )
        for _dim in name_validation_dims
    },
    PageKey.AR6_VETTING: st.Page(
        page_folder / 'IPCC_AR6_vetting.py',
        title=PageName.AR6_VETTING,
    ),
    PageKey.GDP_POP_HARMONIZATION: st.Page(
        page_folder / 'Pop_GDP_harmonization.py',
        title=PageName.GDP_POP_HARMONIZATION,
    ),
}
