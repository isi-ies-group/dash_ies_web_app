# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 20:18:04 2020

@author: GuillermoMatas
"""

import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_table
from dash.dependencies import Input, Output, State

from flask import request

from controls import MAGNITUDE_LABELS, MAGNITUDE_SYMBOLS
from controls import UNITS, VAR_CATEGORIES, DATATABLE_OPTION, HELP_BTN

import pandas as pd
from datetime import timedelta
import datetime as dt
import time
from concurrent.futures import ThreadPoolExecutor

import urllib.parse as urllib
import logging

import db_functions
import aux_functions

app = dash.Dash(__name__)

app.title = 'IES-UPM Dashboard'

server = app.server
app.config.suppress_callback_exceptions = True

PATH_DATOS = 'C:/Users/Helios/Documents/'
PATH_DATOS_FICHERO_METEO = PATH_DATOS + 'meteo.parquet'

logging.basicConfig(
    filename=PATH_DATOS + 'dash-app.log',
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger(__name__)

logger.info('Nueva sesión')

console = logging.StreamHandler()
console.setLevel(logging.INFO)

def carga_df_parquet():
    df_fichero = pd.read_parquet(PATH_DATOS_FICHERO_METEO)
    renombra_meteo = {'G(0)':'g_0', 'G(41)':'g_41', 'D(0)':'d_0', 'B':'b', 'Wvel':'w_vel', 'Wdir':'w_dir', 'Tamb':'helios_t_amb', 'Elev.Sol':'ele_sol', 'Orient.Sol':'ori_sol'}
    df_fichero = df_fichero.rename(columns=renombra_meteo).rename(columns=str.lower)
    # df_fichero = df_fichero.asfreq('1H')
    cols_mean = ['temp_air', 'rad_dir', 'g_0', 'd_0', 'top', 'mid', 'bot', 'cal_top', 'cal_mid', 'cal_bot', 'pres_aire', 'v_viento', 'd_viento', 'ele_sol', 'ori_sol', 'helios_t_amb', 'hr', 'b', 'g_41', 'gn', 'pirgeo', 'temp_pirgeo', 'w_vel', 'w_dir', ]
    cols_sum = ['lluvia', 'limpieza']
    df_mean = df_fichero[cols_mean].resample('1H').agg('mean')
    df_sum = df_fichero[cols_sum].resample('1H').agg('sum')
    
    return pd.concat([df_mean, df_sum], axis='columns')

df = carga_df_parquet()

def description_card():
    """

    :return: A Div containing dashboard title & descriptions.
    """
    return html.Div(
        id="description-card",
        children=[
            html.H5("IES Data Repository"),
            html.H3("Welcome to the IES - UPM Dashboard"),
            html.Div(
                id="intro",
                children="Explore solar data obtained from our sensors. Select the dates and the variables to be displayed.",
            ),
        ],
    )


def generate_control_card():
    """
    :return: A Div containing controls for graphs.
    """
    global df
    
    date_interval = db_functions.getTimeIntervalDB(df)

    return html.Div(
        id="control-card",
        children=[

            html.P("Select Time interval",  style={'display': 'inline-block'}),
            aux_functions.createHelpPopover('date', app.get_asset_url("help-logo.png")),            
            dcc.DatePickerRange(
                id="date-picker-select",
                className="dateRangePickerInput",
                display_format="YYYY-MM-DD",
                start_date=date_interval[1]-timedelta(days=7),
                end_date=date_interval[1],
                min_date_allowed=date_interval[0],
                max_date_allowed=date_interval[1]+timedelta(days=1),  # #Este día no se incluye
                initial_visible_month=date_interval[1],
                # #with_portal=True
            ),
            
            html.Br(),
            html.Br(),
            html.Br(),
            
            html.P("Select Variable to Plot", style={'display': 'inline-block'}),        
            aux_functions.createHelpPopover('graph_var', app.get_asset_url("help-logo.png")),
            dcc.Dropdown(
                id="variable-select",
                className='dropdown',
                options=[
                    {"label": str(MAGNITUDE_LABELS[magnitude]),
                     "value": str(magnitude)} for magnitude in MAGNITUDE_SYMBOLS
                ],
                multi=True,
                value=[],
                #value=list(VAR_CATEGORIES['irradiance'])[:4],
                clearable=False
            ),

            html.Br(),
            html.Br(),
            html.Br(),

            html.P("Select DataTable visibility options", style={'display': 'inline-block'}),
            aux_functions.createHelpPopover('datatable', app.get_asset_url("help-logo.png")), 
            dcc.Dropdown(
                id="datatable-select",
                className='dropdown',
                options=[
                    {"label": str(DATATABLE_OPTION[table_option]),
                     "value": str(table_option)} for table_option in DATATABLE_OPTION
                ],
                multi=False,
                value='none',
                clearable=False
            ),

            html.Br(),
            html.Br(),
            html.Br(),
            
            html.A(
                html.Button('Download Full DataSet', id='download_button', n_clicks=0),
                    id='download-link',
                    download="full_dataset.csv",
                    href="",
                    target="_blank"
            ),
            
            aux_functions.createHelpPopover('download', app.get_asset_url("help-logo.png")),
        ],
    )

def serve_layout():
    return html.Div(
    id="app-container",
    children=[
        # Banner
        html.Div(
            id="banner",
            className="banner",
            children=[html.Img(src=app.get_asset_url("ies_logo.png")),
                      html.H1("INSTITUTO DE ENERGÍA SOLAR")],
        ),
        # Left column
        html.Div(
            id="left-column",
            className="three columns",
            children=[description_card(),generate_control_card()]
            + [
                html.Div(
                    ["initial child"], id="output-clientside", style={"display": "none"}
                )
            ],
        ),
        # Right column
        dcc.Loading(
            id="loading-right-column",
            type="graph",
            
        ),
        html.Div(
                id="auto-generated-datatable",
                className="eleven columns",),
        
        
        html.Hr(),
    ])

@app.callback(
    Output("auto-generated-graphics", "children"),
    [
        Input("date-picker-select", "start_date"),
        Input("date-picker-select", "end_date"),
        Input("variable-select", "value"),
    ],
)
def generate_graphics(start_date, end_date, selected_var):    
    """
        :param: start_date: start date from selection.
        :param: end_date: end date from selection.
        :param: selected_var: variables from selection.
    
        :return: children Graphics.
    """
    logger.info(request.remote_addr)

    global df
    
    df_datos = db_functions.createDataFrameFromQuery(df, selected_var, [start_date, end_date])
    graph_cat = aux_functions.getGraphCategories(selected_var)
    
    fig_vector = []
    for category in graph_cat:
        fig_vector.append(aux_functions.createGraph(df_datos, selected_var, category, [start_date, end_date]))

    graph_components = []
    graph_count=1
    for fig in fig_vector:
        graph_components.append(dcc.Graph(
                                            id="cat-graph-"+str(graph_count),
                                            figure=fig
                                        )
                                )
        
        for i in range(3):
            graph_components.append(html.Br())

        graph_count += 1
     
    return html.Div(graph_components)

@app.callback(
    Output("auto-generated-datatable", "children"),
    [
        Input("date-picker-select", "start_date"),
        Input("date-picker-select", "end_date"),
        Input("variable-select", "value"),
        Input("datatable-select", "value")
    ],
)
def generate_datatable(start_date, end_date, selected_var, datatable_option):    
    """
        :param: start_date: start date from selection.
        :param: end_date: end date from selection.
        :param: selected_var: variables from selection.
        :param: reset: reset graphics if True.
    
        :return: children Graphics.
    """
    global df

    if datatable_option == "none":
        return []

    else:
        if datatable_option == "full_data":
            selected_var=list(MAGNITUDE_SYMBOLS.keys())
            df_datos = db_functions.createDataFrameFromQuery(df, selected_var, [start_date, end_date])
        else:
            df_datos = db_functions.createDataFrameFromQuery(df, selected_var, [start_date, end_date])
            
        # #Relleno de los valores nulos
        df_datos.fillna('NaN', inplace=True)
        return html.Div(dash_table.DataTable(
                    id='db_table',
                    style_cell={
                        'minHeight':'30px',
                        'height':'auto',
                        'minWidth': '130px',
                        'width':'auto',
                        'maxWidth': '150px',
                        'whiteSpace': 'normal',
                        'overflow': 'hidden',
                        'textOverflow': 'ellipsis',
                        },
                    style_header={
                        'backgroundColor': '#1867b7',
                        'color':'white',
                        'fontWeight': 'bold'
                        },
                    style_table={
                        'maxHeight': '1200px',
                        'maxWidth': '100%',
                        'overflowX': 'scroll', 
                        'border':'thin lightgrey solid'
                        },
                    fixed_rows={'headers': True, 'data': 0 },
                    #filter_action="native",
                    sort_action="native",
                    sort_mode="multi",
                    selected_columns=[],
                    selected_rows=[],
                    page_action="native",
                    columns=[{"name": MAGNITUDE_LABELS[i] + UNITS[i], "id": i} for i in df_datos.columns],
                    data=df_datos.to_dict('records'),
                ),
            )

@app.callback(
    dash.dependencies.Output('download-link', 'href'),
    [
        Input("date-picker-select", "start_date"),
        Input("date-picker-select", "end_date"),
        Input("download_button", "n_clicks"),
    ],)
def update_download_link(start_date, end_date, dwn_click):
    # Find which one has been triggered
    ctx = dash.callback_context

    global df

    if ctx.triggered:
        selected_var=list(MAGNITUDE_SYMBOLS.keys())
        df_datos = db_functions.createDataFrameFromQuery(df, selected_var, [start_date, end_date])
        # #Relleno de los valores nulos
        df_datos.fillna('NaN', inplace=True)
        csv_string = df_datos.to_csv(sep='\t', index=False, encoding='utf-8')
        csv_string = "data:text/csv;charset=utf-8," + urllib.quote(csv_string, encoding='utf-8')
        return csv_string

def toggle_popover(n, is_open):
    if n:
        return not is_open
    return is_open


for p in HELP_BTN.keys():
    app.callback(
        Output(f"popover-{p}", "is_open"),
        [Input(f"popover-{p}-target", "n_clicks")],
        [State(f"popover-{p}", "is_open")],
    )(toggle_popover)


@app.callback(
    Output("loading-right-column", "children"),
    [
        Input("date-picker-select", "start_date"),
        Input("date-picker-select", "end_date"),
        Input("variable-select", "value"),
        Input("datatable-select", "value")
    ],
)
def input_triggers_spinner(start_date, end_date, selected_var, table_option):
    return [html.Div(
                id="auto-generated-graphics",
                className="nine columns"),
            html.Br(),
            html.Br(),
            ]

# https://community.plotly.com/t/solved-updating-server-side-app-data-on-a-schedule/6612/15
def refresh_data_every():
    while True:
        if dt.datetime.now().time().hour == 8:
            refresh_data()
            logger.info('DF recargado')
        time.sleep(3600) # reload interval in seconds (1h)

def refresh_data():
    global df
    ### some expensive computation function to update dataframe
    df = carga_df_parquet()

executor = ThreadPoolExecutor(max_workers=1)
executor.submit(refresh_data_every)

app.layout = serve_layout

if __name__ == '__main__':
    app.run_server(port=4050)
