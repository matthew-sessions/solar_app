import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
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
        dcc.Markdown(
            """
        
            ## Value Proposition

            Emphasize how the app will benefit users. Don't emphasize the underlying technology.

            ✅ RUN is a running app that adapts to your fitness levels and designs personalized workouts to help you improve your running.

            ❌ RUN is the only intelligent running app that uses sophisticated deep neural net machine learning to make your run smarter because we believe in ML driven workouts.

            """
        ),
        dcc.Link(dbc.Button('Call To Action', color='primary'), href='/predictions')
    ],
    md=4,
)
loaded_model = load('assets/pipeline.joblib')
lat, lon = 1.999140,112.940784
features = ['zen', 'temperature', 'summary','pressure','visibility','uvIndex','dewPoint']
a = requests.get('https://api.darksky.net/forecast/dc757f87dbdcb50907cdcecf02328582/' + str(lat)+ ',' + str(lon) +'?extend=hourly')
a= a.json()
a = a['hourly']['data']

df = pd.DataFrame(a)

tr = df['time'].values

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

df['TIME'] = df.time.apply(tim)

zenith = []
for i in tr:
  zed = zen(i, lat, lon)
  zenith.append(zed)

df['zen'] = zenith

res = loaded_model.predict(df[features])
df['GHI Level'] = res

gapminder = df.head(24)
fig = px.line(gapminder, x="TIME", y="GHI Level", title='24 Hour GHI Level',height=300)

fig.update_layout(
    margin=dict(l=20, r=20, t=25, b=20)
)


location = pd.DataFrame([[1.999140,112.940784, 'Kapit, Malaysia']], columns=['lat','lon','City'])
fig2 = px.scatter_mapbox(location, lat="lat", lon="lon", hover_name="City",
                        color_discrete_sequence=["fuchsia"], zoom=3, height=300)
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
