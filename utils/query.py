from sqlalchemy.sql.selectable import Select

from models import Base


def build_query_filter(model: Base, query: Select, filters_str: str):
    """
    Returns a SQLAlchemy query filtering the data using the provided filters.
    It assumes that the value part of the filter does not container ' && '.
    """

    if not filters_str:
        return query

    for filter in filters_str.split(' && '):
        column, operator, value = filter.split(' ', maxsplit=2)

        if column[0] == '{' and column[-1] == '}':
            column = column[1:-1]
        else:
            raise ValueError(f'Invalid filter string: {filters_str}')

        # Remove quotes present when value has multiple words
        if value[0] == '"' and value[-1] == '"':
            value = value[1:-1]

        model_col = getattr(model, column)

        if operator == 'scontains':
            query = query.where(model_col.ilike(f'%{value}%'))
        elif operator in ['gt', '>']:
            value = getattr(model, value, value)
            query = query.where(model_col > value)
        elif operator in ['gte', '>=']:
            value = getattr(model, value, value)
            query = query.where(model_col >= value)
        elif operator in ['lt', '<']:
            value = getattr(model, value, value)
            query = query.where(model_col < value)
        elif operator in ['lte', '<=']:
            value = getattr(model, value, value)
            query = query.where(model_col <= value)
        else:
            raise NotImplementedError(f'Unsupported operator type: {operator} in filter {filter}')

    return query


def build_query_sortby(model, query, sort_by):
    for i in sort_by:
        if i['direction'] == 'asc':
            query = query.order_by(getattr(model, i['column_id']).asc())
        elif i['direction'] == 'desc':
            query = query.order_by(getattr(model, i['column_id']).desc())

    return query

