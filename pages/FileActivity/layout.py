import dash_bootstrap_components as dbc
import dash_design_kit as ddk
from dash import dcc, html, register_page
import pandas as pd
from .callbacks import *
from datetime import datetime as dt
import pymssql
conn = pymssql.connect(server='10.20.20.5:1501', user='pythonaperityetl01',
                       password='21SbAjsYdt!', database='COLL_TRANS')

query_dropdown_provider = f"""select distinct provider_id from  coll_trans.dbo.vscr_cy_file_process"""
df = pd.read_sql_query(query_dropdown_provider, conn)
options = [{'label': value, 'value': value} for value in df['provider_id']]

register_page(__name__, name='File Activity')

layout = html.Div([
    ddk.Card(width=100,  style={'text-align': 'center'}, children=[
        dbc.Row(children=[
            dbc.Col(width=2, children=[
                dcc.Input(id='search_filekey', type='text',
                          placeholder='Search by File Key'),

            ]),

            dbc.Col(width=2, children=[
                dcc.Dropdown(['Cleansed', 'Cleansing Error', 'Failed', 'Hold', 'Imported', 'New', 'PUSHED TO CLIENT', 'Re-cleanse', 'Restated'],
                             id='cy_descr_dropdown', placeholder='Select an Cycle status', searchable=False, clearable=False),

            ]),

            dbc.Col(width=2, children=[
                dcc.Dropdown(id='dropdown_provider', options=options,
                             placeholder='Select an Provider id'),
            ]),

            dbc.Col(width=1, children=[
                dcc.DatePickerSingle(

                    id='date-picker-update',
                    # date=dt.today(),
                    placeholder='Search by  Update Date'
                )
            ]),
            dbc.Col(width=2, children=[
                dcc.DatePickerSingle(

                    id='date-picker-create',
                    # date=dt.today(),
                    placeholder='Search by  Create Date'
                )
            ]),
            dbc.Col(width=2, children=[
                html.Button(id='get_review_table', children='REFRESH',
                            style={'border-radius': '8px', 'margin': '8px 8px'})
            ])
        ]),
        dcc.Store(id='file_data_original', storage_type='session'),
        ddk.DataTable(
            id='file_process_name',
            style_cell={'text-align': 'Center', 'text-transform': 'uppercase',
                        'height': 'auto', 'whiteSpace': 'normal'},
            row_selectable='single',
            selected_row_ids=[],
            css=[{
                "selector": ".Select-menu-outer",
                "rule": 'display : block !important'
            }],
        ),
        dbc.Modal(
            id='log_modal',
            is_open=False,
            size='md',
            children=[
                dbc.ModalHeader("Selected Row"),
                dbc.ModalBody([
                    html.H5("Data from Query:"),
                    html.Div(id='modal-content')
                ]),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close-modal", className="ml-auto")
                ),
            ]
        )

    ])
])
