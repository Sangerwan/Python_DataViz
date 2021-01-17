Projet Python Data_Viz sur l'a production photovoltaïque en France
Réalisé par Erwan Sangchanmahola et Olivier Troissant
Cadre d'étude : ESIEE Paris
Version de python utilisé: 3.7
Données utilisées : https://www.data.gouv.fr/fr/datasets/donnees-sur-les-installations-photovoltaique-en-france-et-quelques-pays-europeens/

Rapport d'analyse:

On remarque que les panneaux solaire sont majoritairement installée de façon non optimale (orientation/pente).
On constate tout de même une production plus importante des panneaux orientés vers le sud


User Guide:

L'application repose sur plusieurs modules qu'ils faudra importer avant de la lancer.
Une fois l'application python exécutée, un dashboard est créé à l'adresse http://127.0.0.1:8050/
Le dashboard permet de visualiser les données présentes dans la base de donnée.
Plusieurs intéractions sont possibles a travers des boutons, menu déroulant, ...

Développer Guide:

Le code se structure de la manière suivante:
  -une base de donnée pandas
  -une application web dash avec ses fonctions
  
 L'architecture dash étant facilement modulable il est facile de modifier des éléments, pour plus d'information voir la documentation des modules utilisés: 
 
https://plotly.com/dash/
https://plotly.com/python/plotly-express/
https://pandas.pydata.org/
