"""Common functions to be used for defining pages."""
import functools
from pathlib import Path
import typing as tp

import streamlit as st
from streamlit.navigation.page import StreamlitPage

from iamcompact_nomenclature import dimensions as name_validation_dims

from p.name_validation_pages import (
    make_name_validation_dim_page,
)
from page_ids import (
    PageKey,
    PageName,
)



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
