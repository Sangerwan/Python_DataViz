import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import dash
import os
from scipy import *

import plotly_express as px

import dash
import dash_core_components as dcc
import dash_html_components as html
import requests
import zipfile
import io

#https://www.data.gouv.fr/fr/datasets/donnees-sur-les-installations-photovoltaique-en-france-et-quelques-pays-europeens/

path = os.getcwd()


data_url="https://www.data.gouv.fr/fr/datasets/r/12b8efc1-6c38-46ab-8cfa-6220970fa260"
request = requests.get(data_url, stream=True)
zip = zipfile.ZipFile(io.BytesIO(request.content))
zip.extractall("./data")

df=pd.read_csv("./data/BDPV-opendata-installations.csv", sep=';')

#Remove sud
df['orientation']=df['orientation'].replace("Sud",0);# SUD=0
df['orientation']=df['orientation'].replace("South",0);# SUD=0
df['orientation']=df['orientation'].replace("Sur",0);# SUD=0
#remove Pas_dans_la_liste_panneaux
df=df[df.panneaux_modele != 'Pas_dans_la_liste_panneaux']
#remove 0 prod
df=df[df.production_pvgis != 0]
#remove 0 surface
df=df[df.surface != 0]

france=df.query("country == 'France'")

production_surface = zeros(len(france.production_pvgis))
for i in range(len(france.production_pvgis)):
    production_surface[i] = france.production_pvgis.array[i]/france.surface.array[i];

france.loc[:,'production_surface'] = production_surface;

if __name__ == '__main__':

    app = dash.Dash(__name__)

    unique_par_an=france.groupby('an_installation').size()
    
    fig1 = px.histogram(france, x='an_installation',y='nb_panneaux', labels={'an_installation' : 'année d\'installation','nb_panneaux' : 'nombres de panneaux'})

    fig3 = px.histogram(france, x='panneaux_marque',y='nb_panneaux')
    fig3.layout.xaxis.title="marque du panneau"
    fig3.layout.yaxis.title="nombres de panneaux installés"
    fig3.update_xaxes(categoryorder="total descending")

    fig2 = px.scatter(france, x="pente", y="orientation",
                        color="production_surface",
                        hover_name="nb_panneaux") # (4)
    
    centerLatLon = dict({'lat': 35, 'lon': -5});
    fig = px.scatter_geo(france, lon="lon",lat="lat",scope='europe',size_max=15, center=centerLatLon, color="production_surface", size="production_surface",
                            projection="natural earth")
    

    app.layout = html.Div(children= ([

                            html.H1( children=f'Production des panneaux solaires en fonction de la surface',
                                        style={'textAlign': 'center', 'color': '#7FDBFF'}), # (5)
                            ##
                            html.Div(dcc.Input(id='input-on-submit', type='text')),
                                html.Button('Submit', id='submit-val', n_clicks=0),
                                html.Div(className="app-header", id='container-button-basic', children='Enter a value and press submit'),
                            ##
                            
                            dcc.Graph(
                                    id='histogram1',
                                    figure=fig1,
                                    
                                

                                ),

                            html.Div([

                                dcc.Graph(
                                    id='histogram_brand',
                                    figure=fig3,
                                

                                ),

                                html.Div([
                                        
                                    #dcc.Dropdown(
                                    #    options=[{'label': i, 'value': i} for i in france.columns],
                                        
                                    #),
                                    #dcc.RadioItems(
                                    #    id='filter_type_historgram_brand',
                                    #    options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                                    #    value='Linear',
                                    #    #labelStyle={'display': 'inline-block'},
                                    #),
                                    dcc.Dropdown(
                                        id="year_dropdown_historgram_brand",
                                        options=[{'label': i, 'value': i} for i in sort(france.an_installation.unique())],
                                        placeholder="Select a year",
                                        

                                    ),
                                ]),



                          ]),

                            

                            
                                
                           html.Div(className= "graph2", children=    [ 
                               html.Div(className= "map", children  =[
                                   dcc.Graph(
                                        id='map',
                                        figure=fig
                                    ),
                                   
                               ]),
                               
                                dcc.Graph(
                                    id='graph3',
                                    figure=fig2,

                                )],
                            ),
                       
                          dcc.RangeSlider(
                                        id='surface-slider',
                                        min=france['surface'].min(),
                                        max=france['surface'].max(),
                                       
                                        value=[int(france['surface'].median()),int(france['surface'].median()*2)],
                                        step=2,
                                         marks={
                                            0  : '0 m²',
                                            10 : '10 m²',
                                            50 : '50 m²',
                                            100 : '100 m²',
                                            200 : '200 m²',
                                            300 : '300 m²',
                                            500 : '500 m²',
                                            800 : '800 m²',
                                        },
                           ),  
                          

                           html.Div(className= "graph2", children=    [ 
                               html.Div(className= "map", children  =[

                                   dcc.Graph(
                                    id='graphFabriquants',
                                    figure=fig2,

                                   ),
                                   dcc.Graph(
                                        id='mapFabriquants',
                                        figure=fig
                                   ),
                                   
                               ])
                               
                            ]),
                       
                          dcc.RangeSlider(
                                        id='surface-slider_Fabriquants',
                                        min=france['surface'].min(),
                                        max=france['surface'].max(),
                                       
                                        value=[int(france['surface'].median()),int(france['surface'].median()*2)],
                                        step=2,
                                         marks={
                                            0  : '0 m²',
                                            10 : '10 m²',
                                            50 : '50 m²',
                                            100 : '100 m²',
                                            200 : '200 m²',
                                            300 : '300 m²',
                                            500 : '500 m²',
                                            800 : '800 m²',
                                        },
                           ),

                                
                            

                 html.Div(className="app-header",children=f'''
                                Données utilisées : https://www.data.gouv.fr/fr/datasets/donnees-sur-les-installations-photovoltaique-en-france-et-quelques-pays-europeens/  \n
                                Réalisé par Erwan Sangchanmahola et Olivier Troissant \n
                                Cadre d'étude : ESIEE Paris'''), # (7)
                           

                ]))





