import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px

from app import app

import dash_html_components as html

column1 = dbc.Container([ 
        html.Br([]),
        html.H4(['Notable Features']),
        html.Br([]),
        dbc.Row([dbc.Col([html.Br([]),html.Br([]),html.P(['Here are the top nine features used in my model. As you can see from the permutation importances, the Zenith angle is the most powerful predictor of the GHI. You can get an R² score above 0.75 by using only the zenith angle in your model. But if you want to account for days that would be considered outliers (days that are especially hot with clear skies, or days that are stormy/overcast) you will have to look at many more features.'])]),dbc.Col([html.Img(src='assets/feat.png', className='img-fluid',style={'textAlign':'center','margin':'auto'})])]),
        html.Br([]),
        html.Br([]),
        html.H4(['Data Exploration']),
        html.Br([]),        
        html.P(['This scatter plot allows you to visualize the relationship between the Zenith and the GHI. As the Zenith angle approaches 0° the GHI‌ level increases, and once the Zenith angle hits 90° the there is no detected GHI level (because there is no direct sun to emit radiation). However, there are many outliers where the Zenith angle is close to 0° but the GHI‌ level is relatively low.']),
        html.Br([]),
        html.Img(src='assets/scatter.png', className='img-fluid',style={'textAlign':'center','margin':'auto'}),   
        html.Br([]),
        html.Br([]),
        html.P(['The SHAP values of this model allow us to take a closer look at how the model finds outliers.  The two plots below are two separate days with Zenith angles under 10°. Day One has a Zenith angle of 9.8°, and Day Two has a Zenith angle of 8.1°. If the model was only looking at zenith angles then it would predict that Day Two has a higher GHI level than Day On. However, Day One has a GHI level of 930 and Day Two has a GHI level of 220. The model predicted both days correct within 20 GHI units. So what features caused the extreme difference?']),
        html.Br([]),
        html.Br([]),  
        html.Img(src='assets/shap1.png', className='img-fluid',style={'textAlign':'center','margin':'auto'}),
        html.Br([]),
        html.Br([]), 
        html.P(['It seems that Day One is what you would consider an ideal day for solar power. The sun is almost directly above this location, there is no chance of a storm, and it is a pretty hot day.']),        
        html.Br([]),
        html.Br([]),    
        html.Img(src='assets/shap2.png', className='img-fluid',style={'textAlign':'center','margin':'auto'}),
        html.Br([]),
        html.Br([]), 
        html.P(['Day two, on the other hand, has a very high likelihood of a storming, it is much colder, and there is more cloud coverage. From the SHAP values, you can see that the model really takes into account “precipProbability” or the likelihood it will storm.']),                                 
        html.Br([]),
        html.P(['To visualize the correlation between the Percentage Probability of a Storm and the GHI level, I isolated all observations that have Zenith angles between 20° and 5° and then plotted the “precipProbability” against “GHI”. The correlation is not incredibly apparent, but the relationship is somewhat linear. ']),
        html.Br([]),
        html.Br([]),    
        html.Img(src='assets/realscat.png', className='img-fluid',style={'textAlign':'center','margin':'auto'}),
        html.Br([]),
        html.Br([]), 
        html.Br([]),
        html.H4(['Feature Isolation']),
        html.Br([]),
        html.P(['In my opinion, one of the most useful plots for understanding the impact the Solar Zenith angle has on the GHI is the Parcial Dependancy Plot (PDP). According to this model, the Zenith angle has a consistent impact on the GHI level from 0° to 40° and then bottoms off once it hits 90°. This plot also shows there are many instances where from 0° to 90° the relationship is linear, but overall the relationship is slightly monotonic. ']),                   
        html.Br([]),
        html.Img(src='assets/pdp.png', className='img-fluid',style={'textAlign':'center','margin':'auto'}),
        html.Br([]), 
        html.Br([]),         
        html.Br([])
    ])


layout = dbc.Row([column1])