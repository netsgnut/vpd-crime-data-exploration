from dash import Dash, html, Input, Output
from dash.dcc import Dropdown, Graph, RangeSlider
from dash_bootstrap_components import themes, Container, Row, Col, Label, Tab, Tabs
import numpy as np
import os
import pandas as pd
import plotly.express as px

# Retrieve dataset
df = pd.read_csv("../data/processed/crimedata_aggregated.csv")
print(f"Loaded aggregated dataset, {df.shape[0]} rows read")

# Read in data from the dataset
year_min, year_max = df["year"].min(), df["year"].max()
neighbourhoods = df["neighbourhood"].unique()
types = df["type"].unique()

# Prepare some other constants, too!
app_title = f'Crime Statistics for Vancouver, BC ({year_min} - {year_max})'

# Setup Dash
app = Dash(external_stylesheets=[themes.LUMEN], title=app_title)

# Server (for gunicorn)
server = app.server

# main layout
app.layout = Container(
    [
        html.Header(
            [
                Container(
                    html.H3(app_title),
                    className='container d-flex flex-wrap justify-content-center'
                )
            ],
            className='py-3 mb-4 border-bottom'
        ),
        Row(
            [
                Col(
                    [
                        Label('Years', html_for='year'),
                        RangeSlider(
                            id='years',
                            min=year_min,
                            max=year_max,
                            value=[
                                year_min,
                                year_max
                            ],
                            marks={
                                f'{year_min}': f'{year_min}',
                                f'{year_max}': f'{year_max}'
                            },
                            allowCross=False,
                            tooltip={'placement': 'bottom',
                                     'always_visible': True},
                            step=1
                        ),
                        html.Hr(),
                        Label('Offence Types', html_for='types'),
                        Dropdown(
                            id='types',
                            options=[{'label': n, 'value': n}
                                     for n in np.sort(types)],
                            value=[
                                'Homicide',
                                'Offence Against a Person',
                                'Break and Enter Commercial',
                                'Break and Enter Residential/Other',
                                'Theft from Vehicle'
                            ],
                            multi=True,
                            searchable=True,
                            placeholder='All Neighbourhoods'
                        ),
                        html.Hr(),
                        Label('Neighbourhoods', html_for='neighbourhoods'),
                        Dropdown(
                            id='neighbourhoods',
                            options=[{'label': n, 'value': n}
                                     for n in np.sort(neighbourhoods)],
                            value=[
                                'Central Business District',
                                'Marpole',
                                'West Point Grey'
                            ],
                            multi=True,
                            searchable=True,
                            placeholder='All Neighbourhoods'
                        )
                    ],
                    width=3
                ),
                Col([
                    Row([
                        Col([
                            html.H5('Time series'),
                            Tabs([
                                Tab([
                                    Graph('time-plot')
                                ], label="No Facet"),
                                Tab([
                                    Graph('time-plot-by-type')
                                ], label="Facet by Type"),
                                Tab([
                                    Graph('time-plot-by-neighbourhood')
                                ], label="Facet by Neighbourhood")
                            ])
                        ])
                    ]),
                    Row([
                        Col([
                            html.H5('Heatmap'),
                            Graph('heatmap-type-by-neighbourhood')
                        ])
                    ])
                ], width=9)
            ]
        ),
        html.Footer(
            html.Div([
                html.P("Copyright (C) 2023 Kelvin Wong.",
                       className="text-muted"),
                html.P([
                    html.A("This software",
                           href="https://github.com/netsgnut/vpd-crime-data-exploration", target="_blank"),
                    " free and open source, licensed under the ",
                    html.A(
                        "MIT license", href="https://github.com/UBC-MDS/vpd-crime-data-exploration/blob/master/LICENSE", target="_blank"),
                    ". ",
                    "Uses data derived from Vancouver Police Department's ",
                    html.A("Open Data portal on GeoDASH",
                           href="https://geodash.vpd.ca/opendata", target="_blank"),
                    ". ",
                    "Use of the data is governed by the respective terms and conditions."
                ], className="text-muted")
            ], className='col-md-4 mb-0'),
            className='d-flex flex-wrap justify-content-between align-items-center py-3 my-4 border-top'
        )
    ],
    fluid=True
)


