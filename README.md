Projet Python Data_Viz sur l'a production photovoltaïque en France
Réalisé par Erwan Sangchanmahola et Olivier Troissant
Cadre d'étude : ESIEE Paris
Version de python utilisé: 3.7
Données utilisées : https://www.data.gouv.fr/fr/datasets/donnees-sur-les-installations-photovoltaique-en-france-et-quelques-pays-europeens/

Rapport d'analyse:

Où en est le photovoltaïque Français ?

Ce projet à pour but de globaliser les données francaises du photovoltaïque et avec cette vue d'ensemble de passer au crible les éléments cruciaux de la production d'éléctricité solaire
Constitué de 8 graphiques et cartes divers il permete de mettre en lumière les points clés de ce domaine.

Le 1er graphe bien que personnalisable à souhait montre dans un 1er temps le pic d'installation flagrant 
l'essor du photovoltaïque en france: A partir des années 2008 pour un "age d'or" en 2010-2011 avec plus de 100k d'installations'

Le 2ème 

Sue la projection qui compare la pente optimum et la pente réellement utilisée,
on remarque que les panneaux solaire sont majoritairement installée de façon non optimale (orientation/pente).

La projection polaire nous permet également de vérifier une production plus importante des panneaux orientés vers le sud,
mais également que c'est un phènomène connu puisque la majorité des installation sont comprise dans le cadran 90°-270° autremeent dit orienté vers le sud



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
