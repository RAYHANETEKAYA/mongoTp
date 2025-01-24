import requests
import folium
from pymongo import MongoClient
from datetime import datetime

# Connexion à MongoDB
client = MongoClient("mongodb://localhost:27017/")  # Remplacez par votre URL de connexion MongoDB
db = client['velib_data']  # Remplacez par le nom de votre base de données
collection = db['stations']  # Remplacez par le nom de votre collection

# Récupération des données les plus récentes par date
recent_data = collection.find().sort("duedate", -1)  # Trie par date décroissante

# Initialisation de la carte Folium centrée sur Paris
paris_map = folium.Map(location=[48.8566, 2.3522], zoom_start=13)

# Parcours des stations dans les résultats de MongoDB
i = 0
for record in recent_data:

    # Extraction des champs pertinents
    station_name = record.get("name", "Station inconnue")
    capacity = record.get("capacity", 0)
    num_bikes = record.get("numbikesavailable", 0)
    mechanical_bikes = record.get("mechanical", 0)
    ebikes = record.get("ebike", 0)
    geo_coordinates = record.get("coordonnees_geo", None)  # Coordonnées géographiques
    duedate = record.get("duedate", "Date inconnue")

    # Affichage de la date de mise à jour
    print(f"Date de mise à jour : {duedate}")

    # Vérification si les coordonnées sont valides (si c'est un dictionnaire)
    if geo_coordinates and isinstance(geo_coordinates, dict):
        lat = geo_coordinates.get("lat")
        lon = geo_coordinates.get("lon")

        # Vérifier que les deux coordonnées existent
        if lat is not None and lon is not None:
            # Création du contenu du popup avec les informations de la station
            popup_content = f"""
            <b>{station_name}</b><br>
            Capacité : {capacity}<br>
            Vélos disponibles : {num_bikes}<br>
            Vélos mécaniques : {mechanical_bikes}<br>
            Vélos électriques : {ebikes}<br>
            Mise à jour : {duedate}<br>
            """
            print(popup_content)
            # Ajout d'un marqueur pour chaque station sur la carte
            folium.Marker(
                location=[lat, lon],
                popup=popup_content,
                icon=folium.Icon(color="blue", icon="bicycle")
            ).add_to(paris_map)
        else:
            # Si les coordonnées sont manquantes, affichage d'un message
            print(f"Coordonnées manquantes pour la station : {station_name}")
    else:
        # Affichage des stations avec coordonnées manquantes ou mal formatées
        print(f"Station sans coordonnées valides : {station_name}, Données complètes : {record}")

# Enregistrement de la carte dans un fichier HTML
paris_map.save("velib_station_mongo.html")
print("Carte générée : ouvrez le fichier 'velib_station_map_mongo.html' dans un navigateur.")
