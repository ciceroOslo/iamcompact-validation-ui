from collections.abc import (
    Callable,
    Iterable,
    Mapping,
)
import typing as tp

import pandas as pd
import pyam
import streamlit as st

from nomenclature import (
    DataStructureDefinition,
    CodeList,
)
from nomenclature.code import Code

from iamcompact_nomenclature import get_dsd

from common_elements import (
    check_data_is_uploaded,
    common_setup,
)
from common_keys import SSKey
from page_ids import PageName



def make_name_validation_dim_page(
        dim_name: str,
        run_validation_page_name: tp.Optional[str] = None,
        header: tp.Optional[str] = None,
        intro_message: tp.Optional[str] = None,
        second_message: tp.Optional[str] = None,
        extra_message: tp.Optional[str] = None,
        invalid_names_dict_key: tp.Optional[SSKey] = None,
        dsd: tp.Optional[DataStructureDefinition] = None,
        invalid_names_tab_name: str = 'Unrecognized names',
        all_valid_names_tab_name: str = 'All valid names',
        display_all_valid_names_tab: bool = True,
        invalid_names_display_func: tp.Optional[
            Callable[
                [list[str]|pd.DataFrame, str, tp.Optional[bool]], None]
        ] = None,
        all_valid_names_display_func: tp.Optional[
            Callable[[CodeList, str, tp.Optional[bool]], None]
        ] = None,
        show_valid_code_attrs: tp.Optional[Iterable[str]] = None,
        show_valid_code_colnames: tp.Optional[Mapping[str, str]] = None,
        sort_invalid_names: tp.Optional[bool] = None,
        sort_valid_names: tp.Optional[bool] = None,
) -> None:

    common_setup()

    if invalid_names_dict_key is None:
        invalid_names_dict_key = SSKey.VALIDATION_INVALID_NAMES_DICT

    if dsd is None:
        dsd = get_validation_dsd()

    if run_validation_page_name is None:
        run_validation_page_name = PageName.NAME_VALIDATION_SUMMARY

    if show_valid_code_attrs is None:
        if dim_name == 'region':
            show_valid_code_attrs = ['name', 'description', 'alpha_3',
                                     'countries', 'note']
        elif dim_name == 'variable':
            show_valid_code_attrs = ['name', 'description', 'unit', 'note']
        else:
            show_valid_code_attrs = ['name', 'description', 'note']

    if show_valid_code_colnames is None:
        if dim_name == 'region':
            show_valid_code_colnames = {
                'name': 'Name',
                'description': 'Description',
                'alpha_3': 'ISO3',
                'countries': 'Contains',
                'note': 'Note'
            }
        elif dim_name == 'variable':
            show_valid_code_colnames = {
                'name': 'Name',
                'description': 'Description',
                'unit': 'Valid units',
                'note': 'Note'
            }
        else:
            show_valid_code_colnames = {
                'name': 'Name',
                'description': 'Description',
                'note': 'Note'
            }

    if header is not None:
        st.header(header)
    else:
        st.header(f'Validation of {dim_name} names')

    check_data_is_uploaded(display_message=True, stop=True)

    if invalid_names_dict_key not in st.session_state:
        st.info(
            'The name validation check has not been run yet. Please go to the '
            f'page "{run_validation_page_name}" in the navigation bar '
            'to the left to run it.',
            icon='⛔',
        )
        st.stop()

    if intro_message is not None:
        st.write(intro_message)
    else:
        st.write(
            f'The first tab below shows a list of all {dim_name} names that '
            'were not recognized. If the list is empty, all names should be '
            'valid.'
        )

    if second_message is not None:
        st.write(second_message)
    else:
        st.write(
            f'In the second tab, you can find a list of all valid {dim_name} '
            'names for reference, sorted alphabetically.'
        )

    if extra_message is not None:
        st.write(extra_message)

    invalid_names_obj: dict[str, str]|pd.DataFrame \
        = st.session_state[invalid_names_dict_key]
    invalid_names: list[str]|pd.DataFrame
    if not isinstance(invalid_names_obj, pd.DataFrame):
        invalid_names = st.session_state[invalid_names_dict_key][dim_name]
    else:
        invalid_names = invalid_names_obj

    if display_all_valid_names_tab:
        invalid_names_tab, all_valid_names_tab = st.tabs(
            [
                invalid_names_tab_name,
                all_valid_names_tab_name,
            ]
        )
    else:
        invalid_names_tab, = st.tabs([invalid_names_tab_name])

    with invalid_names_tab:
        if invalid_names_display_func is not None:
            invalid_names_display_func(
                invalid_names,
                dim_name,
                sort_invalid_names,
            )
        else:
            if len(invalid_names) == 0:
                st.info(
                    f'No invalid {dim_name} names found.',
                    icon='✅',
                )
            else:
                if isinstance(invalid_names, pd.DataFrame):
                    raise TypeError(
                        'Invalid names cannot be given as a DataFrame when '
                        '`invalid_names_display_func` is not given.'
                    )
                _do_sort: bool
                if sort_invalid_names is None:
                    _do_sort = False if dim_name == 'region' else True
                else:
                    _do_sort = sort_invalid_names
                st.write(
                    'The following <span style="color: red"><b>unrecognized'
                    f'</b></span> {dim_name} names were found:',
                    unsafe_allow_html=True,
                )
                display_series: pd.Series = pd.Series(invalid_names, name='Name')
                if _do_sort:
                    display_series = display_series.sort_values()
                st.table(pd.Series(invalid_names, name='Name'))

    if display_all_valid_names_tab:
        with all_valid_names_tab:
            if all_valid_names_display_func is not None:
                all_valid_names_display_func(
                    getattr(dsd, dim_name),
                    dim_name,
                    sort_valid_names,
                )
            else:
                st.write(
                    'The following is a list of all <span style="color: green">'
                    f'recognized</span> {dim_name} names:',
                    unsafe_allow_html=True,
                )
                attribute_df: pd.DataFrame = make_attribute_df(
                    getattr(dsd, dim_name),
                    attr_names=show_valid_code_attrs,
                    column_names=show_valid_code_colnames,
                    use_filler='',
                )
                if sort_valid_names:
                    attribute_df = attribute_df.sort_values(
                        by=attribute_df.columns[0]
                    )
                st.table(attribute_df)

