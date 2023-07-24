import streamlit as st
import pandas as pd
import os
import re

from streamlit_extras.switch_page_button import switch_page

pd.options.mode.chained_assignment = None  # default='warn'

st.set_page_config(layout="wide")

KNOWN_MODELS_REGIONS_VARS = 'input_data/available_models_regions_variables_units.xlsx'
VETTING_CHECKS = 'input_data/vetting_checks.pdf'


def main():
    st.header('Validate modelling results')

    st.sidebar.header("Instructions")

    st.sidebar.markdown("The following validation checks are available:")

    st.sidebar.markdown("*Consistency of model, variable, and region names*: \
        Check if the models, variables, or regions of the uploaded file exist in the I2AM PARIS database.")

    st.sidebar.markdown("*Vetting checks*: \
        Check whether the values of key variables fall within reasonable ranges based on \
        past measurements or future estimations. Vetting is based on the \
        IPCC AR6 vetting rules found in the IPCC AR6 Working Group III report, Annex III, Table 11\
        [(link)](https://www.ipcc.ch/report/ar6/wg3/downloads/report/IPCC_AR6_WGIII_Annex-III.pdf).")

    st.sidebar.markdown("*Consistency between disaggregated and aggregated variables*: \
        Check whether the values of aggregated variables correspond to the sum of their respective \
            disaggregated variables (an error margin of 2\% is accepted).")


    df = st.session_state.get('clean_df', pd.DataFrame())
    cleaning_error = st.session_state.get('cleaning_error')
    if not df.empty and not cleaning_error:
        st.markdown('Please select the validation check you want to perform:')
        indices_check = st.checkbox('Consistency of model, variable, and region names', value=True)
        vetting_check = st.checkbox('Vetting checks', value=True)
        basic_sums_check = st.checkbox('Consistency between disaggregated and aggregated variables', value=False)

        validate_button_disable = False
        if not (indices_check or vetting_check or basic_sums_check):
            validate_button_disable = True
            st.info('Please select at least one check.')

        validate_button = st.button('Confirm validation', on_click=validate, args=(df, indices_check, vetting_check, basic_sums_check),
                disabled=validate_button_disable)
        
        if validate_button:
            raw_data.empty()
    else: 
        st.info('No data for validation. Please upload first a results dataset with correct format.', icon="ℹ️")

        validate_data_btn = st.button('Upload data')
        
        if validate_data_btn:
            switch_page("Upload data") 

@st.cache_data
def load_known_names():
    models = pd.read_excel(KNOWN_MODELS_REGIONS_VARS, sheet_name='models').Model.unique()
    regions = pd.read_excel(KNOWN_MODELS_REGIONS_VARS, sheet_name='regions').Region.unique()
    variables_units = pd.read_excel(KNOWN_MODELS_REGIONS_VARS, sheet_name='variable_units')
    variables = variables_units.Variable.unique()
    units = variables_units.Unit.unique()
    variables_units_combination = (variables_units['Variable'] + ' ' + variables_units['Unit']).unique()

    return models,regions,variables_units,variables,units,variables_units_combination


def check_value_format(data):
    numeric_columns =  data.columns[pd.to_numeric(data.columns, errors='coerce').notna()]

    # find possible mixed columns (strings and floats) and turn them to numeric columns, making the strings NaN
    for column in numeric_columns:
        # if pd.api.types.infer_dtype(data[column]) == 'mixed-integer' or pd.api.types.infer_dtype(data[column]) == 'mixed-integer-float':
        data[column] = pd.to_numeric(data[column], errors = 'coerce')

    return data


def check_duplicates(data):
    # check if there are any duplicates (we consider duplicates those entries that have same Model, Scenario, Region and Variable)
    data['duplicates_check'] = data.duplicated(['Model', 'Scenario', 'Region', 'Variable']).apply(lambda x: 'Duplicate' if x else '')

    return data


def check_indices(data):
    models,regions,variables_units,variables,units,variables_units_combination = load_known_names()

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

    return data


