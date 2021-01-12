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
#remove 0 surface
df=df[df.surface != 0]
df=df[df.surface < 5000]

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
print('================================')
print(france["surface"])
#




if __name__ == '__main__':

    app = dash.Dash(__name__) # (3)

    
    fig1 = px.scatter(france, x="surface", y="production_pvgis",
                        color="orientation",
                        size="nb_panneaux",
                        hover_name="nb_panneaux",
) # (4)

    fig2 = px.scatter(france, y="surface", x="production_pvgis") # (4)
    app.layout = html.Div(children= ([

                            html.H1(children=f'Production des panneaux solaires en fonction de la surface',
                                        style={'textAlign': 'center', 'color': '#7FDBFF'}), # (5)

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

                            dcc.Graph(
                                id='graph2',
                                figure=fig2,

                            ), # (6)

                 html.Div(children=f'''
                                The graph above shows relationship between life expectancy and
                                GDP per capita for year . Each continent data has its own
                                colour and symbol size is proportionnal to country population.
                                Mouse over for details.'''), # (7)
                           

                ]))
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