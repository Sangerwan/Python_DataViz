import zipfile
import io
import numpy as np
import pandas as pd
import dash
import plotly_express as px
import dash_core_components as dcc
import dash_html_components as html
import requests


"""
    Projet Data_Viz:

    Visualisation des informations sur les panneaux solaires en france

    url: http://127.0.0.1:8050/
    données utilisées: https://www.data.gouv.fr/fr/datasets/donnees-sur-les-installations-photovoltaique-en-france-et-quelques-pays-europeens/
"""

DATA_URL = "https://www.data.gouv.fr/fr/datasets/r/12b8efc1-6c38-46ab-8cfa-6220970fa260"
request = requests.get(DATA_URL, stream=True)
data = zipfile.ZipFile(io.BytesIO(request.content))
data.extractall("./data")

df = pd.read_csv("./data/BDPV-opendata-installations.csv", sep=';')

#Remove sud
df['orientation'] = df['orientation'].replace("Sud",0)# SUD=0
df['orientation'] = df['orientation'].replace("South",0)
df['orientation'] = df['orientation'].replace("Sur",0)
#remove Pas_dans_la_liste_panneaux
df = df[df.panneaux_modele != 'Pas_dans_la_liste_panneaux']
#remove 0 prod
df = df[df.production_pvgis != 0]
#remove 0 surface
df = df[df.surface != 0]
df=df.fillna(0)
france = df.query("country == 'France'")

orientation_polar = np.zeros(len(france.orientation))
for i in range(len(france.orientation)):
    orientation_polar[i] = str(int(france.orientation.array[i]) + 180)
france.insert(7,'orientation_polar',orientation_polar,True)

production_surface = np.zeros(len(france.production_pvgis))
for i in range(len(france.production_pvgis)):
    production_surface[i] = france.production_pvgis.array[i] / france.surface.array[i]
france.insert(6,'production_surface',production_surface,True)

france['orientation'] = france.orientation.astype(float)

