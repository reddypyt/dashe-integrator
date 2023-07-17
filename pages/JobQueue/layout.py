import dash_bootstrap_components as dbc
import dash_design_kit as ddk
from dash import dcc, html, register_page

from .callbacks import *
from datetime import datetime as dt
import pymssql
conn = pymssql.connect(server='10.20.20.5:1501', user='pythonaperityetl01',
                       password='21SbAjsYdt!', database='COLL_TRANS')

query_dropdown_client = f"""select distinct client_descr from is_etl.dbo.etl_job_queue"""
df = pd.read_sql_query(query_dropdown_client, conn)
options = [{'label': value, 'value': value} for value in df['client_descr']]

register_page(__name__, name='JOB Queue')

layout = html.Div([
    ddk.Card(width=100,  style={'text-align': 'center'}, children=[
        dbc.Row(children=[
            dbc.Col(width=1, children=[
                dcc.Dropdown(['SUCCESS', 'FAILED', 'TRIGGERED', 'FINISHED', 'PICKED UP', 'RUNNING', 'PICKED_UP',
                             'WAITING', 'CANCELLED'], 'SUCCESS', id='filter_dropdown', searchable=False, clearable=False),
                dbc.Alert(id="push_message", duration=4000, is_open=False)
            ]),
            dbc.Col(width=2, children=[
                dcc.Dropdown(['Today', 'Yesterday', 'Weekly', 'Last Month', 'Last Quarter', 'Last 6 Months', 'Last Year',
                             'Rest'], 'Weekly', id='days_ago', searchable=False, clearable=False),

            ]),
            dbc.Col(width=2, children=[
                dcc.Dropdown(id='dropdown_clientdescr', options=options,
                             value=options[0]['value'] if options else 'Trinchero'),
            ]),

            dbc.Col(width=1, children=[
                dcc.DatePickerSingle(
                    id='date-picker',
                    date=dt.today()
                )
            ]),
            dbc.Col(width=3, children=[
                html.Button(id='get_review_table', children='REFRESH',
                            style={'border-radius': '8px', 'margin': '8px 8px'})
            ])
        ]),
        dcc.Store(id='table_data_original', storage_type='session'),
        ddk.DataTable(
            id='job_queue_name',
            style_cell={'text-align': 'Center', 'text-transform': 'uppercase',
                        'height': 'auto', 'whiteSpace': 'normal'},
            css=[{
                "selector": ".Select-menu-outer",
                "rule": 'display : block !important'
            }],
        )
    ])
])