@app.callback(
    dash.dependencies.Output('map', 'figure'),
    dash.dependencies.Input('surface-slider', 'value')
)
def update_figure(input_value):
    proddf = france[france.surface <= input_value[1]]
    proddf = proddf[proddf.surface >= input_value[0]]
        

    centerLatLon = dict({'lat': 46, 'lon': 0});
    fig = px.scatter_geo(proddf, lon="lon",lat="lat",scope='europe', size_max=10, center=centerLatLon, color="production_surface", size="production_surface",
                        projection="natural earth")

    fig.update_layout(transition_duration=500, geo = dict(projection_scale=5))
    return fig


@app.callback(
        dash.dependencies.Output('mapFabriquants', 'figure'),
        dash.dependencies.Input('surface-slider_Fabriquants', 'value')
    )
def update_figure(input_value):
    proddf = france[france.surface <= input_value[1]]
    proddf = proddf[proddf.surface >= input_value[0]]
        

    centerLatLon = dict({'lat': 46, 'lon': 0});
    fig = px.scatter_geo(proddf, lon="lon",lat="lat",scope='europe', size_max=10, center=centerLatLon, color="production_surface", size="production_surface",
                        projection="natural earth")

    fig.update_layout(transition_duration=500, geo = dict(projection_scale=5))
    return fig

@app.callback(
        dash.dependencies.Output('graphFabriquants', 'figure'),
        dash.dependencies.Input('surface-slider_Fabriquants', 'value')
    )
def update_figure(input_value):
    proddf = france[france.surface <= input_value[1]]
    proddf = proddf[proddf.surface >= input_value[0]]
        

    centerLatLon = dict({'lat': 46, 'lon': 0});
    fig = px.scatter_geo(proddf, lon="lon",lat="lat",scope='europe', size_max=10, center=centerLatLon, color="production_surface", size="production_surface",
                        projection="natural earth")

    fig.update_layout(transition_duration=500, geo = dict(projection_scale=5))
    return fig


@app.callback(
    dash.dependencies.Output('graph3', 'figure'),
    dash.dependencies.Input('surface-slider', 'value')
)
def update_figure(input_value):
    proddf = france[france.surface <= input_value[1]]
    proddf = proddf[proddf.surface >= input_value[0]]

    centerLatLon = dict({'lat': 35, 'lon': -5});
    fig2 = px.scatter(proddf, x="pente", y="orientation",
                        color="production_surface",
                    hover_name="nb_panneaux")

    fig2.update_layout(transition_duration=500)
    fig2.update_coloraxes(showscale=False)
    return fig2





    @app.callback(
    dash.dependencies.Output(component_id='histogram_brand', component_property='figure'), # (1)
    [dash.dependencies.Input(component_id='year_dropdown_historgram_brand', component_property='value')] # (2)
    )
    def update_figure(input_value): # (3)
        if input_value == None:
            fig3 = px.histogram(france, x='panneaux_marque',y='nb_panneaux')
            fig3.layout.xaxis.title="marque du panneau"
            fig3.layout.yaxis.title="nombres de panneaux installés"
            fig3.update_xaxes(categoryorder="total descending")
            return fig3
        
        constructeur_an_df = france[france.an_installation == input_value]

        fig3 = px.histogram(constructeur_an_df, x='panneaux_marque',y='nb_panneaux')
        fig3.layout.xaxis.title="marque du panneau"
        fig3.layout.yaxis.title="nombres de panneaux installés"
        fig3.update_xaxes(categoryorder="total descending")

        return fig3



    app.run_server(debug=False) # (8)