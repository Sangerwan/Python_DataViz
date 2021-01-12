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

print('describe')
print(df.describe())
print('value')
print(df.values)
print('column')
print(df.columns)
print('index')
print(df.index)
i= df.columns

country= df['country']
print(country.unique())

france=df.query("country == 'France'")

print(france['id'])
print(france['an_installation'].unique())

print(france);
production = france["production_pvgis"]
surface = france["surface"]
#france = france[france.surface!=8388607]

print(surface.unique())
#
# Data
#



production_surface = zeros(len(production))
for i in range(len(production)):
    production_surface[i] = production.array[i]/surface.array[i];

france.loc[:,'production_surface'] = production_surface;

print(france.columns);
france
production
surface
surfaces= surface.unique()
print('surface')
print(surfaces)
print(type(surfaces))
sorted_surface=np.sort(surfaces)
print(sorted_surface)
france = france.sort_values(by=['surface'])

print(type(df))

#




if __name__ == '__main__':

    app = dash.Dash(__name__) # (3)

    
    fig1 = px.scatter(france, x="surface", y="production_pvgis",
                        color="orientation",
                        size="nb_panneaux",
                        hover_name="nb_panneaux") # (4)

    fig2 = px.scatter(france, x="panneaux_marque", y="production_surface",
                        color="production_surface",
                        hover_name="nb_panneaux") # (4)
    
    centerLatLon = dict({'lat': 46, 'lon': 0});
    fig = px.scatter_geo(france, lon="lon",lat="lat",scope='europe',size_max=23, center=centerLatLon, color="production_pvgis", size="production_surface",
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

                            
                                
                           html.Div(className= "map", children=    [ dcc.Graph(
                                    id='map',
                                    figure=fig
                                ),
                                dcc.Graph(
                                    id='graph3',
                                    figure=fig2,

                                )],
                            ),

                           html.Div(children=
                                    dcc.Slider(
                                    id='prod-slider',
                                    min=france['production_surface'].min(),
                                    max=france['production_surface'].max(),
                                    value=france['production_surface'].median(),
                                    step=10
                                ),                                      
                           ),

                                
                            

                 html.Div(className="app-header",children=f'''
                                The graph above shows relationship between life expectancy and
                                GDP per capita for year . Each continent data has its own
                                colour and symbol size is proportionnal to country population.
                                Mouse over for details.'''), # (7)
                           

                ]))


    @app.callback(
        dash.dependencies.Output('map', 'figure'),
        dash.dependencies.Input('prod-slider', 'value')
    )
    def update_figure(input_value):
        proddf = france[france.production_surface >= input_value]

        centerLatLon = dict({'lat': 46, 'lon': 0});
        fig = px.scatter_geo(proddf, lon="lon",lat="lat",scope='europe', size_max=5, center=centerLatLon, color="production_pvgis", size="production_surface",
                            projection="natural earth")

        fig.update_layout(transition_duration=500)
        return fig





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