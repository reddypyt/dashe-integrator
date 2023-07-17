import dash_bootstrap_components as dbc
import dash_design_kit as ddk
from dash import dcc, html, register_page
import pandas as pd
from .callbacks import *
from datetime import datetime as dt
import pymssql
conn = pymssql.connect(server='10.20.20.5:1501', user='pythonaperityetl01',
                       password='21SbAjsYdt!', database='COLL_TRANS')

query_dropdown_provider = f"""select distinct provider_id as provider_id, application
                             from  coll_trans.dbo.vscr_daily_activity_l2"""
df = pd.read_sql_query(query_dropdown_provider, conn)
options_pro = [{'label': value, 'value': value} for value in df['provider_id']]
options_app = [{'label': value, 'value': value}
               for value in df['application'].drop_duplicates()]

register_page(__name__, name='Daily Activity L2')

layout = html.Div([
    ddk.Card(width=100,  style={'text-align': 'center'}, children=[
        dbc.Row(children=[

            dbc.Col(width=2, children=[
                dcc.Dropdown(id='dropdown_provider', options=options_pro,
                             placeholder='Select an Provider id'),
            ]),


            dbc.Col(width=2, children=[
                dcc.Dropdown(id='dropdown_application', options=options_app,
                             placeholder='Select an Application'),
            ]),

            dbc.Col(width=1, children=[
                dcc.DatePickerSingle(

                    id='date-picker-update',
                    # date=dt.today(),
                    placeholder='Search by Create Date'
                )
            ])
        ]),

        dcc.Store(id='daily_data_l2_original', storage_type='session'),
        ddk.DataTable(
            id='daily_process_l2_name',
            style_cell={'text-align': 'Center', 'text-transform': 'uppercase',
                        'height': 'auto', 'whiteSpace': 'normal'},
            css=[{
                "selector": ".Select-menu-outer",
                "rule": 'display : block !important'
            }],
        )

    ])
])
