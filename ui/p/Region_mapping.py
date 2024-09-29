"""Page to run reigon mapping and add it to session state before vetting."""

import pyam
import streamlit as st

from iamcompact_nomenclature.mapping import map_regions

from common_elements import (
    check_data_is_uploaded,
    common_setup,
)
from common_keys import (
    PAGE_RUN_NAME,
    SSKey,
)



def main() -> None:

    common_setup()

    st.header('Map/rename and aggregate regions')

    st.write(
        'This page maps/renames and aggregates model-specific regions to '
        'common regions with recognized region names.'
    )
    st.write(
        'Multi-country regions that are specific to a given model will in most '
        'cases be renamed by adding the model name as a prefix '
        '(`"Model|region"`), and aggregating to common regions.'
    )
    st.write(
        'Single-country regions or multi-country regions that are identical '
        'to a common region will in most cases be unchanged if they use the '
        'recognized common name, or otherwise renamed.'
    )
    st.write(
        'When completed, the region-mapped data will be used in the vetting '
        'steps.'
    )

    check_data_is_uploaded(display_message=True, stop=True)

    iam_df: pyam.IamDataFrame = st.session_state[SSKey.IAM_DF_UPLOADED]

    st.info(
        'Only recognized variable names can be included in the region '
        'mapping. Unrecognized variable names will cause the mapping function '
        'to fail. Please make sure that you have performed the name validation '
        'step and fixed or removed any unrecognized variables before '
        'proceeding.',
        icon='ℹ️',
    )

    include_excluded = st.checkbox(
        'Include regions/models that were excluded from region mapping in '
        'further processing.'
    )

    if st.session_state.get(SSKey.IAM_DF_REGIONMAPPED, None) is not None:
        st.info(
            'You have already performed the region-mapping step. You only need '
            'to press the button below if you for some reason want to run it '
            'again.',
            icon='✅'
        )
    run_mapping_button_area = st.empty()
    if not run_mapping_button_area.button('Perform region mapping'):
        st.stop()

    run_mapping_button_area.empty()
    regmapped_iam_df: pyam.IamDataFrame
    regmap_excluded_iam_df: pyam.IamDataFrame|None = None
    with st.spinner('Performing region mapping...'):
        if include_excluded:
            regmapped_iam_df, regmap_excluded_iam_df = map_regions(
                iam_df,
                return_excluded=include_excluded,
            )
        else:
            regmapped_iam_df = map_regions(iam_df, return_excluded=False)

    result_iam_df: pyam.IamDataFrame
    if include_excluded:
        with st.spinner('Combining results with excluded items...'):
            result_iam_df = pyam.concat(
                [regmapped_iam_df, regmap_excluded_iam_df]
            )
    else:
        result_iam_df = regmapped_iam_df

    st.session_state[SSKey.IAM_DF_REGIONMAPPED] = result_iam_df

    st.info(
        'Region mapping complete. You can now proceed with the vetting steps.',
        icon='✅',
    )
    
###END def mail


if __name__ == PAGE_RUN_NAME:
    main()
