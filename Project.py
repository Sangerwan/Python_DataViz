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

                          dcc.Slider(
                                        id='surface-slider',
                                        min=france['surface'].min(),
                                        max=france['surface'].max(),
                                        value=france['surface'].median(),
                                        step=10
                                    ),     

                                
                            

                 html.Div(className="app-header",children=f'''
                                The graph above shows relationship between life expectancy and
                                GDP per capita for year . Each continent data has its own
                                colour and symbol size is proportionnal to country population.
                                Mouse over for details.'''), # (7)
                           

                ]))


    @app.callback(
        dash.dependencies.Output('map', 'figure'),
        dash.dependencies.Input('surface-slider', 'value')
    )
    def update_figure(input_value):
        proddf = france[france.surface >= input_value]

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
        proddf = france[france.surface >= input_value]

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
        
        index=np.where(sorted_surface == input_value)[0]
        print(index)
        print(index[0])
        print(index[0]-5)
        a = range(index[0]-5,index[0])

        print(a)
        x_range_min=min(x for x in range(index[0]-50,index[0]+1) if x>=0)
        x_range_max=max(x for x in range(index[0],index[0]+50) if x<sorted_surface.size)

        surface_min=min(x for x in france['surface'][x_range_min:x_range_max])
        surface_max=max(x for x in france['surface'][x_range_min:x_range_max])

        nb_panneau_min=min(x for x in france['nb_panneaux'][x_range_min:x_range_max])
        nb_panneau_max=max(x for x in france['nb_panneaux'][x_range_min:x_range_max])

        y_range_min=min(x for x in france['production_pvgis'][x_range_min:x_range_max])
        y_range_max=max(x for x in france['production_pvgis'][x_range_min:x_range_max])

        print('surface')
        print(x_range_min)
        print(x_range_max)
        print(france['surface'][x_range_min:x_range_max])

        print('prod')
        print(y_range_min)
        print(y_range_max)
        print(france['production_pvgis'][x_range_min:x_range_max])

        print('nb_panneaux')
        print(nb_panneau_min)
        print(nb_panneau_max)
        print(france['nb_panneaux'][x_range_min:x_range_max])

        print('======france======')
        print(france)
        print('======filter======')
        print(france[france.surface.isin(range(x_range_min,x_range_max))])
        print(france[france.surface.isin(range(x_range_min,x_range_max))].surface.unique())

        return px.scatter(france[france.surface.isin(range(x_range_min,x_range_max))],
                         x='surface',
                         y='production_pvgis',
                        color='orientation',
                        size='nb_panneaux',
                       hover_name='nb_panneaux',
                       labels={'x' : 'surface','y' : 'production_pvgis','color' : 'orientation','size' : 'nb_panneaux','hover_name' : 'nb_panneaux'},)

        
    def filter(data_frame, x_axis, y_axis, centered_x_value=None, x_axis_range=None, color=None, size=None, hover_name=None, label=None):
        if centered_x_value is not None:
            index=np.where(data_frame[x_axis] == input_value)[0]
            if x_axis_range is not None:
                min_index=min(x for x in range(index[0]-x_axis_range,index[0]+1) if x>=0)
                max_index=max(x for x in range(index[0],index[0]+x_axis_range) if x<data_frame[x_axis].size)
                min_value=min(value for value in data_frame[y_axis][min_index:max_index])
                max_value=max(value for value in data_frame[y_axis][min_index:max_index])
                return df.scatter(data_frame,x=x_axis,y=y_axis,color=color,size=size,hover_name=hover_name,label=label)

        return df.scatter(data_frame,x=x_axis,y=y_axis,color=color,size=size,hover_name=hover_name,label=label)

    #
    # RUN APP234
    #1

    app.run_server(debug=False) # (8)