def check_vetting(data):
    # create empty vetting check column
    data['vetting_check'] = ''

    # create empty vettings list where the vetting results are stored as Series with index the original index of the entry and value the result of the vetting check
    vettings_results = []

    # list of dictionaries with the basic vettings
    vetting_list = [{'variable': 'Emissions|CO2|Energy and Industrial Processes', 'low': 30116.8, 'high': 45175.2, 'year': 2020, 'error': 'Vetting error: CO2 EIP emissions'},
                    {'variable': 'Emissions|CH4', 'low': 303.2, 'high': 454.8, 'year': 2020, 'error': 'Vetting error: CH4 emissions'},
                    {'variable': 'Primary Energy', 'low': 462.4, 'high': 693.6, 'year': 2020, 'error': 'Vetting error: Primary Energy'},
                    {'variable': 'Secondary Energy|Electricity|Nuclear', 'low': 6.839, 'high': 12.701, 'year': 2020, 'error': 'Vetting error: Electricity Nuclear'},
                    {'variable': 'Emissions|CO2', 'low': 0, 'high': 1000000, 'year': 2030, 'error': 'Vetting warning: No net negative CO2 emissions before 2030'},
                    {'variable': 'Secondary Energy|Electricity|Nuclear', 'low': 0, 'high': 20, 'year': 2030, 'error': 'Vetting warning: Electricity from Nuclear in 2030'},
                    {'variable': 'Emissions|CH4', 'low': 100, 'high': 1000, 'year': 2040, 'error': 'Vetting warning: CH4 emissions in 2040'}]

    # creating Series objects with index the index of the error or warning and value the vetting error or warning if exists and appending them to the vetting_results
    for vetting in vetting_list:
        # basic vetting checks
        vettings_results.append(data[(data['Variable'] == vetting['variable']) 
            & (data['Region'] == 'World')].apply(lambda x: f"{vetting['error']} for year {vetting['year']}. Range must be between {vetting['low']} and {vetting['high']}." if x[vetting['year']] < vetting['low'] or x[vetting['year']] > vetting['high'] else '', axis=1))

    # list of dictionaries with the sum vettings
    vettings_list = [{'variable1': 'Emissions|CO2|AFOLU', 'variable2': 'Emissions|CO2|Energy and Industrial Processes', 'low': 26550.6, 'high': 61951.4, 'year': 2020, 'error': 'Vetting error: CO2 total emissions (EIP + AFOLU)'},
                     {'variable1': 'Carbon Sequestration|CCS|Biomass|Energy', 'variable2': 'Carbon Sequestration|CCS|Fossil|Energy', 'low': 0, 'high': 250, 'year': 2020, 'error': 'Vetting error: CCS from Energy 2020 '},
                     {'variable1': 'Secondary Energy|Electricity|Wind', 'variable2': 'Secondary Energy|Electricity|Solar', 'low': 4.255, 'high': 12.765, 'year': 2020, 'error': 'Vetting error: Electricity Solar & Wind'},
                     {'variable1': 'Carbon Sequestration|CCS|Biomass|Energy', 'variable2': 'Carbon Sequestration|CCS|Fossil|Energy', 'low': 0, 'high': 2000, 'year': 2030, 'error': 'Vetting warning: CCS from Energy in 2030'}]

    for vetting in vettings_list:
        # vetting sums checks
        vetting_group = data[((data['Variable'] == vetting['variable1']) | (data['Variable'] == vetting['variable2']))
                        & (data['Region'] == 'World')].groupby(['Model', 'Scenario']).sum()[vetting['year']]
        
        # get indexes with sum out of bounds
        indexes = vetting_group[(vetting_group < vetting['low']) | (vetting_group > vetting['high'])].index
        for index in indexes:
            # append Series object with index the index of the error or warning and value the vetting error or warning
            vettings_results.append(pd.Series({data[(data['Model'] == index[0]) & (data['Scenario'] == index[1]) & (data['Variable'] == vetting['variable1']) & (data['Region'] == 'World')].index[0]: f"{vetting['error']} for year {vetting['year']}. Sum range must be between {vetting['low']} and {vetting['high']}."}))
            vettings_results.append(pd.Series({data[(data['Model'] == index[0]) & (data['Scenario'] == index[1]) & (data['Variable'] == vetting['variable2']) & (data['Region'] == 'World')].index[0]: f"{vetting['error']} for year {vetting['year']}. Sum range must be between {vetting['low']} and {vetting['high']}."}))

    # percent change between 2010-2020 vetting check 
    vettings_results.append(data[(data['Variable'] == 'Emissions|CO2|Energy and Industrial Processes') 
            & (data['Region'] == 'World')].apply(lambda x: 'Vetting error: CO2 emissions EIP 2010-2020 - % change' if abs((x[2020]-x[2010])/x[2010]) > 0.5 else '', axis=1))

    # write vetting results to the original dataframe's vetting_check column
    for vetting in vettings_results:
        for key, value in vetting.to_dict().items():
            data['vetting_check'][key] = value

    return data