def get_filtered_data(years, types, neighbourhoods):
    """
    Get filtered data from the dataframe
    """
    df_filtered = df.copy()

    df_filtered = df_filtered[df_filtered["year"]
                              >= years[0]][df_filtered["year"] <= years[1]]

    if len(types) > 0:
        df_filtered = df_filtered[df_filtered["type"].isin(types)]

    if len(neighbourhoods) > 0:
        df_filtered = df_filtered[df_filtered["neighbourhood"].isin(
            neighbourhoods)]

    return df_filtered.reset_index(drop=True)


@app.callback(
    Output('time-plot', 'figure'),
    Input('years', 'value'),
    Input('types', 'value'),
    Input('neighbourhoods', 'value')
)
def create_time_plot_figure(year, types, neighbourhoods):
    df = get_filtered_data(year, types, neighbourhoods).groupby(
        ['year']).sum('count').reset_index()

    if len(df) == 0:
        return None

    fig = px.line(df, x='year', y='count')
    fig.update_layout(
        xaxis=dict(dtick=1),
        xaxis_title='Year',
        yaxis_title='Count',
        title='Number of Offences over Time'
    )
    return fig


@app.callback(
    Output('time-plot-by-type', 'figure'),
    Input('years', 'value'),
    Input('types', 'value'),
    Input('neighbourhoods', 'value')
)
def create_time_plot_by_type_figure(year, types, neighbourhoods):
    df = get_filtered_data(year, types, neighbourhoods).groupby(
        ['year', 'type']).sum('count').reset_index()

    if len(df) == 0:
        return None

    fig = px.line(df, x='year', y='count', color="type")
    fig.update_layout(
        xaxis=dict(dtick=1),
        xaxis_title='Year',
        yaxis_title='Count',
        legend_title_text='Type',
        title='Number of Offences over Time, Faceted by Type'
    )
    fig.update_layout(
        legend=dict(
            orientation='h',
            yanchor="bottom",
            y=-0.4,
            xanchor="right",
            x=1
        )
    )
    return fig


@app.callback(
    Output('time-plot-by-neighbourhood', 'figure'),
    Input('years', 'value'),
    Input('types', 'value'),
    Input('neighbourhoods', 'value')
)
def create_time_plot_by_neighbourhood_figure(year, types, neighbourhoods):
    df = get_filtered_data(year, types, neighbourhoods).groupby(
        ['year', 'neighbourhood']).sum('count').reset_index()

    if len(df) == 0:
        return None

    fig = px.line(df, x='year', y='count', color="neighbourhood")
    fig.update_layout(
        xaxis=dict(dtick=1),
        xaxis_title='Year',
        yaxis_title='Count',
        legend_title_text='Type',
        title='Number of Offences over Time, Faceted by Neighbourhood'
    )
    fig.update_layout(
        legend=dict(
            orientation='h',
            yanchor="bottom",
            y=-0.4,
            xanchor="right",
            x=1
        )
    )
    return fig


@app.callback(
    Output('heatmap-type-by-neighbourhood', 'figure'),
    Input('years', 'value'),
    Input('types', 'value'),
    Input('neighbourhoods', 'value')
)
def create_heatmap_type_by_neighbourhood_figure(year, types, neighbourhoods):
    df = get_filtered_data(year, types, neighbourhoods).groupby(
        ['type', 'neighbourhood']).sum('count').reset_index()
    df = df.pivot(index='type', columns='neighbourhood')['count'].fillna(0)

    if len(df) == 0:
        return None

    fig = px.imshow(df, x=df.columns, y=df.index)
    fig.update_layout(
        xaxis=dict(dtick=1),
        xaxis_title='Neighbourhood',
        yaxis_title='Offence Type',
        legend_title_text='Type',
        title='Number of Offences, Faceted by Type and Neighbourhood'
    )
    return fig


if __name__ == '__main__':
    debug_flag = "" if os.getenv('DEBUG') is None else os.getenv('DEBUG')
    app.run_server(debug=(debug_flag.lower() == 'true' or debug_flag == '1'))