###END def make_name_validation_page


def make_variable_unit_combo_validation_page() -> None:

    def _invalid_names_display_func(
            invalid_combos: list[str]|pd.DataFrame,
            dim_name: str,
            sort_names: tp.Optional[bool] = None,
    ) -> None:
        if not isinstance(invalid_combos, pd.DataFrame):
            raise ValueError(
                'Invalid variable/unit combos must be given as a DataFrame.'
            )
        if len(invalid_combos) == 0:
            st.info(
                f'No invalid variable/unit combinations found.',
                icon='✅',
            )
        else:
            st.write(
                'Variables for which unrecognized units were found, and '
                'recognized units for each variable (does not include '
                'unrecognized *variables*):'
            )
            display_df: pd.DataFrame = invalid_combos.reset_index() \
                .astype(str).rename(
                    {
                        'variable': 'Variable',
                        'invalid': 'Unrecognized unit',
                        'expected': 'Valid unit(s)',
                    },
                    axis=1,
                )
            if sort_names is None or sort_names==True:
                display_df = display_df.sort_values('Variable')
            st.table(display_df)

    return make_name_validation_dim_page(
        dim_name='variable/unit combination',
        header='Validation of variable/unit combinations',
        intro_message='The table below shows recognized variables for which ' \
            'unrecognized units were found (unrecognized *variables* are not ' \
            'included).',
        second_message='The last column contains the variable or list of ' \
            'units that *is* recognized for the given variable.',
        invalid_names_dict_key=SSKey.VALIDATION_INVALID_UNIT_COMBOS_DF,
        invalid_names_tab_name='Unrecognized variable/unit combinations',
        display_all_valid_names_tab=False,
        invalid_names_display_func=_invalid_names_display_func,
    )

