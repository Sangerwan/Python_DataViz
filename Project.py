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

for i in range (len(france.orientation)):
    france.orientation.array[i]=str(int(france.orientation.array[i])+180)

production_surface = np.zeros(len(france.production_pvgis))
for i in range(len(france.production_pvgis)):
    production_surface[i] = france.production_pvgis.array[i]/france.surface.array[i];

france.insert(6,'production_surface',production_surface,True);

Nom_colonnes= {
    'mois_installation': 'mois d\'installation',
    'an_installation': 'année d\'installation',
    'nb_panneaux': 'nombre de panneaux',
    'panneaux_marque': 'marque du panneau',
    'panneaux_modele': 'modèle du panneau',
    'nb_onduleur': 'nombre d\'onduleurs',
    'onduleur_marque': 'marque de l\'onduleur',
    'onduleur_modele': 'modèle de l\'onduleur',
    'puissance_crete': 'puissance crète (Wc)',
    'surface': 'surface (m²)',
    'pente': 'pente (°)',
    'pente_optimum': 'pente optimum (°)',
    'orientation' : 'orientation par rapport au Sud',
    'orientation_optimum': 'orientation optimum par rapport au Sud',
    'installateur': 'installateur',
    'production_pvgis': 'production annuelle (kWh)',
    'lat': 'latitude',
    'lon': 'longitude',
    }

if __name__ == '__main__':

    app = dash.Dash(__name__)

    unique_par_an=france.groupby('an_installation').size()
    
    fig1 = px.histogram(france, x='an_installation',y='nb_panneaux')

    fig3 = px.histogram(france, x='panneaux_marque',y='nb_panneaux')
    fig3.layout.xaxis.title="marque du panneau"
    fig3.layout.yaxis.title="nombre de panneaux installés"
    fig3.update_xaxes(categoryorder="total descending")

    figPolar = px.scatter_polar(france, r="nb_panneaux",log_r=True, theta="orientation")

    figPuissance =  px.violin(france, y=france.puissance_crete,x="an_installation",log_y=True,log_x=False, color="an_installation", box=True, 
                                hover_data=france.columns)

    fig2 = px.scatter(france, x="pente", y="orientation",
                        color="production_surface",
                        hover_name="nb_panneaux") 
    
    centerLatLon = dict({'lat': 46, 'lon': 2});
    fig = px.scatter_geo(france, lon="lon",lat="lat",scope='europe',size_max=15, center=centerLatLon, color="production_surface", size="surface",
                            projection="natural earth")
    mapConstructeurs = px.scatter_geo(france, lon="lon",lat="lat",scope='europe',size_max=15, center=centerLatLon, color="panneaux_marque",
                            projection="natural earth")
    

    labelsValues= []
    AnneeInstallUnique = np.sort(france.an_installation.unique())
    for i in range(len(AnneeInstallUnique)):
        if (AnneeInstallUnique[i] != 1993):
            labelsValues.append(dict({'label' : AnneeInstallUnique[i], 'value': AnneeInstallUnique[i]}))
    
    mapConstructeurs.update_layout(transition_duration=500, geo = dict(projection_scale=5))
    fig.update_layout(transition_duration=500, geo = dict(projection_scale=5))

    app.layout = html.Div(children= ([

                            html.H1( children=f'Analyse de la production photovoltaïque en France',
                                        style={'textAlign': 'center', 'color': '#7FDBFF'}), 
                            html.Div([
                                            
                                    dcc.Dropdown(
                                        id='figure1_type',
                                        options=[
                                            {'label': 'Histogramme', 'value': 'Histogramme'}, 
                                            {'label': 'Nuage de points', 'value': 'Nuage'}
                                            ],
                                        value='Histogramme',
                                        clearable=False,
                                    ),
                                                                           
                                    
                            ]),

                            html.Div([
                                    
                                dcc.Graph(
                                    id='figure1',
                                    figure=fig1,
                                ),

                                html.Div([

                                    html.Div(id='figure1_title',
                                             style={'color': 'blue', 'fontSize': 24,'textAlign': 'center'},
                                             ),
                                    html.Div([
                                            dcc.Dropdown(
                                                id='x_dropdown_figure1',
                                                options=[{'label': v, 'value': k} for k,v in Nom_colonnes.items()],
                                                value="an_installation",
                                                clearable=False,
                                                placeholder='',
                                            ),                         
                                    ], style={'width': '49%', 'display': 'inline-block'}),

                                    html.Div([
                                        
                                            dcc.Dropdown(
                                                id='y_dropdown_figure1',
                                                options=[{'label': v, 'value': k} for k,v in Nom_colonnes.items()],
                                                value='nb_panneaux',
                                                clearable=False,
                                                placeholder='',
                                            ),
                                        
                                    ],style={'width': '49%', 'display': 'inline-block'}
                                    ),
                                ]),
                            ]),
                            

                            html.Div([

                                    dcc.Graph(
                                        id='histogram_brand',
                                        figure=fig3,
                                

                                    ),

                                html.Div([
                                        

                                    dcc.Dropdown(
                                        id='year_dropdown_historgram_brand',
                                        options=[{'label': i, 'value': i} for i in np.sort(france.an_installation.unique())],
                                        placeholder='Select a year',
                                        value=2006                    
                                    ),
                                ]),



                          ]),

                        html.Div(className= "graphSurfaceProduction", children=    [ 
                               
                                dcc.Graph(
                                    id='histogram1',
                                    figure=fig1,
                                ),                                  
                               
                                dcc.Graph(
                                    id='graph3skks',
                                    figure=figPolar,
                                )

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
                                       
                                        value=[4,4.5],
                                        step=0.2,
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
                                            figure=figPuissance,

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
                                    value=[2004,2006],
                                ),
                            ),

                                
                            

                 html.Div(className="app-header",children=f'''
                                Données utilisées : https://www.data.gouv.fr/fr/datasets/donnees-sur-les-installations-photovoltaique-en-france-et-quelques-pays-europeens/  
                                '''),
                  html.Div(className="app-header",children=f'''Réalisé par Erwan Sangchanmahola et Olivier Troissant 
                                Cadre d'étude : ESIEE Paris'''),
                           
    ]))
                


