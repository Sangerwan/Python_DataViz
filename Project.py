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

#https://www.data.gouv.fr/fr/datasets/donnees-sur-les-installations-photovoltaique-en-france-et-quelques-pays-europeens/

path = os.getcwd()
####
#Pas_dans la liste
#Sud
#production 0
#orientation_optimum nan
#pente optimum
#postal_code_suffix
#
###
print(path)
df=pd.read_csv("./BDPV-opendata-installations/BDPV-opendata-installations.csv", sep=';')
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
df=df[df.surface < 1000]
df=df[df.production_pvgis < 50000 ]



for col in df:
    print(col)
    print(df[col].unique())

i= df.columns

country= df['country']

france=df.query("country == 'France'")



production = france["production_pvgis"]
surface = france["surface"]
#france = france[france.surface!=8388607]


#
# Data
#



production_surface = zeros(len(production))
for i in range(len(production)):
    production_surface[i] = production.array[i]/surface.array[i];

france.loc[:,'production_surface'] = production_surface;


surfaces= surface.unique()

sorted_surface=np.sort(surfaces)

france = france.sort_values(by=['surface'])


#




if __name__ == '__main__':

    app = dash.Dash(__name__) # (3)

    
    fig1 = px.scatter(france, x="surface", y="production_pvgis",
                        color="orientation",
                        size="nb_panneaux",
                        hover_name="nb_panneaux") # (4)

    fig2 = px.scatter(france, x="pente", y="orientation",
                        color="production_surface",
                        hover_name="nb_panneaux") # (4)
    
    centerLatLon = dict({'lat': 35, 'lon': -5});
    fig = px.scatter_geo(france, lon="lon",lat="lat",scope='europe',size_max=15, center=centerLatLon, color="production_surface", size="production_surface",
                            projection="natural earth")
    

    app.layout = html.Div(children= ([

                            html.H1( children=f'Production des panneaux solaires en fonction de la surface',
                                        style={'textAlign': 'center', 'color': '#7FDBFF'}), # (5)

                            html.Div(dcc.Input(id='input-on-submit', type='text')),
                                html.Button('Submit', id='submit-val', n_clicks=0),
                                html.Div(className="app-header", id='container-button-basic', children='Enter a value and press submit'),

                            
                            dcc.Graph(
                                id='graph1',
                                figure=fig1,

                            ), # (6)

                            html.Label('surface'),
                                    dcc.Dropdown(
                                        id="surface_dropdown_graph1",
                                        options=[{'label': i, 'value': i} for i in sorted_surface],
                                        value=sorted_surface[0]
                            ),

                            
                                
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
    dash.dependencies.Output(component_id='graph1', component_property='figure'), # (1)
    [dash.dependencies.Input(component_id='surface_dropdown_graph1', component_property='value')] # (2)
    )
    def update_figure(input_value): # (3)
        
        index=np.asarray(np.where(sorted_surface == input_value))
        print(index)
        print(type(index))
        print(index-5)
        #range=[x for x in [index-5,index+5] if x>=0 and x< np.unique(sorted_surface, return_counts=True) ]
        return px.scatter(france, x="surface", y="production_pvgis",
                        color="orientation",
                        size="nb_panneaux",
                       hover_name="nb_panneaux",
                       range_x= (0,2)) # (4)
    #lol ceci est un test
        


    #
    # RUN APP234
    #1

    app.run_server(debug=False) # (8)