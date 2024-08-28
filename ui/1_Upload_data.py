import streamlit as st
import pandas as pd
import os
import re

from streamlit_extras.switch_page_button import switch_page

from utils import clean_triple_textblock as mdblock


pd.options.mode.chained_assignment = None  # default='warn'

st.set_page_config(layout="wide")


def main():

    st.header("Upload modelling results for vetting")

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

    uploaded_file = st.file_uploader("Upload a spreadsheet file with modelling results in IAMC timeseries format.", 
        type=["xlsx", "csv"],key="uploaded_file")


    if uploaded_file is not None:
        # load data
        if uploaded_file.type == 'text/csv':
            raw_data = pd.read_csv(uploaded_file)
        else:
            raw_data = pd.read_excel(uploaded_file)

        st.session_state['current_filename'] = st.session_state['uploaded_file'].name
        st.session_state['current_file_size'] = st.session_state['uploaded_file'].size

        # Refresh all variables
        # ###
        # The state initialization below is partially old code from
        # i2am_paris_validation, needs to be cleaned up.
        # ###
        st.session_state['validated_data'] = pd.DataFrame()
        st.session_state['missing_values_count'] = None
        st.session_state['duplicates_count'] = None
        st.session_state['model_errors'] = None
        st.session_state['region_errors'] = None
        st.session_state['variable_errors'] = None
        st.session_state['unit_errors'] = None
        st.session_state['vetting_errors'] = None   

        clean_results_dataset(raw_data)

    df = st.session_state.get('clean_df', pd.DataFrame())
    if not df.empty: 
        if uploaded_file is None:
            st.write(st.session_state['current_filename'],
                f", {round(st.session_state['current_file_size']/1000,1)} KB")

        st.dataframe(df)

        if st.session_state.get('cleaning_error'):
            st.info('Please fix the errors and upload a new file.', icon="ℹ️")
        else:
            st.info('The file has the correct column format! \
                Click the button below for validation.', icon="ℹ️")

            validate_data_btn = st.button('Validate data')
            
            if validate_data_btn:
                switch_page("Validate_data") 

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
# 
# 
# if __name__ == "__main__":
#     main()
