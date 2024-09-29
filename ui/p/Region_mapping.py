"""Page to run reigon mapping and add it to session state before vetting."""

import streamlit as st

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

###END def mail


if __name__ == PAGE_RUN_NAME:
    main()