#-----------------------------------
#RANGESLIDER => MAP PRODUCTION
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
        

    centerLatLon = dict({'lat': 46, 'lon': 2});
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
    
    proddf=france[france.an_installation == 67]
    yearData =france[france.an_installation == 66]
    if (input_value!=[]):        
        for year in input_value: 
            yearData = france[france.an_installation == year]
            proddf=pd.concat([proddf,yearData], ignore_index=True)
    else :
        proddf=france
       
    centerLatLon = dict({'lat': 46, 'lon': 2});
    mapConstructeurs = px.scatter_geo(proddf, lon="lon",lat="lat",scope='europe',size_max=15, center=centerLatLon, color="panneaux_marque", 
                            projection="natural earth")
    

    mapConstructeurs.update_layout(transition_duration=500, geo = dict(projection_scale=5))
    return mapConstructeurs






#-----------------------------------
#CHECKBOX => GRAPH VIOLIN FABRIQUANTS
#-----------------------------------
@app.callback(
        dash.dependencies.Output('graphFabriquants', 'figure'),
        dash.dependencies.Input('chexboxFabriquants', 'value')
    )
def update_figure(input_value):
    proddf=france[france.an_installation == 67]
    yearData =france[france.an_installation == 66]
    if (input_value!=[]):        
        for year in input_value: 
            yearData = france[france.an_installation == year]
            proddf=pd.concat([proddf,yearData], ignore_index=True)
    else :
        proddf=france        
        input_value=france.an_installation

    figPuissance =  px.violin(proddf, y=proddf.puissance_crete,x="an_installation",log_y=True,log_x=False, color="an_installation", box=True,
          hover_data=proddf.columns)
    figPuissance.update_layout(transition_duration=500)
    figPuissance.update_xaxes(type='category')
    return figPuissance

@app.callback(
    dash.dependencies.Output(component_id='figure1_title', component_property='children'),
    [dash.dependencies.Input(component_id='x_dropdown_figure1', component_property='value'),
    dash.dependencies.Input(component_id='y_dropdown_figure1', component_property='value')]
    )
def update_histogram_title(x_axis, y_axis):
    return '"' +Nom_colonnes[y_axis]+'"' + ' en fontcion de ' + '"'+Nom_colonnes[x_axis]+'"'


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
dash.dependencies.Output(component_id='figure1', component_property='figure'),
[dash.dependencies.Input(component_id='figure1_type', component_property='value'),
dash.dependencies.Input(component_id='x_dropdown_figure1', component_property='value'),
dash.dependencies.Input(component_id='y_dropdown_figure1', component_property='value')]
)
def update_figure(type, x_axis, y_axis):
    
    if type == 'Nuage':
        nuage = px.scatter(france, x=x_axis,y=y_axis)
        nuage.layout.xaxis.title=Nom_colonnes[x_axis]
        nuage.layout.yaxis.title=Nom_colonnes[y_axis]
        return nuage
    if type =='Histogramme':
        histogram = px.histogram(france, x=x_axis,y=y_axis)
        histogram.layout.xaxis.title=Nom_colonnes[x_axis]
        histogram.layout.yaxis.title=Nom_colonnes[y_axis]
        return histogram
    else: 
        print('type error')
        return


#-----------------------------------
#YEAR DROPDOWN => HISTOGRAM
#-----------------------------------
@app.callback(
dash.dependencies.Output(component_id='histogram_brand', component_property='figure'),
[dash.dependencies.Input(component_id='year_dropdown_historgram_brand', component_property='value')]
)
def update_figure(input_value):
    if input_value == None:
        fig3 = px.histogram(france, x='panneaux_marque',y='nb_panneaux')
        fig3.layout.xaxis.title="marque du panneau"
        fig3.layout.yaxis.title="nombre de panneaux installés"
        fig3.update_xaxes(categoryorder="total descending")
        return fig3
        
    constructeur_an_df = france[france.an_installation == input_value]

    fig3 = px.histogram(constructeur_an_df, x='panneaux_marque',y='nb_panneaux')
    fig3.layout.xaxis.title="marque du panneau"
    fig3.layout.yaxis.title="nombre de panneaux installés"
    fig3.update_xaxes(categoryorder="total descending")

    return fig3



app.run_server(debug=False)
