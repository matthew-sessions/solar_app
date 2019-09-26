import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
import pandas as pd 
import plotly.express as px

df = pd.DataFrame([[13.444304,144.793732,'Guam'],[20.716179,-158.214676,'Hawaii'],[18.200178, -66.664513,'Puerto Rico'],[15.183333, 145.750000,'Northern Mariana Islands'],[18.3434415, -64.8671634,'US Virgin Islands'],[-14.275632, -170.702042,'American Samoa']],columns=['lat','lon','location'])

fig = px.scatter_mapbox(df, lat="lat", lon="lon", hover_name="location",
                        color_discrete_sequence=["fuchsia"], zoom=1, height=400)
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

column1 = dbc.Container([ 
		html.Br([]),
		html.H4(['Project Inspiration']),
		html.Br([]),
		html.P(['I spent over two years in Southeast Asia doing humanitarian work. During my time there I visited many small villages deep in the island of Borneo. I saw community houses, convenient stores, and even schools that were totally off the grid. They used gas-powered generators to power their homes and schools. This method of energy generation is limited and expensive; they could only afford to leave the generator running for 6-7 hours a day. I was told that many families spend close to 25% of their monthly income on this inconvenient sorce of power. After hearing this I began to tinker with the idea of bringing solar energy to these villages. ']),
		html.P(['Once I finished as a volunteer I relocated to Shenzhen, China and started a career in Digital Marketing and Product Research. Residing in the manufacturing hub of the world, I met a handful of expats that were partners of factories that produced Solar Panels, Converters, and Batteries. I learned about this industry and have discussed potential ways rural communities could convert to solar.']),
		html.Br([]),
		html.H4(['Data Collection']),
		html.Br([]),
		html.P(['To my surprise, there is a limited amount of publicly available solar data in Southeast Asia. I spent hours trying to find historical Solar Irration data for various regions throughout Asia. I‌ ended up finding the National Solar Radiation Database (NSRDB). This Database contains various weather features along with the corresponding GHI for the United States and US Territories around the globe.']),
		dcc.Link('NSRDB Site', href='https://nsrdb.nrel.gov/'),
		html.Br([]),
		html.P(['I used the NSRDB developer API to collect training data in order to build my first baseline model. After viewing this dataset’s features I concluded there are enough features to create a baseline model but not enough for a deployable model.']),
		html.Img(src='assets/first_data.png', className='img-fluid'),
		html.Br([]),
		html.Br([]),
		html.P(['I‌ collected over 300,000 observations from six US Territories and States with a climate similar to Malaysia. ']),
		html.Br([]),
		html.Div([dcc.Graph(figure=fig)]),
		html.Br([]),
		html.H4(['Baseline Model']),
		html.Br([]),	
		html.P(['After collecting all this data, I created multiple models using XGBooster, Random Forest, Mulitple Regression, Logistic Regression, and a Decision Tree Regressor. I then tested all these models on Locations that were not in my training data. The best performing model was a Random Forest Regressor with an R² score of 0.859 and a Mean Absolute Error of 60. I used this model as my Baseline with the goal to improve the R² by adding more features from other datasets. ']),
		html.Br([]),
		html.Img(src='assets/rsqr.png', className='img-fluid',style={'textAlign':'center','margin':'auto'}),
		html.Br([]),
		html.H4(['Improving & Automating My Model']),
		html.P(['The goal of this project is to have continual forecast projections of my model. This means I ultimately needed to write a script that pulls in up-to-date data, wrangles/clean the data, make the predictions and then display it to the user. ']),
		html.P(['With this goal in mind, I searched for a weather API‌ that had the same features as my original dataset and more. I discovered the Darksky API has all the features I needed and more.']),
		html.P(['I pulled in data from the Darksky API with the same locations as my original dataset. I then merged the two datasets on the “Time” column. This took my dataset from having six solid features to having more than 15 features. After merging the data I was able to create a model that took in features from the Darksky API with the GHI target from the NSRDB dataset.  ']),
		html.P(['I‌ then created my final model with this new dataset and got great results. My R² score increased to 0.91 and my Mean Absolute Error decreased to 56.8. I tested this model on data from various locations and consistently received nealy identical scores.']),
		html.Br([]),
		html.Img(src='assets/finalmod.png', className='img-fluid',style={'textAlign':'center','margin':'auto'}),
		html.Br([]),
		html.H4(['Web Deployment']),
		html.Br([]),
		html.P(['Deploying the model as a web app was fairly difficult due to the fact that I did not have preset data. My app is meant to dynamically pull in data from an API which means that the data must be cleaned before entering the predictive model. Also the most predictive feature in my model the “Zenith Angle” is not included in the Darksky API. This is okay due to the fact that the Zenith angle is derived from the Longitude, Latitude, and the time of day (Information that I have). So I built a function that calculated the Zenith angle and added it as a new feature to my dataset.']),				
		html.Br([]),
		html.Img(src='assets/zen.png', className='img-fluid',style={'textAlign':'center','margin':'auto'}),
		html.Br([]),
		html.P(['After a few hours of debugging a script that pulls in data, cleans the data, calculates the Zenith angle, applies the model, and displays the predictions; I deployed it as an interactive web app using Plotly & Dash']),
		html.P(['Thanks for reading about my project! You can discover more insights about this project by clicking the link below!']),
		dcc.Link('View Insights', href='/insights'),
		html.Br([]),	
		html.Br([]),
		html.Br([])					

	])

layout = dbc.Row([column1])