# TP 1 

Ce TP permet de récupérer les données en temps réel des stations Vélib' via l'API et de les insérer dans une base de données MongoDB. Les données sont mises à jour toutes les minutes pour garantir leur fraîcheur.

## Fonctionnalités

- **Récupération des données des stations Vélib'** : Le projet interroge l'API pour récupérer les informations des stations Vélib' en temps réel.
- **Insertion dans MongoDB** : Les données récupérées sont stockées dans une base de données MongoDB afin d'être facilement consultées et analysées.
- **Mise à jour périodique** : Les données sont mises à jour toutes les minutes, garantissant qu'elles sont toujours à jour.
# TP 2

Ce TP interroge l'API pour récupérer des informations sur les stations Vélib'. Il affiche une carte interactive à l'aide de la bibliothèque Python **Folium**, où chaque station est représentée par un marqueur. Lorsque l'utilisateur clique sur un marqueur, un **popup** contenant des informations détaillées sur la station s'affiche.

Les informations affichées dans le popup incluent :

- **Nom de la station** : Le nom de la station Vélib'.
- **Capacité** : Le nombre total de vélos que la station peut accueillir.
- **Vélos disponibles** : Le nombre de vélos disponibles à la station.
- **Vélos mécaniques** : Le nombre de vélos mécaniques disponibles.
- **Vélos électriques** : Le nombre de vélos électriques disponibles.

# TP 3

Ce TP a pour objectif de récupérer les données les plus récentes des stations Vélib' depuis une base de données MongoDB et de les afficher sur une carte interactive à l'aide de **Folium**. Chaque station est marquée sur la carte avec des informations détaillées telles que :

- **Nom de la station**
- **Capacité de la station**
- **Nombre de vélos disponibles**
- **Nombre de vélos mécaniques et électriques**
- **Date de mise à jour**

La carte est ensuite sauvegardée en format HTML et peut être ouverte dans n'importe quel navigateur web.

# TP 4 

Cette application permet de rechercher les stations Vélib' à proximité d'une adresse donnée (moins de 500 mètres) qui possèdent des vélos disponibles. Elle utilise **Flask** pour l'interface web, **MongoDB** pour récupérer les informations sur les stations Vélib', et **Folium** pour générer une carte interactive affichant la position de l'utilisateur et les stations proches.

## Fonctionnalités

1. **Géocodage d'adresse** : L'application convertit une adresse en coordonnées géographiques (latitude, longitude) via **Geopy**.
2. **Recherche de stations Vélib'** : Recherche des stations Vélib' dans une base de données MongoDB et filtre les stations situées à moins de 500 mètres de l'adresse fournie, avec des vélos disponibles.
3. **Carte interactive** : Génération d'une carte interactive avec **Folium** pour afficher la position de l'utilisateur et les stations Vélib' à proximité.
4. **Affichage des résultats** : La liste des stations proches est affichée avec les informations suivantes :
   - Nom de la station
   - Capacité de la station
   - Nombre de vélos disponibles
   - Distance par rapport à l'utilisateur
















