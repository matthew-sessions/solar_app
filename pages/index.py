import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px

from app import app


import requests
from pysolar.solar import *
import plotly.express as px
from joblib import load
import pandas as pd

"""
https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout

Layout in Bootstrap is controlled using the grid system. The Bootstrap grid has 
twelve columns.

There are three main layout components in dash-bootstrap-components: Container, 
Row, and Col.

The layout of your app should be built as a series of rows of columns.

We set md=4 indicating that on a 'medium' sized or larger screen each column 
should take up a third of the width. Since we don't specify behaviour on 
smaller size screens Bootstrap will allow the rows to wrap so as not to squash 
the content.
"""

column1 = dbc.Col(
    [
        html.Br([]),
        html.H4(["Solar Irradiance Predictions"]),
        html.Br([]),
        html.P(['There are many small communities in Southeast Asia that do not have access to grid power. Solar energy is a valid alternative for these communities, however, due to technological and logistic hurdles, solar technology has yet to be implemented at scale.']),
        html.P(['This application forecasts the Global Horizontal Irradiance levels (GHI)‌ for four specific villages in Malaysia and Indonesia that could potentially transition to solar energy. ']),
        html.P(['Click create “Create Forcast” below to see the GHI‌ forcast of any given location around the Globe!']),
        dcc.Link(dbc.Button('Create Forcast', color='primary'), href='/predictions',style={'margin':'auto','textAlign': 'center'}),
        html.Br([])
    ],
    md=4,
)
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

df = pd.DataFrame()

aa =[[1.916045,113.130924, 'Kapit, Sarawak'],[6.177620,116.975330,'Beluran, Sabah'],[-1.288079, 131.249800,'Salawati, Indonesia'],[4.809317, 103.145713,'Jerangou Terengganu']]

for lat,lon, loc in aa:
  a = requests.get('https://api.darksky.net/forecast/322da9f437b1767029b90e4aa3da5a07/' + str(lat)+ ',' + str(lon) +'?extend=hourly')
  a= a.json()
  di = a['currently']
  aa = a['hourly']['data']
  data = pd.DataFrame(aa)
  data = data.head(24)
  data['lat'] = [lat] * len(data)
  data['lon'] = [lon] * len(data)
  data['Location'] = [loc] * len(data)
  df = df.append(data, ignore_index=True)


df['TIME'] = df.time.apply(tim)


zenith = []
for i in df[['time','lat','lon']].values:
  zenith.append(zen(int(i[0]),i[1],i[2]))

 
  
df['zen'] = zenith

res = loaded_model.predict(df[features])
df['GHI Level'] = res


df['GHI Level'] = res
fig = px.line(df, x="TIME", y="GHI Level", title='24 Hour GHI Level',height=300,color='Location')
fig.update_layout(showlegend=False)
fig.update_layout(
    margin=dict(l=20, r=20, t=65, b=40)
)


fig2 = px.scatter_mapbox(df, lat="lat", lon="lon", hover_name="Location",
                        color_discrete_sequence=["fuchsia"], zoom=3,height=300)
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

fig2.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
column2 = dbc.Col(
    [
        dcc.Graph(figure=fig),dcc.Graph(figure=fig2)

    ]
)

layout = dbc.Row([column1, column2])
