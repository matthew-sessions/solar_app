import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd

from app import app

import dash_html_components as html
import plotly.graph_objects as go

import requests
from pysolar.solar import *
import plotly.express as px
from joblib import load
import pandas as pd





column2 = html.Div([
    html.Div([
    html.H3('Blobal Horizontal Irradiance (GHI) Predictor'),
    html.P('Enter the Latitude & Longitude of any location to view the GHI level predictions'),
    dcc.Input(id='input-1-state', type='number', value=47.600237,placeholder="Latitude", style={'marginRight':7}),
    dcc.Input(id='input-2-state', type='number', value=-121.886079,placeholder="Longitude", style={'marginRight':7,'marginTop':7}),
    html.Div(html.Button(id='submit-button', n_clicks=0, children='Predict'),style={'marginTop':10,'textAlign': 'center'}),
     ], style={'marginRight':7,'marginLeft':7, 'textAlign':'center','marginTop':50}),
    html.Hr(style={'border-width':2,'color':'grey'})
    ],style={'margin':'auto','width':600,'height':250})


col3 = dbc.Row([
    html.Div(id='output-state')])


@app.callback(Output('output-state', 'children'),
              [Input('submit-button', 'n_clicks')],
              [State('input-1-state', 'value'),
               State('input-2-state', 'value')])
def update_output(n_clicks, input1, input2):
    lat = input1
    lon = input2
    loaded_model = load('assets/pipeline.joblib')
    features = ['zen', 'temperature', 'summary','pressure','visibility','uvIndex','dewPoint']

    def zen(time,lat,lon):
      from datetime import datetime
      mix = datetime.fromtimestamp(time).strftime('%Y,%m,%d,%H')
      spt = mix.split(',')
      import datetime
      date = datetime.datetime(int(spt[0]), int(spt[1]), int(spt[2]), int(spt[3]), 0, tzinfo=datetime.timezone.utc)
      return(float(90) - get_altitude(lat, lon, date))

    def tim(time):
      from datetime import datetime
      mix = datetime.fromtimestamp(time).strftime('%Y,%m,%d,%H')
      mixx = mix.split(',')
      return(str(mixx[3]) + ':00')


    a = requests.get('https://api.darksky.net/forecast/dc757f87dbdcb50907cdcecf02328582/' + str(lat)+ ',' + str(lon) +'?extend=hourly')
    a= a.json()
    location = a['timezone']
    aa = a['hourly']['data']
    data = pd.DataFrame(aa)
    data = data.head(24)
    data['lat'] = [lat] * len(data)
    data['lon'] = [lon] * len(data)
    data['Location'] = [a['timezone']] * len(data)
    df = data

    #Get the data for current GHI level
    dic = a['currently']

    current = pd.DataFrame([dic.values()], columns=dic.keys())
    current['lat'] = lat
    current['lon'] = lon

    location = a['timezone'] 
    current['Location'] = a['timezone']
    zenith2 = []
    for i in current[['time','lat','lon']].values:
      zenith2.append(zen(int(i[0]),i[1],i[2]))
    current['zen'] = zenith2
    current.zen

    currentghi = loaded_model.predict(current[features])
    current['Current GHI Level'] = currentghi


    #Get projected GHI for the next 24 hours

    zenith2 = []
    for i in current[['time','lat','lon']].values:
      zenith2.append(zen(int(i[0]),i[1],i[2]))
    current['zen'] = zenith2
    current.zen

    df['TIME'] = df.time.apply(tim)

    zenith = []
    for i in df[['time','lat','lon']].values:
      zenith.append(zen(int(i[0]),i[1],i[2]))

    df['zen'] = zenith

    res = loaded_model.predict(df[features])
    df['GHI Level'] = res


    try: df
    except NameError: df = pd.DataFrame([['0',0,'Enter Longitude & Latitude to see data']],columns=['TIME','GHI Level','Location'])

    fig = px.line(df, x="TIME", y="GHI Level", title='24 Hour GHI Level',color='Location')
    fig.update_layout(showlegend=False)


    try: current
    except NameError: current = pd.DataFrame([[0,'No current location',None,None]],columns=['Current GHI Level','Location','lat',"lon"])


    fig2 = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]}, 
        value = float(current['Current GHI Level']), 
        mode = "gauge+number+delta",
        title = {'text': "Current GHI level in " + str(current['Location'].values[0])},
        delta = {'reference': 450}, 
        gauge = {'axis': {'range': [None, 1200]},
                 'bar': {'color':'darkblue'},
                 'steps' : [
                     {'range': [0, 250], 'color': "lightgray"}, 
                     {'range': [600, 900], 'color': "gray"}], 
                 'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 1100}}))


    fig3 = px.scatter_mapbox(current, lat="lat", lon="lon", hover_name='Location',hover_data=['Current GHI Level'], zoom=3)
    fig3.update_layout(
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




    #fig3.update_layout(margin={"r":0,"t":25,"l":0,"b":0}) 

    coll = dbc.Col(
        [
            dcc.Graph(figure=fig2),dcc.Graph(figure=fig),dcc.Graph(figure=fig3)

        ]
    )

    return(coll)


layout = dbc.Row([column2])
layout2 = dbc.Row([col3])