Nom_colonnes = {
    'id': 'id',
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

print(france.pente_optimum)
if __name__ == '__main__':

    app = dash.Dash(__name__)

    unique_par_an = france.groupby('an_installation').size()

    figPolar = px.scatter_polar(france, r="production_surface",log_r=True, theta="orientation_polar",color='production_surface',range_color=[20,300])
    center_lat_lon = dict({'lat': 46, 'lon': 2})

    app.layout = html.Div(className="main",
        children=([

            html.H1(
                children='Analyse de la production photovoltaïque en France',
                style={'textAlign': 'center', 'color': '#7FDBFF'}
                ),

            html.Div([
                dcc.Dropdown(
                    id='figure1_type',
                    options=[
                        {'label': 'Histogramme', 'value': 'Histogramme'},
                        {'label': 'Nuage de points', 'value': 'Nuage'}
                        ],
                    value='Histogramme',
                    clearable=False,),
                ]),

            html.Div([
                dcc.Graph(
                    id='figure1',
                    ),

                html.Div([
                    html.Div(
                        id='figure1_title',
                        style={'color': 'blue', 'fontSize': 24,'textAlign': 'center'},
                        ),

                    html.Div([
                        dcc.Dropdown(
                            id='x_dropdown_figure1',
                            options=[
                                {'label': v, 'value': k} for k,v in Nom_colonnes.items()
                                ],
                            value='nb_panneaux',
                            clearable=False,
                            placeholder='',
                            )
                        ],
                        style={'width': '49%', 'display': 'inline-block'}
                        ),

                    html.Div([
                        dcc.Dropdown(
                            id='y_dropdown_figure1',
                            options=[
                                {'label': v, 'value': k} for k,v in Nom_colonnes.items()
                                ],
                            value="an_installation",
                            clearable=False,
                            placeholder='',
                            )
                        ],
                        style={'width': '49%', 'display': 'inline-block'}
                        ),
                    ]),

                html.Div([
                    html.Button(
                        'Inverser les axes',
                        id='invert_axes')
                    ])
                ]),


            html.Div([
                dcc.Graph(
                    id='histogram_brand',
                    ),

                html.Div(
                    'Nombre de panneaux installés par année',
                    style={'color': 'blue', 'fontSize': 24,'textAlign': 'center'},
                    ),

                html.Div([
                    dcc.Dropdown(
                        id='year_dropdown_historgram_brand',
                        options=[
                            {'label': i, 'value': i} for i in np.sort(france.an_installation.unique())
                            ],
                        placeholder='Select a year',
                        value=2006),
                    ]),
                ]),

            html.Div(className= "pente_orientation",
                children=[
                dcc.Graph(
                    id='scatter_pente_orientation',
                    ),

                html.Div(
                    id='scatter_pente_orientation_title',
                    style={'color': 'blue', 'fontSize': 24,'textAlign': 'center'},
                    ),

                html.Div([
                    dcc.Dropdown(
                        id='scatter_pente_orientation_dropdown',
                        options=[
                            {'label': 'pente', 'value': 'pente'},
                            {'label': 'orientation', 'value': 'orientation'},
                            ],
                        clearable=False,
                        value='pente'
                        ),
                    ]),
                ]),

            html.Div(
                className= "polarGraph",
                children= [
                    dcc.Graph(
                        id='polar',
                        figure=figPolar
                     ),
               ]),


            html.Div(
                className= "blocSlider",
                children=[

                html.Div(
                'Moyenne d\'orientation des panneaux',
                style={'color': 'blue', 'fontSize': 24,'textAlign': 'center'},
                ),

                html.Div(
                    className= "graphSurfaceProduction",
                    children=[
                        dcc.Graph(
                            id='map',
                            ),
                        dcc.Graph(
                            id='graph3'
                            ),
                        ]
                    ),

                dcc.RangeSlider(
                    id='surface-slider',
                    min=np.log(france['surface'].min()),
                    max=6,

                    value=[4,4.3],
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
             ]),


            html.Div(
                className= "graphConstructeur",
                children=[
                    html.Div(
                        children=[
                            dcc.Graph(
                                id='graphPuissanceCrete'
                                ),
                            ],
                        ),
                    html.Div(
                        children=[
                            dcc.Graph(
                                id='mapFabriquants'
                                ),
                            ],
                        )
                    ]
                ),

            html.Div(
                className= "chexbox",
                children=dcc.Checklist(
                    id='chexboxFabriquants',
                    options=[
                        {'label': i, 'value': i} for i in np.sort(france.an_installation.unique())
                        ],
                    value=[2004,2006],
                    ),
                ),




            html.Div(
                className="app-header",
                children='''
                        Données utilisées : https://www.data.gouv.fr/fr/datasets/donnees-sur-les-installations-photovoltaique-en-france-et-quelques-pays-europeens/
                        '''
                ),
            html.Div(
                className="app-header",
                children='''
                Réalisé par Erwan Sangchanmahola et Olivier Troissant
                        Cadre d'étude : ESIEE Paris'''
                )
            ])
        )




#-----------------------------------
#RANGESLIDER => MAP PRODUCTION
#-----------------------------------
@app.callback(
    dash.dependencies.Output('map', 'figure'),
    dash.dependencies.Input('surface-slider', 'value')
    )
def update_mapProduction(input_value):
    """
    Change la plage de données à afficher sur la carte en fonction de la surface sélectionnée
    Args: 
        input_value[0] min 
        input_value[1] max
    """
    imax = np.exp(input_value[1])
    imin = np.exp(input_value[0])
    proddf = france[france.surface <= imax]
    proddf = proddf[proddf.surface >= imin]

    mapProduction = px.scatter_geo(proddf, lon="lon",lat="lat",scope='europe', size_max=10,
                            center=center_lat_lon, color="production_surface", size="surface",
                            projection="natural earth")

    mapProduction.update_layout(transition_duration=500, geo = dict(projection_scale=5))
    return mapProduction


#-----------------------------------
#CHECKBOX => MAP FABRIQUANTS
#-----------------------------------
@app.callback(
    dash.dependencies.Output('mapFabriquants', 'figure'),
    dash.dependencies.Input('chexboxFabriquants', 'value')
    )
def update_mapConstructeurs(input_value):
    """
    Change la plage de données à afficher sur la carte en fonction des années cochées
    Args: 
        Series "year"[]
    """
    proddf = france[france.an_installation == 67]
    year_data = france[france.an_installation == 66]
    if input_value != []:
        for year in input_value:
            year_data = france[france.an_installation == year]
            proddf = pd.concat([proddf,year_data], ignore_index=True)
    else :
        proddf = france

    mapConstructeurs = px.scatter_geo(proddf, lon="lon",lat="lat",scope='europe',size_max=15,
                                        center=center_lat_lon, color="panneaux_marque",
                                        projection="natural earth")

    mapConstructeurs.update_layout(transition_duration=500, geo = dict(projection_scale=5))
    return mapConstructeurs

#-----------------------------------
#CHECKBOX => GRAPH VIOLIN PUISSANCE
#-----------------------------------
@app.callback(
    dash.dependencies.Output('graphPuissanceCrete', 'figure'),
    dash.dependencies.Input('chexboxFabriquants', 'value')
    )
def update_violonPuissance(input_value):
    """
    Change la plage de données à afficher sur le graph en fonction des années cochées
    Args: 
        Series "year"[]
    """
    proddf = france[france.an_installation == 67]
    year_data = france[france.an_installation == 66]
    if input_value != []:
        for year in input_value:
            year_data = france[france.an_installation == year]
            proddf = pd.concat([proddf,year_data], ignore_index=True)
    else :
        proddf = france
        input_value = france.an_installation

    violonPuissance = px.violin(proddf, y=proddf.puissance_crete,x="an_installation",log_y=True,
                                log_x=False, color="an_installation", box=True,
                                hover_data=proddf.columns)
    violonPuissance.update_layout(transition_duration=500)
    violonPuissance.update_xaxes(type='category')
    return violonPuissance



#-----------------------------------
#YEAR DROPDOWN => HISTOGRAM PROD/PENTE
#-----------------------------------
@app.callback(
    dash.dependencies.Output('graph3', 'figure'),
    dash.dependencies.Input('surface-slider', 'value')
    )
def update_figureProdPente(input_value):
    """
    Change la plage de données à afficher sur le graph en fonction de la surface sélectionnée
    Args: 
        input_value[0] min 
        input_value[1] max
    """
    imax = np.exp(input_value[1])
    imin = np.exp(input_value[0])
    proddf = france[france.surface <= imax]
    proddf = proddf[proddf.surface >= imin]

    figureProdPente = px.scatter(proddf, x="pente", y="orientation",
                        color="production_surface",
                    hover_name="nb_panneaux")

    figureProdPente.update_layout(transition_duration=500)
    figureProdPente.update_coloraxes(showscale=False)
    return figureProdPente


@app.callback(
    dash.dependencies.Output('figure1_title', 'children'),
    [dash.dependencies.Input('x_dropdown_figure1', 'value'),
    dash.dependencies.Input('y_dropdown_figure1', 'value')]
    )
def update_figure1_title(x_axis, y_axis):
    """
    Retourne le titre du graphique
    Args:
        x_axis: valeur de l'abscisse
        y_axis: valeur de l'ordonnée
    """
    return '"' + Nom_colonnes[y_axis] + '"' + ' en fonction de ' + '"' + Nom_colonnes[x_axis] + '"'


@app.callback(
    dash.dependencies.Output('x_dropdown_figure1', 'value'),
    dash.dependencies.Output('y_dropdown_figure1', 'value'),
    [dash.dependencies.Input('invert_axes', 'n_clicks'),
    dash.dependencies.State('x_dropdown_figure1', 'value'),
    dash.dependencies.State('y_dropdown_figure1', 'value')]
    )
def invert_figure1_axes(button, x_axis, y_axis):
    """
    Inverse les axes du graphique quand le bouton change d'état
    Args:
        button: le bouton
        x_axis: valeur de l'abscisse
        y_axis: valeur de l'ordonnée
    """
    return y_axis, x_axis

@app.callback(
    dash.dependencies.Output('figure1', 'figure'),
    [dash.dependencies.Input('figure1_type', 'value'),
    dash.dependencies.Input('x_dropdown_figure1', 'value'),
    dash.dependencies.Input('y_dropdown_figure1', 'value')]
    )
def update_figure1(graphic_type, x_axis, y_axis):
    """
    Retourne un graphique avec les axes selectionnés.

    Args:
        type: le type du graphique (nuage de points ou histogramme)
        x_axis: valeur de l'abscisse
        y_axis: valeur de l'ordonnée
    """
    if graphic_type == 'Nuage':
        nuage = px.scatter(france, x=x_axis,y=y_axis)
        nuage.layout.xaxis.title = Nom_colonnes[x_axis]
        nuage.layout.yaxis.title = Nom_colonnes[y_axis]
        return nuage
    if graphic_type == 'Histogramme':
        histogram = px.histogram(france, x=x_axis,y=y_axis)
        histogram.layout.xaxis.title = Nom_colonnes[x_axis]
        histogram.layout.yaxis.title = Nom_colonnes[y_axis]
        return histogram

    print('type error')
    return 'type error'


@app.callback(
    dash.dependencies.Output('histogram_brand', 'figure'),
    [dash.dependencies.Input('year_dropdown_historgram_brand', 'value')]
    )
def update_histogram(input_value):
    """
    Retourne l'histogramme en fonction de l'année.

    Args:
        input_value: l'année
    """
    if input_value is None:
        histogram = px.histogram(france, x='panneaux_marque',y='nb_panneaux')
        histogram.layout.xaxis.title = "marque du panneau"
        histogram.layout.yaxis.title = "nombre de panneaux installés"
        histogram.update_xaxes(categoryorder="total descending")
        return histogram

    constructeur_an_df = france[france.an_installation == input_value]
    histogram = px.histogram(constructeur_an_df, x='panneaux_marque',y='nb_panneaux')
    histogram.layout.xaxis.title = "marque du panneau"
    histogram.layout.yaxis.title = "nombre de panneaux installés"
    histogram.update_xaxes(categoryorder="total descending")

    return histogram

@app.callback(
    dash.dependencies.Output('scatter_pente_orientation_title', 'children'),
    [dash.dependencies.Input('scatter_pente_orientation_dropdown', 'value')]
    )
def update_scatter_pente_title(dropdown_value):
    """
    Retourne le titre du graphique
    Args:
        dropdown_value: valeur du menu déroulant
    """
    if dropdown_value == 'pente':
        return 'Comparaison entre la pente optimum et la pente actuelle'

    if dropdown_value == 'orientation':
        return 'Comparaison entre la orientation optimum et la orientation actuelle'

    print('type error')
    return 'type error'

@app.callback(
    dash.dependencies.Output('scatter_pente_orientation', 'figure'),
    [dash.dependencies.Input('scatter_pente_orientation_dropdown', 'value')]
    )
def update_scatter_pente(input_value):
    """
    Retourne un nuage de points en fonction de la valeur du menu déroulant

    Args:
        input_value: pente ou orientation
    """
    if input_value == 'pente':
        figure_pente = px.scatter(france, x='id',y=['pente','pente_optimum'])
        figure_pente.layout.yaxis.title = Nom_colonnes['pente']
        return figure_pente

    if input_value == 'orientation':
        orientation_pente = px.scatter(france, x='id',y=['orientation','orientation_optimum'])
        orientation_pente.layout.yaxis.title = Nom_colonnes['orientation']
        return orientation_pente

    print('type error')
    return 'type error'

app.run_server(debug=False)
