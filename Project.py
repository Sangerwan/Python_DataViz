import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import dash
import os

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
france = france[france.surface!=8388607]

print(surface.unique())
#
# Data
#

france
production
surface


#


if __name__ == '__main__':

    app = dash.Dash(__name__) # (3)

    fig = px.scatter(france, x="surface", y="production_pvgis",
                        color="orientation",
                        size="nb_panneaux",
                        hover_name="nb_panneaux") # (4)


    app.layout = html.Div(children= ([

                            html.H1(children=f'Life expectancy vs GDP per capita ({surface})',
                                        style={'textAlign': 'center', 'color': '#7FDBFF'}), # (5)

                            dcc.Graph(
                                id='graph2',
                                figure=fig,

                            ), # (6)

                            html.Div(children=f'''
                                The graph above shows relationship between life expectancy and
                                GDP per capita for year . Each continent data has its own
                                colour and symbol size is proportionnal to country population.
                                Mouse over for details.
                            ''') # (7)

                            

    ],[

                            html.H2(children=f'Life expectancy vs GDP per capita ({surface})',
                                        style={'textAlign': 'center', 'color': '#7FDBFF'}), # (5)

                            dcc.Graph(
                                id='graph1',
                                figure=fig,

                            ) # (6)

                            

                            

    ]
                                    
                                    
                                    
                                    
                                    )
    )

    #
    # RUN APP
    #

    app.run_server(debug=False) # (8)