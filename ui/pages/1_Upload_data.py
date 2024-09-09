import tempfile

import pandas as pd
import pyam
import streamlit as st
from streamlit.elements.arrow import DataframeState
from streamlit_extras.switch_page_button import switch_page

from common_keys import SSKey
from utils import (
    clean_triple_textblock as mdblock,
    get_empty_iam_df,
)
from page_defs import (
    PageKey,
    pages,
)


# The option below should probably be removed, but just commenting out for now.
# I don't think we want to do anything that triggers chained assignment
# warnings.
# pd.options.mode.chained_assignment = None  # default='warn'

st.set_page_config(layout="wide")


def main():

    st.header("Upload modelling results for vetting")

    st.write(__name__)

    st.sidebar.header("Instructions")

    st.sidebar.markdown(mdblock(
        """Upload a file with modelling results using the page to the right,
        then go to subsequent pages to perform different vetting checks and view
        or download the results.

        The file to upload should be an Excel (.xlsx) or CSV file in IAMC \
        format. Please observe the following formatting rules:

        ### Column names
        * The data sheet(s) must have the columns "Model", "Scenario", "Region",
          "Variable", and "Unit" to the left.
        * Subsequent columns should have years as headers (e.g., 2015, 2020,
          etc.)
        * If you require additional columns (like "Subannual"), please contact
          the developers. Non-standard columns are likely to cause problems for
          the current version of the vetting checks.

        ### Excel file worksheets
        If uploading an Excel file:
        * All data (other than metadata) must be in one or more worksheets with
          names that start with "data" or "Data".
        * Metadata must be in a worksheet named "meta" (case-sensitive), though
          the metadata is not used in the current vetting checks and therefore
          is ignored for now.
        * All other worksheets will be ignored.

        ### Values
        * All rows *must* have values for the index columns ("Model",
          "Scenario", "Region", and "Variable"). "Unit" can be left blank for
          dimensionless units with no scale factor (but is otherwise mandatory).
        * No duplicate rows are allowed, i.e., all rows *must* have unique
          for the index columns, even for rows in different Excel worksheets.
        * Cells with missing data *must* be left blank. Do not use "NA", "-"
          or other non-numeric values. A value of "0" will be interpreted as a
          literal zero, and must not be used for missing values. Please check
          that Excel has not filled in zeros in blank cells.
        """
    ))

    def _clear_uploaded_iam_df():
        st.session_state[SSKey.IAM_DF_UPLOADED] = None
        st.session_state[SSKey.DO_INSPECT_DATA] = False
    uploaded_file = st.file_uploader(
        'Upload a spreadsheet file with modelling results in IAMC timeseries '
        'format.', 
        type=["xlsx", "csv"],
        key=SSKey.FILE_CURRENT_UPLOADED,
        on_change=_clear_uploaded_iam_df
    )

    # if uploaded_file is None:
    #     _clear_uploaded_iam_df()

    if uploaded_file is not None \
              and st.session_state[SSKey.IAM_DF_UPLOADED] is None:
        parsing_status_text = st.empty()
        parsing_status_text.info('Parsing uploaded file...', icon='⏳')
        # load data
        if uploaded_file.type == 'text/csv':
            with tempfile.NamedTemporaryFile(
                    mode='w',
                    encoding='utf-8',
                    suffix='.csv',
                    delete=True,
                    delete_on_close=False,
            ) as _file:
                _file.write(uploaded_file.getvalue().decode('utf-8'))
                raw_data: pyam.IamDataFrame = pyam.IamDataFrame(_file.name,
                                                                engine='c')
        else:
            with tempfile.NamedTemporaryFile(
                    mode='wb',
                    suffix='.xlsx',
                    delete=True,
                    delete_on_close=False,
            ) as _file:
                _file.write(uploaded_file.getvalue())
                raw_data: pyam.IamDataFrame = pyam.IamDataFrame(_file.name,
                                                                engine='calamine')

        st.session_state[SSKey.FILE_CURRENT_NAME] \
            = st.session_state[SSKey.FILE_CURRENT_UPLOADED].name
        st.session_state[SSKey.FILE_CURRENT_SIZE] = \
            st.session_state[SSKey.FILE_CURRENT_UPLOADED].size

        # Refresh all variables
        # ###
        # The state initialization below is partially old code from
        # i2am_paris_validation, needs to be cleaned up.
        # ###
        # st.session_state['validated_data'] = pd.DataFrame()
        # st.session_state['missing_values_count'] = None
        # st.session_state['duplicates_count'] = None
        # st.session_state['model_errors'] = None
        # st.session_state['region_errors'] = None
        # st.session_state['variable_errors'] = None
        # st.session_state['unit_errors'] = None
        # st.session_state['vetting_errors'] = None   

        # clean_results_dataset(raw_data)
        st.session_state[SSKey.IAM_DF_UPLOADED] = raw_data
        parsing_status_text.empty()

    df: pyam.IamDataFrame|None = st.session_state.get(SSKey.IAM_DF_UPLOADED)
    if df is not None:
        if uploaded_file is None:
            st.write(
                st.session_state[SSKey.FILE_CURRENT_NAME],
                f", {round(st.session_state[SSKey.FILE_CURRENT_SIZE]/1000,1)} "
                    "kB"
            )

        inspect_data_button_text: str = 'Inspect data'
        continue_button_text: str = 'Continue'
        next_page_name: str = 'AR6 vetting checks'
        next_page_key: PageKey = PageKey.AR6_VETTING

        inspect_info_text: str = 'File uploaded. Click ' \
            f'"{inspect_data_button_text}" to view the data in a table.'
        proceed_info_text: str = f'Click "{continue_button_text}" to ' \
            f'continue to the first vetting check ({next_page_name}), or ' \
            'click a page name in the left sidebar to jump directly to ' \
            'any check.'

        if not st.session_state.get(SSKey.DO_INSPECT_DATA, False):
            st.info(
                '\n\n'.join([inspect_info_text, proceed_info_text]),
                icon="ℹ️"
            )
            inspect_data_btn = st.button(inspect_data_button_text)
            if inspect_data_btn:
                st.session_state[SSKey.DO_INSPECT_DATA] = True
                st.rerun()
        else:
            st.info(
                proceed_info_text,
                icon="ℹ️"
            )
            # The call to `IamDataFrame.timeseries` here, as well as maybe
            # `st.dataframe`, does take some time and may be computationally
            # expensive. We should probably put them both inside a function
            # that can be st.cached.
            df_state = make_timeseries_table(df)
        validate_data_btn = st.button(continue_button_text)
        if validate_data_btn:
            st.switch_page(pages[next_page_key])

