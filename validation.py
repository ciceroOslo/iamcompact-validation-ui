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
        variables_units_combination = (variables_units['Variable'] + ' ' + variables_units['Unit']).unique()

        st.button('Validate', on_click=validate, args=(data, models, regions, variables, units, variables_units_combination))

def count_errors(df, column):
    index = list(df[column].value_counts().index)
    index.remove('')
    errors = df[column].value_counts()[index].values.sum()
    return errors

def validate(data, models, regions, variables, units, variables_units_combination):

    with st.spinner('Validating...'):
        
        # check if model is valid
        data['model_check'] = data.Model.apply(lambda x: 'Model ' + x + ' not found!' if x not in models else '')

        # check if region is valid
        data['region_check'] = data.Region.apply(lambda x: 'Region ' + x + ' not found!' if x not in regions else '')

        # check if variable is valid
        data['variable_check'] = data.Variable.apply(lambda x: 'Variable ' + x + ' not found!' if x not in variables else '')

        # check if unit is valid
        data['unit_check'] = data.Unit.apply(lambda x: 'Unit ' + x + ' not found!' if x not in units else '')

        # check if variable unit combination is valid
        data['variable_unit_check']= data.apply(lambda x: f"Variable {x['Variable']} combined with unit {x['Unit']} not found!" if (x['Variable'] + ' ' + x['Unit']) not in variables_units_combination else '', axis=1)

        # check if there are any duplicates (we consider duplicates those entries that have same Model, Scenario, Region and Variable)
        data['duplicates_check'] = data.duplicated(['Model', 'Scenario', 'Region', 'Variable']).apply(lambda x: 'Duplicate' if x else '')

        # find possible mixed columns (strings and floats) and turn them to numeric columns, making the strings NaN
        for column in data.columns:
            if pd.api.types.infer_dtype(data[column]) == 'mixed-integer' or pd.api.types.infer_dtype(data[column]) == 'mixed-integer-float':
                data[column] = pd.to_numeric(data[column], errors = 'coerce')

        # vetting checks
        data['vetting_check'] = ''

        vetting_CO2_EIP_emissions = data[(data['Variable'] == 'Emissions|CO2|Energy and Industrial Processes') 
            & (data['Region'] == 'World')].apply(lambda x: 'vetting error' if x[2020] < 30116.8 or x[2020] > 45175.2 else '', axis=1)

        vetting_CH4_emissions = data[(data['Variable'] == 'Emissions|CH4') 
            & (data['Region'] == 'World')].apply(lambda x: 'vetting error' if x[2020] < 303.2 or x[2020] > 454.8 else '', axis=1)

        vetting_Primary_Energy = data[(data['Variable'] == 'Primary Energy') 
            & (data['Region'] == 'World')].apply(lambda x: 'vetting error' if x[2020] < 462.4 or x[2020] > 693.6 else '', axis=1)

        vetting_Electricity_Nuclear = data[(data['Variable'] == 'Secondary Energy|Electricity|Nuclear') 
            & (data['Region'] == 'World')].apply(lambda x: 'vetting error' if x[2020] < 6.839 or x[2020] > 12.701 else '', axis=1)

        vetting_No_net_negative_CO2_emissions_before_2030 = data[(data['Variable'] == 'Emissions|CO2') 
            & (data['Region'] == 'World')].apply(lambda x: 'vetting warning' if x[2030] < 0 or x[2030] > 1000000 else '', axis=1)

        vetting_Electricity_from_Nuclear_in_2030 = data[(data['Variable'] == 'Secondary Energy|Electricity|Nuclear') 
            & (data['Region'] == 'World')].apply(lambda x: 'vetting warning' if x[2030] < 0 or x[2030] > 20 else '', axis=1)

        vetting_CH4_emissions_in_2040 = data[(data['Variable'] == 'Emissions|CH4') 
            & (data['Region'] == 'World')].apply(lambda x: 'vetting warning' if x[2040] < 100 or x[2040] > 1000 else '', axis=1)

        vettings = [vetting_CO2_EIP_emissions, vetting_CH4_emissions, vetting_Primary_Energy, vetting_Electricity_Nuclear,\
            vetting_No_net_negative_CO2_emissions_before_2030, vetting_Electricity_from_Nuclear_in_2030, vetting_CH4_emissions_in_2040]

        for vetting in vettings:
            for key, value in vetting.to_dict().items():
                data['vetting_check'][key] = value

        # color errors, duplicates and vetting errors with red, missing values and vetting warnings with yellow
        styler = data.style.applymap(lambda x: f'background-color: red' if 'not found' in str(x) or 'Duplicate' in str(x) or 'vetting error' in str(x) else (f'background-color: yellow' if str(x) == 'nan' or 'vetting warning' in str(x) else f'background-color: white'))

        # write validated data to excel
        styler.to_excel('validation.xlsx', index=False)


    path = os.getcwd()
    print('\n\n\nPath', path, '\n\n\n')

    st.success('Validation Done!')

    # check if file was generated
    
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

            # count errors in variable unit combinations
            variable_unit_errors = count_errors(data, 'variable_unit_check')

            # count duplicates
            duplicates_count = count_errors(data, 'duplicates_check')

            # count missing or invalid values
            missing_values_count = data.isna().sum().values.sum()

            # count vetting errors and warnings
            vetting_errors_warnings = count_errors(data, 'vetting_check')

            if model_errors or region_errors or variable_errors or unit_errors or variable_unit_errors or duplicates_count:
                st.header(f'Errors with {model_errors} models, {region_errors} regions, {variable_errors} variables, {unit_errors} units,\
                          {variable_unit_errors} variable units combinations. Found {vetting_errors_warnings} vetting errors and warnings. Found {duplicates_count} duplicates and {missing_values_count} missing or invalid values!')
            else:
                st.header('No errors or duplicates found!')
            print(validated['model_check'][:10])
            st.dataframe(validated.style.applymap(lambda x: f'background-color: red' if not pd.isna(x) else f'background-color: white', subset=['model_check', 'region_check', 'variable_check', 'unit_check', 'variable_unit_check', 'duplicates_check']))
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
