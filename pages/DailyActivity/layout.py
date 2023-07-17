import dash_bootstrap_components as dbc
import dash_design_kit as ddk
from dash import dcc, html, register_page
import pandas as pd
from .callbacks import *
from datetime import datetime as dt
import pymssql
conn = pymssql.connect(server='10.20.20.5:1501', user='pythonaperityetl01',
                       password='21SbAjsYdt!', database='COLL_TRANS')

query_dropdown_provider = f"""select distinct concat(provider_id,'-(',provider_descr,')') as provider_id, application
                             from  coll_trans.dbo.vscr_daily_activity_l1"""
df = pd.read_sql_query(query_dropdown_provider, conn)
options_pro = [{'label': value, 'value': value} for value in df['provider_id']]
options_app = [{'label': value, 'value': value}
               for value in df['application'].drop_duplicates()]

register_page(__name__, name='Daily Activity')

layout = html.Div([
    ddk.Card(width=100,  style={'text-align': 'center'}, children=[
        dbc.Row(children=[

            dbc.Col(width=2, children=[
                dcc.Dropdown(['Today', 'Yesterday', 'Weekly', 'Last Month', 'Last Quarter', 'Last 6 Months', 'Last Year',
                             'Rest'], 'Weekly', id='days_ago', searchable=False, clearable=False),

            ]),

            dbc.Col(width=2, children=[
                dcc.Dropdown(id='dropdown_provider', options=options_pro,
                             placeholder='Select an Provider id'),
            ]),


            dbc.Col(width=2, children=[
                dcc.Dropdown(id='dropdown_application', options=options_app,
                             placeholder='Select an Application'),
            ]),


            dbc.Col(width=2, children=[
                html.Button(id='get_review_table', children='REFRESH',
                            style={'border-radius': '8px', 'margin': '8px 8px'})
            ])
        ]),
        dcc.Store(id='daily_data_original', storage_type='session'),
        ddk.DataTable(
            id='daily_process_name',
            row_selectable='single',
            selected_row_ids=[],
            style_cell={'text-align': 'Center', 'text-transform': 'uppercase',
                        'height': 'auto', 'whiteSpace': 'normal'},
            # style_as_list_view=True,
            css=[{
                "selector": ".Select-menu-outer",
                "rule": 'display : block !important'
            }],
        ),
        html.Div(id='page-content')
    ])
])
