import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import dash
import os

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

production_surface = np.zeros(len(france.production_pvgis))
for i in range(len(france.production_pvgis)):
    production_surface[i] = france.production_pvgis.array[i]/france.surface.array[i];

france.insert(6,'production_surface',production_surface,True);

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
    fig = px.scatter_geo(france, lon="lon",lat="lat",scope='europe',size_max=15, center=centerLatLon, color="production_surface", size="surface",
                            projection="natural earth")
    mapConstructeurs = px.scatter_geo(france, lon="lon",lat="lat",scope='europe',size_max=15, center=centerLatLon, color="panneaux_marque",
                            projection="natural earth")
    

    labelsValues= []
    AnneeInstallUnique = np.sort(france.an_installation.unique())
    for i in range(len(AnneeInstallUnique)):
        labelsValues.append(dict({'label' : AnneeInstallUnique[i], 'value': AnneeInstallUnique[i]}))
                                    

    app.layout = html.Div(children= ([

                            html.H1( children=f'Analyse de la production photovoltaïque en France',
                                        style={'textAlign': 'center', 'color': '#7FDBFF'}), 
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
                                        options=[{'label': i, 'value': i} for i in np.sort(france.an_installation.unique())],
                                        placeholder="Select a year",
                                        

                                    ),
                                ]),



                          ]),

                            

                            
                                
                           html.Div(className= "graphSurfaceProduction", children=    [ 
                               
                                dcc.Graph(
                                    id='map',
                                    figure=fig
                                ),                                   
                               
                                dcc.Graph(
                                    id='graph3',
                                    figure=fig2,

                                )],
                            ),
                       
                          dcc.RangeSlider(
                                        id='surface-slider',
                                        min=np.log(france['surface'].min()),
                                        max=6,
                                       
                                        value=[4,5],
                                        step=0.5,
                                         marks={
                                            0 : '0 m²',
                                            1 : '10 m²',
                                            2 : '100 m²',
                                            3 : '1000 m²',
                                            4 : '1 Hectares',
                                            5 : '10 Hectares',
                                            6 : '100 Hectares',
                                        },
                           ),  
                          

                           html.Div(className= "graphConstructeur", children=    [ 
                                   html.Div(children=
                                       dcc.Graph(
                                            id='graphFabriquants',
                                            figure=fig,

                                       ),
                                   ),
                                   
                                   html.Div(children=
                                       dcc.Graph(
                                            id='mapFabriquants',
                                            figure=mapConstructeurs,
                                       ),
                                   )
                                   
                               
                            ]),
                       
                          html.Div(className= "chexbox", children=
                                dcc.Checklist(     
                                    id='chexboxFabriquants',
                                    options=labelsValues,
                                    value=[],
                                ),
                            ),

                                
                            

                 html.Div(className="app-header",children=f'''
                                Données utilisées : https://www.data.gouv.fr/fr/datasets/donnees-sur-les-installations-photovoltaique-en-france-et-quelques-pays-europeens/  \n
                                Réalisé par Erwan Sangchanmahola et Olivier Troissant \n
                                Cadre d'étude : ESIEE Paris'''), # (7)
                           

                ]))


#-----------------------------------
#RANGESLIDER => MAP FABRIQUANTS
#-----------------------------------
@app.callback(
    dash.dependencies.Output('map', 'figure'),
    dash.dependencies.Input('surface-slider', 'value')
)
def update_figure(input_value):
    imax= np.exp(input_value[1]);
    imin= np.exp(input_value[0]);
    proddf = france[france.surface <= imax]
    proddf = proddf[proddf.surface >= imin]
        

    centerLatLon = dict({'lat': 46, 'lon': 0});
    fig = px.scatter_geo(proddf, lon="lon",lat="lat",scope='europe', size_max=10, center=centerLatLon, color="production_surface", size="surface",
                        projection="natural earth")

    fig.update_layout(transition_duration=500, geo = dict(projection_scale=5))
    return fig


#-----------------------------------
#CHECKBOX => MAP FABRIQUANTS
#-----------------------------------
@app.callback(
        dash.dependencies.Output('mapFabriquants', 'figure'),
        dash.dependencies.Input('chexboxFabriquants', 'value')
    )
def update_figure(input_value):
    proddf = france
    yearData =france

    proddf = france.where(france.an_installation.isin(input_value), proddf, False, None, None, 'raise', True)

    #for year in input_value: 
        #proddf=pd.concat([proddf,yearData], ignore_index=True)
    #yearData = france[france.an_installation. == inputvalue]

        

    centerLatLon = dict({'lat': 46, 'lon': 0});
    mapConstructeurs = px.scatter_geo(proddf, lon="lon",lat="lat",scope='europe',size_max=15, center=centerLatLon, color="panneaux_marque", 
                            projection="natural earth")
    

    mapConstructeurs.update_layout(transition_duration=500, geo = dict(projection_scale=5))
    return mapConstructeurs



#-----------------------------------
#CHECKBOX => GRAPH FABRIQUANTS
#-----------------------------------
@app.callback(
        dash.dependencies.Output('graphFabriquants', 'figure'),
        dash.dependencies.Input('surface-slider_Fabriquants', 'value')
    )
def update_figure(input_value):
   
        

    centerLatLon = dict({'lat': 46, 'lon': 0});
    fig = px.scatter_geo(france, lon="lon",lat="lat",scope='europe', size_max=15, center=centerLatLon, color="production_surface", size="production_surface",
                        projection="natural earth")

    fig.update_layout(transition_duration=500, geo = dict(projection_scale=5))
    return fig



#-----------------------------------
#YEAR DROPDOWN => HISTOGRAM
#-----------------------------------
@app.callback(
    dash.dependencies.Output('graph3', 'figure'),
    dash.dependencies.Input('surface-slider', 'value')
)
def update_figure(input_value):
    imax= np.exp(input_value[1]);
    imin= np.exp(input_value[0]);
    proddf = france[france.surface <= imax]
    proddf = proddf[proddf.surface >= imin]

    centerLatLon = dict({'lat': 35, 'lon': -5});
    fig2 = px.scatter(proddf, x="pente", y="orientation",
                        color="production_surface",
                    hover_name="nb_panneaux")

    fig2.update_layout(transition_duration=500)
    fig2.update_coloraxes(showscale=False)
    return fig2



#-----------------------------------
#YEAR DROPDOWN => HISTOGRAM
#-----------------------------------
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