###END def main


def make_timeseries_table(idf: pyam.IamDataFrame) -> DataframeState:
    """Get the timeseries table of an IamDataFrame.

    Check the session state to see if `idf` is the same as the current uploaded
    IamDataFrame, and whether a timeseries table has already been generated.
    If so, use that.
    """
    timeseries: pd.DataFrame|None = None
    if idf is st.session_state.get(SSKey.IAM_DF_UPLOADED):
        timeseries = st.session_state.get(SSKey.IAM_DF_TIMESERIES, None)
    if timeseries is None:
        timeseries = idf.timeseries()
    return st.dataframe(timeseries)
###END def get_timeseries_table

# ###
# Commenting out the function below. Old function from i2am_paris_validation.
# ###
# def clean_results_dataset(df):
#     error = False
# 
#     str_cols = pd.to_numeric(df.columns, errors='coerce').isna()
#     numeric_cols = pd.to_numeric(df.columns, errors='coerce').notna()
# 
#     string_df = df.loc[:,str_cols].rename(columns=lambda x: re.sub('^[Mm][Oo][Dd][Ee][Ll]$', 'Model', x)) \
#                             .rename(columns=lambda x: re.sub('^[Ss][Cc][Ee][Nn][Aa][Rr][Ii][Oo]$', 'Scenario', x)) \
#                             .rename(columns=lambda x: re.sub('^[Rr][Ee][Gg][Ii][Oo][Nn]$', 'Region', x)) \
#                             .rename(columns=lambda x: re.sub('^[Vv][Aa][Rr][Ii][Aa][Bb][Ll][Ee]$', 'Variable', x)) \
#                             .rename(columns=lambda x: re.sub('^[Uu][Nn][Ii][Tt]$', 'Unit', x))
# 
#     for column in ['Model', 'Region', 'Scenario', 'Variable', 'Unit']:
#         if column not in df.columns:
#             st.error(f'Column {column} is missing or has a different name!', icon="🚨")
#             error = True
# 
#     if numeric_cols.sum()==0:
#         st.error(f'No year columns!', icon="🚨")
#         error = True
# 
#     numeric_df = df.loc[:,numeric_cols]
# 
#     numeric_df = numeric_df.apply(pd.to_numeric, axis=1, errors='coerce')
#     numeric_df.columns = pd.to_numeric(numeric_df.columns, errors='coerce')
# 
#     string_df = string_df.convert_dtypes()
# 
#     df = pd.concat([string_df, numeric_df], axis=1)
# 
#     st.session_state['clean_df'] = df
#     st.session_state['cleaning_error'] = error
# 
#     return df, error

main()
