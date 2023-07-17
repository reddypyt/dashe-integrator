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


EDITABLE_COLS = ['']
HIDDEN_COLS = ['UNIQUEPK']


@callback(
    Output('daily_data_l2_original', 'data'),
    Output('daily_process_l2_name', 'data'),
    Output('daily_process_l2_name', 'columns'),
    Output('daily_process_l2_name', 'dropdown'),
    Output('daily_process_l2_name', 'hidden_columns'),
    # State('job_queue_name', 'data'),
    Input('dropdown_provider', 'value'),
    Input('dropdown_application', 'value'),

    Input('date-picker-update', 'date')
)
def get_table(provider_id, application, date_picker, *args):

    # df = pd.DataFrame(conn.execute(text(query)))
    # filtered_status = 'SUCCESS'

    query_daily_l2 = f"""
            select application,component_descr,provider_id,total_files as "Total Files",pushed_to_client as "Pushed To Client",
            files_in_process as "Files In Process",ready_to_push as "Ready to Push",failed_load as "Failed Load",failed_transform as "Failed Transform",
            on_hold as "On Hold", to_ingest as "To Ingest", to_transform as "To Transform",failed as "Failed", pending as "Pending", failed_push as "Failed Push"
            from coll_trans.dbo.vscr_daily_activity_l2
            where 1 = 1
            """
    if provider_id:
        query_daily_l2 += f""" AND provider_id = '{provider_id}'"""
    if application:
        query_daily_l2 += f""" AND application = '{application}'"""

    if date_picker:
        query_daily_l2 += f""" AND create_date = '{date_picker}'"""

    print(query_daily_l2)
    df = pd.read_sql_query(query_daily_l2, conn)
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
