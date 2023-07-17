from pandas import DataFrame as Dataframe


OPS = [
        ['ge ', '>='],
        ['le ', '<='],
        ['lt ', '<'],
        ['gt ', '>'],
        ['ne ', '!='],
        ['eq ', '='],
        ['contains '],
        ['datestartswith ']
    ]


def apply_filters(df_table: Dataframe, filter: str):
    """
    Apply a filter string to a pandas DataFrame.

    Args:
        df_table (DataFrame): The DataFrame to filter.
        filter (str): The filter string to apply.

    Returns:
        DataFrame: The filtered DataFrame.
    """
    df_table_filtered = df_table.copy()
    filtering_expressions = filter.split(' && ')
    for filter_part in filtering_expressions:
        if not filter_part:
            continue

        col_name, operator, filter_value = split_filter_part(filter_part)
        if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
            # these operators match pandas series operator method names
            df_table_filtered = df_table_filtered.loc[getattr(df_table_filtered[col_name], operator)(filter_value)]
        elif operator == 'contains':
            df_table_filtered = df_table_filtered.loc[df_table_filtered[col_name].str.contains(filter_value, na=False)]
        elif operator == 'datestartswith':
            # this is a simplification of the front-end filtering logic, only works with complete fields in standard format
            df_table_filtered = df_table_filtered.loc[df_table_filtered[col_name].str.startswith(filter_value)]

    return df_table_filtered

def split_filter_part(filter_part: str) -> tuple[str, str, str | float]:
    """
    Split a filter part string into its component parts.

    Args:
        filter_part (str): The filter part string to split.

    Returns:
        Tuple[str, str, Union[str, float]]: A tuple containing the column name, operator, and filter value.
    """
    for operator_type in OPS:
        for operator in operator_type:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find('{') + 1: name_part.rfind('}')]

                value_part = value_part.strip()
                v0 = value_part[0]
                if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
                    value = value_part[1: -1].replace('\\' + v0, v0)
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part

                # word operators need spaces after them in the filter string, but we don't want these later
                return name, operator_type[0].strip(), value

    raise ValueError(f'No operator found in filter part: {filter_part}')