###END def make_variable_unit_combo_validation_page


@tp.overload
def get_validation_dsd(
    allow_load: tp.Literal[False],
    force_load: bool = False,
    show_spinner: bool = True,
) -> DataStructureDefinition|None:
    ...
@tp.overload
def get_validation_dsd(
    allow_load: bool = True,
    force_load: bool = False,
    show_spinner: bool = True,
) -> DataStructureDefinition:
    ...
def get_validation_dsd(
    allow_load: bool = True,
    force_load: bool = False,
    show_spinner: bool = True,
) -> DataStructureDefinition|None:
    """Get the DataStructureDefinition object for the validation checks.
    
    Parameters
    ----------
    allow_load : bool, optional
        Whether to allow loading the DataStructureDefinition object from the
        source (the `iamcompact_nomenclature.get_dsd` method) if it has not
        already been loaded. If False and the DataStructureDefinition object
        has not already been loaded, the function will return None.
    force_load : bool, optional
        Whether to force loading of the DataStructureDefinition object, i.e.,
        don't obtain it from the session state even if it is available.
        Optional, by default False.
    show_spinner : bool, optional
        Whether to show a spinner while loading. Optional, by default True.

    Returns
    -------
    DataStructureDefinition or None
        The DataStructureDefinition object for the validation checks if already
        loaded into session state or if `allow_load` is True. None if it has
        not been loaded and `allow_load` is False.
    """
    dsd: DataStructureDefinition|None = st.session_state.get(
        SSKey.VALIDATION_DSD, None)
    if (dsd is None and allow_load) or force_load:
        if show_spinner:
            with st.spinner('Loading datastructure definition...'):
                dsd = get_dsd(force_reload=force_load)
        else:
            dsd = get_dsd(force_reload=force_load)
        st.session_state[SSKey.VALIDATION_DSD] = dsd
    return dsd
###END def get_validation_dsd


def make_attribute_df(
        codelist: CodeList,
        attr_names: tp.Optional[Iterable[str]] = None,
        column_names: tp.Optional[Mapping[str, str]] = None,
        use_filler: bool|tp.Any = False,
) -> pd.DataFrame:
    """Make a DataFrame with the specified attributes of a CodeList.

    Parameters
    ----------
    codelist : CodeList
        The CodeList object to get the attributes from.
    attr_names : Iterable[str]
        The names of the attributes to include. Optional, by default
        `['name', 'description']`.
    column_names : Mapping[str, str]
        A mapping from attribute name to column name. Optional, by default uses
        the attribute names directly as column names.
    use_filler : bool or any
        Whether to use filler values for items that miss the given attributes
        (as opposed to raising an `AttributeError`). If `False` (bool literal),
        no filler will be used, and `AttributeError` will be most likely be
        raised if any of `attr_names` is missing for any of the code items. If
        any other value, that value will be used as for any attributes that are
        not found.

    Returns
    -------
    pd.DataFrame
        A DataFrame with the specified attributes listed in columns.
    """
    if attr_names is None:
        attr_names = ['name', 'description']
    if column_names is None:
        column_names = dict(zip(attr_names, attr_names))
    return_df: pd.DataFrame = pd.DataFrame(
        data=[
            [getattr(_code, _attr_name) for _attr_name in attr_names]
            if use_filler==False else
            [getattr(_code, attrname, use_filler) for attrname in attr_names]
            for _code in codelist.values()
        ],
        columns=list(column_names.values()),
        dtype=str,
    )
    if use_filler is not False:
        return_df = return_df.fillna(use_filler)
    return return_df
###END def make_attribute_df
