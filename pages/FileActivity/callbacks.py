import time
from datetime import datetime
from dash import html
# import dash_enterprise_auth as auth
import pandas as pd
import plotly.express as px
from dash import Input, Output, State, callback, callback_context, clientside_callback, no_update
from sqlalchemy import text

from utils.db import get_pg_connection
import pymssql
conn = pymssql.connect(server='10.20.20.5:1501', user='pythonaperityetl01',
                       password='21SbAjsYdt!', database='COLL_TRANS')


EDITABLE_COLS = []
HIDDEN_COLS = ['comment', 'filepath', 'dir_results']


@callback(
    Output('file_data_original', 'data'),
    Output('file_process_name', 'data'),
    Output('file_process_name', 'columns'),
    Output('file_process_name', 'dropdown'),
    Output('file_process_name', 'hidden_columns'),
    # State('job_queue_name', 'data'),
    Input('search_filekey', 'value'),
    Input('cy_descr_dropdown', 'value'),
    Input('dropdown_provider', 'value'),

    Input('date-picker-update', 'date'),
    Input('date-picker-create', 'date'),
    Input('get_review_table', 'n_clicks')

)
def get_table(file_key, cycle_status, provider_id, date_picker_udpate, date_picker_create, *args):

    # df = pd.DataFrame(conn.execute(text(query)))
    # filtered_status = 'SUCCESS'

    query_file = f"""
            select top 100 'log' as LOG,technology_descr, file_key, concat(cy_status_id,'-(',cy_status_descr, ')') as cycle_status,
            period_id,import_table,concat(provider_id,'-(',provider_descr,')') as provider_descr,concat(provider_service_component_id,'-(',provider_service_component_descr,')') as service_descr,
            concat(pv_src_group_id,'-(',pv_src_group_descr,')') as service_group_descr,file_name,
            filepath,dir_results,comment
            from coll_trans.dbo.vscr_cy_file_process
            where 1 = 1
            """
    if file_key:
        query_file += f""" AND file_key ='{file_key}'"""
    if cycle_status:
        query_file += f""" AND cy_status_descr = '{cycle_status}'"""
    if provider_id:
        query_file += f""" AND provider_id = '{provider_id}'"""
    if date_picker_udpate:
        query_file += f""" AND update_date >= '{date_picker_udpate}'"""
    if date_picker_create:
        query_file += f""" AND create_date >= '{date_picker_create}'"""

    print(query_file)
    df = pd.read_sql_query(query_file, conn)
    columns = [{
        'id': i,
        'name': i,
        'editable': True if i in EDITABLE_COLS else False,
        'hideable': False if i not in HIDDEN_COLS else True,
        # 'presentation': 'dropdown' if i == 'exclude_flag' else 'input',
        'presentation': 'button' if i == 'LOG' else 'input'

    } for i in (df.columns)]

    data = df.to_dict('records')

    dropdowns = {
        'exclude_flag': {
            'options': [{'label': l, 'value': v} for l, v in [('YES', True), ('NO', False)]]
        }
    }

    return data, data, columns, dropdowns, HIDDEN_COLS


@callback(
    Output('modal', 'is_open'),
    Input('file_process_name', 'selected_rows'),
    State('file_process_name', 'derived_virtual_data'),
    prevent_initial_call=True
)
def open_modal(selected_rows, derived_virtual_data):
    if selected_rows:
        selected_row = derived_virtual_data[selected_rows[0]]
        row_id = selected_row['file_key']
        query_modal = f""" select file_key, msg from coll_trans.dbo.aud_log
                        where file_key = '{row_id}'
                    """
        df = pd.read_sql_query(query_modal, conn)
        content = html.Div([

        ])
    return content
