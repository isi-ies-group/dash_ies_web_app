# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 00:30:16 2020

@author: GuillermoMatas
"""

import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_table
from dash.dependencies import Input, Output, State

import plotly.graph_objects as go

from controls import VAR_CATEGORIES, MAGNITUDE_SYMBOLS 
from controls import MAGNITUDE_LABELS, UNITS, HELP_BTN
import db_functions

import math
import numpy as np
import pandas as pd


def getGraphCategories(selected_var):
    iter_dict = VAR_CATEGORIES.copy()
    graph_categories = []
    for element in selected_var:
        for category in iter_dict:
            if element in iter_dict[category]:
                iter_dict.pop(category)
                graph_categories.append(category)
                break

    return graph_categories

def createGraph(df, selected_var, category, dates):
    graph_var=[]
    for element in selected_var:
        if element in VAR_CATEGORIES[category]:
            graph_var.append(str(element))
    
    fig=go.Figure()
    
    if category == "wind direction":
        
        n_bins=12
        graph_df=pd.DataFrame()
        
        for wind_dir_var in graph_var:
            for wind_speed_var in VAR_CATEGORIES["wind speed"]:
                if (wind_dir_var[2:] in wind_speed_var) or (wind_dir_var[:2] in wind_speed_var):
                    
                    # #Creación de un dataframe que contiene los datos 
                    # #de velocidad de viento asociado a su dirección
                    aux_df=db_functions.createDataFrameFromQuery(df, [wind_speed_var],dates)
                    graph_df[wind_speed_var]=aux_df[wind_speed_var].copy()
                    graph_df[wind_dir_var]=df[wind_dir_var].copy()
        
                    if UNITS[wind_dir_var] == '(rad)':
                        for i in range(1,len(graph_df[wind_dir_var])):
                            graph_df[wind_dir_var][i] = graph_df[wind_dir_var][i]*(360/2*math.pi)
                    
                    # #Agrupación de los datos de velocidad de viento 
                    # #en bins en función de la dirección
                    bins = pd.cut(graph_df[wind_dir_var],list(np.linspace(0,360,n_bins+1)))
                    # #Cálculo de la frecuencia relativa y 
                    # #velocidad media del viento en función de la dirección
                    plot_df = graph_df.groupby(bins)[wind_speed_var].agg(['count','mean'])
                    plot_df['count'] /= plot_df['count'].sum()
                    
                    # #Representación de una magnitud ficticia representativa
                    # #con 
                    # #fórmula=velocidad media en la dir*frecuencia en la dir
                    plot_df['y_trace'] = plot_df['count'] * plot_df['mean']
                    
                    # ------
            
            fig.add_trace(go.Barpolar(r=plot_df['y_trace'],
                                     name=MAGNITUDE_SYMBOLS[wind_dir_var],
                                     #mode='markers'
                                     )
                          )
 
        fig.update_layout(
        title="IES - UPM: "+ category.capitalize(),
        #polar_radialaxis_range=[0, plot_df['y_trace']],
        showlegend=True
        )            
            
    else:
        for y_trace in graph_var:
            
            fig.add_trace(go.Scatter(x=df.index, 
                                     y=df[y_trace],
                                     name=MAGNITUDE_SYMBOLS[y_trace],
                                     mode='lines'
                                     )
                          )
    
        fig.update_layout(
        title="IES - UPM: "+ category.capitalize(),
        xaxis_title=MAGNITUDE_LABELS['measure_utc_dt'],
        showlegend=True
        )
    
    return fig


def createHelpPopover(identifier_key, img_src):
    return html.Div(
        [
        dbc.Button(
            id="popover-{}-target".format(identifier_key), 
            color="blue",
            className='help-button',
            children=[html.Img(src=img_src)],
        ),
        dbc.Popover(
            [
                dbc.PopoverHeader(HELP_BTN[identifier_key]['header']),
                dbc.PopoverBody(HELP_BTN[identifier_key]['body'], style={'whiteSpace': 'pre-wrap'}),
            ],
            id="popover-{}".format(identifier_key),
            is_open=False,
            target="popover-{}-target".format(identifier_key),
        ),
    ],
    style={'display': 'inline-block'},
    className="help-button"
    
)
    
    