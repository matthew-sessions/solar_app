import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px

from app import app

import dash_html_components as html


column2 = dbc.Row([
    dcc.Input(id='input-1-state', type='number', placeholder='Latitude'),
    dcc.Input(id='input-2-state', type='number', placeholder='Longitude'),
    html.Button(id='submit-button', n_clicks=0, children='Predict'),
     ])
col3 = dbc.Row([
    html.Div(id='output-state')])


@app.callback(Output('output-state', 'children'),
              [Input('submit-button', 'n_clicks')],
              [State('input-1-state', 'value'),
               State('input-2-state', 'value')])
def update_output(n_clicks, input1, input2):
    df = pd.DataFrame([[input1,input2]],columns=['x','y'])
    fig2 = px.scatter_mapbox(df, lat="x", lon="y", 
                            color_discrete_sequence=["fuchsia"], zoom=3,height=450)
    fig2.update_layout(
        mapbox_style="white-bg",
        mapbox_layers=[
            {
                "below": 'traces',
                "sourcetype": "raster",
                "source": [
                    "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
                ]
            }
          ])

    fig2.update_layout(margin={"r":0,"t":25,"l":0,"b":0}) 
    coll = dbc.Col(
        [
            dcc.Graph(figure=fig2)

        ]
    )     
    return(coll)


layout = dbc.Row([column2])
layout2 = dbc.Row([col3])