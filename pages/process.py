import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app

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
		html.P(['I used the NSRDB developer API to collect training data in order to build my first baseline model. After view this dataset’s features I concluded there are enough features to create a baseline model but not enough for a deployable model.']),
		html.Img(src='assets/first_data.png', className='img-fluid')
	])

layout = dbc.Row([column1])