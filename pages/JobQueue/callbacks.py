import time
from datetime import datetime

# import dash_enterprise_auth as auth
import pandas as pd
import plotly.express as px
from dash import Input, Output, State, callback, callback_context, clientside_callback, no_update
from sqlalchemy import text

from utils.db import get_pg_connection
import pymssql
conn = pymssql.connect(server='10.20.20.5:1501', user='pythonaperityetl01',
                       password='21SbAjsYdt!', database='COLL_TRANS')


EDITABLE_COLS = ['status']
HIDDEN_COLS = ['client_descr']


@callback(
    Output('table_data_original', 'data'),
    Output('job_queue_name', 'data'),
    Output('job_queue_name', 'columns'),
    Output('job_queue_name', 'dropdown'),
    Output('job_queue_name', 'hidden_columns'),
    # State('job_queue_name', 'data'),
    Input('filter_dropdown', 'value'),
    Input('dropdown_clientdescr', 'value'),
    Input('days_ago', 'value'),
    Input('date-picker', 'date'),
    Input('get_review_table', 'n_clicks')

)
def get_table(filtered_status, client_descr, days_ago, date_picker, *args):

    # df = pd.DataFrame(conn.execute(text(query)))
    # filtered_status = 'SUCCESS'
    if days_ago == 'Today':
        days_ago_filter = 'DATEADD(day,-1,GETDATE())'
    elif days_ago == 'Yesterday':
        days_ago_filter = 'DATEADD(day,-2,GETDATE())'
    elif days_ago == 'Weekly':
        days_ago_filter = 'DATEADD(day, -7,GETDATE())'
    elif days_ago == 'Monthly':
        days_ago_filter = 'DATEADD(month, -1, GETDATE())'
    elif days_ago == 'Last Quarter':
        days_ago_filter = 'DATEADD(month, -3, GETDATE())'
    elif days_ago == 'Last 6 Months':
        days_ago_filter = 'DATEADD(month, -6, GETDATE())'
    elif days_ago == 'Last Year':
        days_ago_filter = ' DATEADD(month, -12, GETDATE())'
    else:
        days_ago_filter = 'DATEADD(month, -36, GETDATE())'

    query = f"""select queue_pickup_Date, status, cycle_id, cycle_desc, client_descr from is_etl.dbo.etl_job_queue
            where queue_pickup_date >=  {days_ago_filter}
            and status = '{filtered_status}'
            and client_descr ='{client_descr}'
            and update_date >= '{date_picker}'
            """
    print(query)
    df = pd.read_sql_query(query, conn)
    columns = [{
        'id': i,
        'name': i,
        'editable': True if i in EDITABLE_COLS else False,
        'hideable': False if i not in HIDDEN_COLS else True,
        'presentation': 'dropdown' if i == 'exclude_flag' else 'input'
    } for i in (df.columns)]

    data = df.to_dict('records')

    dropdowns = {
        'exclude_flag': {
            'options': [{'label': l, 'value': v} for l, v in [('YES', True), ('NO', False)]]
        }
    }

    return data, data, columns, dropdowns, HIDDEN_COLS


@callback(
    Output('table_data_original', 'data', allow_duplicate=True),
    Input('job_queue_name', 'data'),
    State('job_queue_name', 'data_previous'),
    State('job_queue_name', 'selected_rows'),
    prevent_initial_call=True
)
def update_table_data(data, previous_data,  *args):

    ctx = callback_context.triggered[0]['prop_id'].split('.')[0]

    if ctx == 'job_queue_name':
        if data != previous_data:
            with conn.cursor() as cursor:
                for row, previous_row in zip(data, previous_data):
                    id_value = row['cycle_id']
                    update_column_check1 = row['status']

                    if row['update_column_check1'] != previous_row['update_column_check1']:
                        update_query = f"""update is_etl.dbo.etl_job_queue
                                set status = %s where cycle_id = %s"""
                        cursor.execute(
                            update_query, (update_column_check1, id_value))
            conn.commit()
    return data
