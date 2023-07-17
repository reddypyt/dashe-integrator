import time
from datetime import datetime
import dash_html_components as html
# import dash_enterprise_auth as auth
import pandas as pd
import dash_dangerously_set_inner_html
import plotly.express as px
from dash import Input, Output, State, callback, callback_context, clientside_callback, no_update
from sqlalchemy import text
from dash.exceptions import PreventUpdate
from utils.db import get_pg_connection
import pymssql
conn = pymssql.connect(server='10.20.20.5:1501', user='pythonaperityetl01',
                       password='21SbAjsYdt!', database='COLL_TRANS')


EDITABLE_COLS = []
HIDDEN_COLS = ['days_ago']


@callback(
    Output('daily_data_original', 'data'),
    Output('daily_process_name', 'data'),
    Output('daily_process_name', 'columns'),
    Output('daily_process_name', 'dropdown'),
    Output('daily_process_name', 'hidden_columns'),
    # State('job_queue_name', 'data'),
    Input('days_ago', 'value'),

    Input('dropdown_provider', 'value'),
    Input('dropdown_application', 'value'),

    Input('get_review_table', 'n_clicks')

)
def get_table(days_ago, provider_id, application, *args):

    # df = pd.DataFrame(conn.execute(text(query)))
    # filtered_status = 'SUCCESS'

    query_daily = f"""
            select application,concat(provider_id, '-(', provider_descr ,')') as provider,
            create_date as "Create date",total_files as "Total Files", pushed_to_client as "Pushed to Client",
            ready_to_push as "Ready to Push", failed_load as "Failed Load", failed_transform as "Failed Transform",
            on_hold as "On Hold", to_ingest as "To Ingest", to_transform as "To Transform",failed, pending, failed_push as "Failed Push",
            days_ago 
            from coll_trans.dbo.vscr_daily_activity_l1
            where 1 = 1
            """
    if days_ago:
        query_daily += f""" AND days_ago_label = '{days_ago}'"""
    if provider_id:
        query_daily += f""" AND provider_id = substring('{provider_id}',1,3)"""

    if application:
        query_daily += f""" AND application = '{application}'"""

    print(query_daily)
    df = pd.read_sql_query(query_daily, conn)
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


clientside_callback(
    """
        function navigatePage(selected_rows) {
            console.log(selected_rows);
            window.location.href=`/dailyactivityl2/layout`;
        }
    """,
    Output('page-content', 'children'),
    Input('daily_process_name', 'selected_rows'),
    prevent_initial_call=True
)