def check_basic_sums(data):

    numeric_columns =  data.columns[pd.to_numeric(data.columns, errors='coerce').notna()]

    # create a list with the aggregated variables
    aggr_vars = []
    unique_vars = data.Variable.unique()
    for var in unique_vars:
        var_levels = var.count('|')

        if var_levels > 0:
            for level in range(0,var_levels):
                test_aggr_var = var.rsplit("|",level+1)[0]

                if test_aggr_var in unique_vars:
                    if test_aggr_var not in aggr_vars:
                        aggr_vars.append(test_aggr_var)
                        break

    # create dictionary with keys the aggregated variables and values the disaggregated variables
    var_tree = {}
    for var in unique_vars:
        var_levels = var.count('|')

        if var_levels > 0:
            for level in range(0,var_levels):
                test_aggr_var = var.rsplit("|",level+1)[0]

                if test_aggr_var in unique_vars:
                    if test_aggr_var not in var_tree.keys():
                        if var not in aggr_vars:
                            var_tree[test_aggr_var] = [var]
                    else:
                        if var not in aggr_vars:
                            var_tree[test_aggr_var].append(var)

    # check basic sums
    data['basic_sum_check'] = ''
    for variable in var_tree.keys():
        # get data that have the aggregated variable
        agg_results = data[data['Variable'].isin(var_tree[f'{variable}'])].groupby(['Model', 'Scenario', 'Region']).sum()[numeric_columns]

        for row in agg_results.index:
            for year in numeric_columns:
                values = data[(data['Model'] == row[0]) & (data['Scenario'] == row[1]) & (data['Region'] == row[2])  & (data['Variable'] == variable)][year].values
                if len(values) != 0:
                    # find percentage difference using the formula |x1 - x2|/((x1+x2)/2)
                    diff = (abs(values[0] - agg_results[year][row[0]][row[1]][row[2]]))/((values[0] + agg_results[year][row[0]][row[1]][row[2]])/2)
                    
                    # set difference margin at 2%
                    if diff > 0.02:
                        data.loc[(data['Model'] == row[0]) & (data['Scenario'] == row[1]) & (data['Region'] == row[2])  & (data['Variable'] == variable), 'basic_sum_check'] += f'Basic sum check error on year {year}.     \n'

    return data


def validate(data, indices_check, vetting_check, basic_sums_check):
        with st.spinner('Validating...'):

            # default checks
            data = check_value_format(data)

            data = check_duplicates(data)

            if indices_check:
                data = check_indices(data)

            if vetting_check:
                data = check_vetting(data)               

            if basic_sums_check:
                data = check_basic_sums(data)               

            # color errors, duplicates and vetting errors with red, missing values and vetting warnings with yellow
            styler = data.style.applymap(lambda x: f'background-color: red' if 'not found' in str(x) or 'Duplicate' in str(x) or 'Vetting error' in str(x) else (f'background-color: yellow' if str(x) == 'nan' or 'Vetting warning' in str(x) or 'sum check error' in str(x) else f'background-color: white'))

            # write validated data to excel
            styler.to_excel('validation.xlsx', index=False)


        path = os.getcwd()

        st.success(f'Validation Done!')

        # check if file was generated
        
        if os.path.exists(os.path.join(path,'validation.xlsx')):
            save_file()
            with st.spinner('Loading Validated File...'):
                validated = pd.read_excel('validation.xlsx')
                # st.title("Validated")

                # # get data from styler object
                # data = styler.data

                # # count errors in models
                # model_errors = count_errors(data, 'model_check')

                # # count errors in regions
                # region_errors = count_errors(data, 'region_check')

                # # count errors in variables
                # variable_errors = count_errors(data, 'variable_check')

                # # count errors in units
                # unit_errors = count_errors(data, 'unit_check')

                # # count errors in variable unit combinations
                # variable_unit_errors = count_errors(data, 'variable_unit_check')

                # # count duplicates
                # duplicates_count = count_errors(data, 'duplicates_check')

                # # count missing or invalid values
                # missing_values_count = data.isna().sum().values.sum()

                # # count vetting errors and warnings
                # vetting_errors_warnings = count_errors(data, 'vetting_check')

                # # count basic sum errors
                # basic_sum_check_errors = data.basic_sum_check.str.count('year').sum()

                # if model_errors or region_errors or variable_errors or unit_errors or variable_unit_errors or duplicates_count:
                #     st.header(f'Errors with {model_errors} models, {region_errors} regions, {variable_errors} variables, {unit_errors} units,\
                #             {variable_unit_errors} variable units combinations! Found {vetting_errors_warnings} vetting errors and warnings! Found {duplicates_count} duplicates and {missing_values_count} missing or invalid values! Found {basic_sum_check_errors} basic sum errors across variables!')
                # else:
                #     st.header('No errors or duplicates found!')
                # print(validated['model_check'][:10])
                st.dataframe(validated)#.style.applymap(lambda x: f'background-color: red' if not pd.isna(x) else f'background-color: white', subset=['model_check', 'region_check', 'variable_check', 'unit_check', 'variable_unit_check', 'duplicates_check']))
            # st.button('Show validated file', on_click=show_file)
        else:
            print(30*'#')
            print('+ Validation file does not exist')
            print(30*'#'+"\n")


def count_errors(df, column):
    index = list(df[column].value_counts().index)
    index.remove('')
    errors = df[column].value_counts()[index].values.sum()
    return errors

def save_file():

    with open('validation.xlsx', 'rb') as template_file:
        template_byte = template_file.read()

        st.download_button(label="Save validated file",
                            data=template_byte,
                            file_name="validated.xlsx",
                            mime='application/octet-stream')
    

if __name__ == "__main__":
    main()
