#!/usr/bin/env python
# coding: utf-8

# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
csv_url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv'
spacex_df = pd.read_csv(csv_url)
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create dropdown options
dropdown_options = [{'label': 'All Sites', 'value': 'All Sites'}]
launch_sites = sorted(list(spacex_df['Launch Site'].unique()))
for site in launch_sites:
    dropdown_options.append({'label': site, 'value': site})


# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.H3("Select Launch Site:",
                                        style={'color': '#503D36'}),
                                dcc.Dropdown(
                                    id='site-dropdown',
                                    options=dropdown_options,
                                    value="All Sites",

                                    style={'width': '80%', 
                                           'padding': '3px',
                                           'font-size':'20px',
                                           },
                                    searchable=True,
                                           ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0', 10000: '10000'},
                                                value=[min_payload, max_payload],
                                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ]
                        )

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    # filtered_df = spacex_df
    if entered_site == 'All Sites':
        fig = px.pie(spacex_df, values='class', 
                     names='Launch Site', 
                     title='Total Successful Launches by Site')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        fig = px.pie(filtered_df, names='class', 
                     title=f'Launch Outcomes for Site {entered_site}')
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), 
               Input(component_id='payload-slider', component_property='value')])

def get_scatter_chart(entered_site, payload_range):
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
                            (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
    if entered_site == 'All Sites':
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                         color='Booster Version Category',
                         title='Correlation between Payload and Success for All Sites')
        return fig
    else:
        site_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.scatter(site_df, x='Payload Mass (kg)', y='class',
                         color='Booster Version Category',
                         title=f'Correlation between Payload and Success for Site {entered_site}')
        return fig



# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

# Now with the dashboard completed, you should be able to use it to analyze SpaceX launch data, and answer the following questions:

# Which site has the largest successful launches?
    # VAFB SLC-4E
# Which site has the highest launch success rate?
    # KSC LC-39A
# Which payload range(s) has the highest launch success rate?
    # 2000 - 4000 kg
# Which payload range(s) has the lowest launch success rate?
    # 6000 - 10000 kg
# Which F9 Booster version (v1.0, v1.1, FT, B4, B5, etc.) has the highest
# launch success rate?
    # FT and B5(which only has 1 launch)
