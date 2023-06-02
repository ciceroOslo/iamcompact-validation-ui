import streamlit as st
import pandas as pd
import os

st.set_page_config(layout="wide")
st.title("Validator")
# col1, col2 = st.columns([1, 3])
# with col2:
#     placeholder = st.empty()

def main():
    uploaded_file = st.file_uploader("Upload data for validation", type=["xlsx", "xls"])
    
    if uploaded_file is not None:
        # load data
        data = pd.read_excel(uploaded_file)
        st.dataframe(data)

        # load validation data
        models = pd.read_excel('available_models_regions_variables_units.xlsx', sheet_name='models').Model.unique()
        regions = pd.read_excel('available_models_regions_variables_units.xlsx', sheet_name='regions').Region.unique()
        variables_units = pd.read_excel('available_models_regions_variables_units.xlsx', sheet_name='variable_units')
        variables = variables_units.Variable.unique()
        units = variables_units.Unit.unique()

        st.button('Validate', on_click=validate, args=(data, models, regions, variables, units))

def count_errors(df, column):
    index = list(df[column].value_counts().index)
    index.remove('')
    errors = df[column].value_counts()[index].values.sum()
    return errors

def validate(data, models, regions, variables, units):

    with st.spinner('Validating...'):
        
        # check if model is valid
        data['model_check'] = data.Model.apply(lambda x: 'Model ' + x + ' not found!' if x not in models else '')

        # check if region is valid
        data['region_check'] = data.Region.apply(lambda x: 'Region ' + x + ' not found!' if x not in regions else '')

        # check if variable is valid
        data['variable_check'] = data.Variable.apply(lambda x: 'Variable ' + x + ' not found!' if x not in variables else '')

        # check if unit is valid
        data['unit_check'] = data.Unit.apply(lambda x: 'Unit ' + x + ' not found!' if x not in units else '')

        # color errors with red
        styler = data.style.applymap(lambda x: f'background-color: red' if x!='' else f'background-color: white', subset=['model_check', 'region_check'])

        # write validated data to excel
        styler.to_excel('validation.xlsx', index=False)

    st.success('Validation Done!')

    # check if file was generated
    path = os.getcwd()
    print(path)
    if os.path.exists(path + '\\validation.xlsx'):
        save_file()
        with st.spinner('Loading Validated File...'):
            validated = pd.read_excel('validation.xlsx')
            st.title("Validated")

            # get data from styler object
            data = styler.data

            # count errors in models
            model_errors = count_errors(data, 'model_check')

            # count errors in regions
            region_errors = count_errors(data, 'region_check')

            # count errors in variables
            variable_errors = count_errors(data, 'variable_check')

            # count errors in units
            unit_errors = count_errors(data, 'unit_check')


            st.header(f'Errors with {model_errors} models, {region_errors} regions, {variable_errors} variables and {unit_errors} units!')
            print(validated['model_check'][:10])
            st.dataframe(validated.style.applymap(lambda x: f'background-color: red' if not pd.isna(x) else f'background-color: white', subset=['model_check', 'region_check', 'variable_check', 'unit_check']))
        # st.button('Show validated file', on_click=show_file)
    else:
        print('Not exists')

# @st.cache_data
# def convert_df(df):
#     return df.to_csv().encode('utf-8')

def save_file():
    # csv = convert_df(data)
    # st.download_button('Save validated file', csv, file_name='validated.csv', mime='text/csv')

    with open('validation.xlsx', 'rb') as template_file:
        template_byte = template_file.read()

        st.download_button(label="Save validated file",
                            data=template_byte,
                            file_name="validated.xlsx",
                            mime='application/octet-stream')

# def show_file():
    

if __name__ == "__main__":
    main()
