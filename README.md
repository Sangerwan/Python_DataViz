Projet Python Data_Viz sur l'a production photovoltaïque en France
Réalisé par Erwan Sangchanmahola et Olivier Troissant
Cadre d'étude : ESIEE Paris
Version de python utilisé: 3.7
Données utilisées : https://www.data.gouv.fr/fr/datasets/donnees-sur-les-installations-photovoltaique-en-france-et-quelques-pays-europeens/

Rapport d'analyse:

Où en est le photovoltaïque Français ?

Ce projet à pour but de globaliser les données francaises du photovoltaïque et avec cette vue d'ensemble de passer au crible les éléments cruciaux de la production d'éléctricité solaire
Constitué de 8 graphiques et cartes divers, il permet de mettre en lumière les points clés de ce domaine.

Le premier graphe, bien que personnalisable à souhait, montre dans un premier temps un pic d'installation flagrant.
l'essor du photovoltaïque en france: A partir des années 2008 pour un "age d'or" en 2010-2011 avec plus de 100k d'installations'

Le 2ème permet un rapide aperçu des constructeurs dominants le marché à différentes années :
ce que l'on retient :
	une domination de "BPSolar" jusqu'à 2005.
	puis une succession de nouveaux constructeurs, forte concurrence.
	et enfin on retient notament "colas" qui devance largement en 2016 avec plus de 2500 installations; derrière se trouve "Solar World" avec moins du double.


Ensuite vient la projection qui compare la pente optimum et la pente réellement utilisée.
On remarque que les panneaux solaire sont majoritairement installée de façon non optimale (orientation/pente).
Ce graphique dresse la même constatation avec l'orientation (possibilité de selectionner en dessous la donnée à comparer).

La projection polaire nous permet de vérifier une production plus importante des panneaux orientés vers le sud,
mais également que c'est un phènomène connu puisque la majorité des installation sont comprise dans le cadran 90°-270° autrement dit orienté Sud.

"La production selon la localisation ou la pente" Il est également intéressant de noter la répartition (en fonction de la surface réglable grâce au range slider)
des installations en france et de comparer le ratio production/surface, on voit ici que le coté méditerranéen au sud profite largement d'un bon rendement,
c'est aussi le cas sur le reste du littoral avec moins d'importance, le nord et l'est sont par contre à une moyenne plus basse
Cette carte de rendement est très interressante de pars son rapprochement avec la durée d'ensoleillement la similitude est ainsi flagrante

Enfin pour complèter cette analyse rendement nous avons le graphe (aussi en fonction de la surface) qui permet de visualiser la pente idéal en la comparant avec la couleur la plus chaude
Ainsi, il apparait qu'une pente optimum moyenne serait comprise entre 25° et 35°.

Les deux derniers sont moins lisible 
le graph en violon représente (pour chaque année selectionnée) la valeur moyenne des rendements des installations, il permet ainsi de comparer les moyennes de rendement entre chaque année
on observe que ce rendement tant a augmenter quasi-constamment
Enfin la carte est intéressante pour situer précisement la répartition des installations, il est possivle de sélectionner plusieurs années et également les constructeurs
ce que l'ont peut remarquer: une concentration forte d'installation sur le littoral  mais également autour des grandes aglomérations, les fameuses "diagonales du vide" sont bien visibles ici.



User Guide:

L'application repose sur plusieurs modules (zipfile37, numpy, pandas, dash, plotly_express) qu'il faudra installer avec pip install.
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
