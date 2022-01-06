# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv(r'C:\Users\xiaow\Downloads\spacex_launch_dash.csv')
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1 ('SpaceX Launch Records Dashboard',
                                         style = {'textAlign' : 'center',
                                                  'color' : '#503D36',
                                                  'font-size' : 40}),
                                dcc.Dropdown(id = 'site-dropdown',
                                             options = [{'label': 'All Sites', 'value': 'All'},
                                            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}],
                                             value = 'All',
                                             placeholder='Select a Launch Site here',
                                             searchable=True),
                                html.Br(),

                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P('Payload range (Kg):'),
                                dcc.RangeSlider(id = 'payload-slider',
                                                min = 0, max = 10000, step = 1000,
                                                marks = {0: '0',
                                                         1000: '1000',
                                                         2000: '2000',
                                                         3000: '3000',
                                                         4000: '4000',
                                                         5000: '5000',
                                                         6000: '6000',
                                                         7000: '7000',
                                                         8000: '8000',
                                                         9000: '9000',
                                                         10000: '10000'},
                                                allowCross=False,
                                                value = [min_payload, max_payload]),
                                html.Br(),

                                html.Div(dcc.Graph(id = 'success-payload-scatter-chart'))
                                ])

@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)

def get_pie_chart(site_dropdown):
    filtered_df = spacex_df
    if site_dropdown == 'All':
        fig = px.pie(filtered_df, values = 'class',
                     names = 'Launch Site',
                     title = 'Total Launches for All Sites')
        return fig
    else:
        specific_df = spacex_df[spacex_df['Launch Site']==site_dropdown]
        specific_df = specific_df.groupby(['Launch Site', 'class']).size().reset_index(name = 'class count')
        title = f'Success count for {site_dropdown}'
        fig = px.pie(specific_df, names = 'class', values = 'class count', title = title)
        return fig

@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)

def update_scatter(site_dropdown, payload_slider):
    if site_dropdown == 'All':
        low, high = payload_slider
        df = spacex_df
        mask = (df['Payload Mass (kg)'] > low) & (df['Payload Mass (kg)'] < high)
        fig = px.scatter(df[mask],
                         x = 'Payload Mass (kg)',
                         y = 'class',
                         color = 'Booster Version',
                         size = 'Payload Mass (kg)',
                         hover_data = ['Payload Mass (kg)'],
                         title = 'Correlation between Payload and Success for all Sites')
    else:
        low, high = payload_slider
        df = spacex_df.loc[spacex_df['Launch Site'] == site_dropdown]
        mask = (df['Payload Mass (kg)'] > low) & (df['Payload Mass (kg)'] < high)
        fig = px.scatter(
            df[mask],
            x = 'Payload Mass (kg)',
            y = 'class',
            color = 'Booster Version',
            size = 'Payload Mass (kg)',
            hover_data = ['Payload Mass (kg)']
        )
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()