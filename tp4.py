from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import folium

# Connexion à MongoDB
client = MongoClient("mongodb://localhost:27017/")  # Remplacez par l'URL de connexion MongoDB
db = client['velib_data']  # Accès à la base de données 'velib_data'
collection = db['stations']  # Accès à la collection 'stations' où les données des stations sont stockées

# Initialisation de l'application Flask
app = Flask(__name__)

# Fonction pour géocoder une adresse (convertir une adresse en coordonnées géographiques)
def geocode_address(address):
    geolocator = Nominatim(user_agent="velib_app")  # Initialisation du géocodeur Nominatim avec un user-agent spécifique
    location = geolocator.geocode(address)  # Géocodage de l'adresse
    if location:  # Si l'adresse est valide et a pu être géocodée
        return (location.latitude, location.longitude)  # Retourne les coordonnées géographiques (latitude, longitude)
    return None  # Si l'adresse est invalide, retourne None

# Route principale pour afficher la page d'accueil
@app.route('/')
def home():
    return render_template('index.html')  # Rendu de la page d'accueil (index.html)

# Endpoint pour rechercher les stations proches de l'utilisateur
@app.route('/search', methods=['POST'])
def search():
    # Récupérer les données JSON envoyées dans la requête POST
    data = request.json
    address = data.get("address")  # Adresse de l'utilisateur envoyée dans la requête
    # Géocoder l'adresse de l'utilisateur pour obtenir ses coordonnées géographiques
    user_coords = geocode_address(address)
    if not user_coords:  # Si l'adresse est invalide
        return jsonify({"error": "Adresse invalide."}), 400  # Retourne une erreur 400 avec message

    # Récupérer les stations avec des vélos dans MongoDB
    stations = collection.find({"ebike": {"$gt": 0}})  # Filtrer les stations ayant des vélos
    nearby_stations = []  # Liste pour stocker les stations proches de l'utilisateur

    # Parcours des stations pour vérifier si elles sont proches de l'utilisateur
    for station in stations:
        geo_coordinates = station.get("coordonnees_geo", {})  # Récupérer les coordonnées géographiques de la station
        station_coords = (geo_coordinates.get("lat"), geo_coordinates.get("lon"))  # Extraire latitude et longitude

        # Vérifier si les coordonnées de la station sont valides
        if station_coords[0] is not None and station_coords[1] is not None:
            # Calculer la distance entre l'utilisateur et la station en mètres
            distance = geodesic(user_coords, station_coords).meters
            if distance <= 500:  # Si la station est à moins de 500 mètres
                # Ajouter la station à la liste des stations proches
                nearby_stations.append({
                    "name": station.get("name", "Station inconnue"),  # Nom de la station
                    "distance": round(distance, 2),  # Distance à la station en mètres
                    "capacity": station.get("capacity", 0),  # Capacité de la station
                    "numbikesavailable": station.get("numbikesavailable", 0),  # Nombre de vélos disponibles
                    "ebike": station.get("ebike", 0),  # Nombre de vélos disponibles
                    "lat": station_coords[0],  # Latitude de la station
                    "lon": station_coords[1],  # Longitude de la station
                })

    # Générer une carte avec Folium centrée sur la position de l'utilisateur
    folium_map = folium.Map(location=user_coords, zoom_start=15)  # Initialiser la carte à la position de l'utilisateur
    folium.Marker(user_coords, popup="Votre position", icon=folium.Icon(color="red")).add_to(folium_map)  # Ajouter un marqueur pour la position de l'utilisateur

    # Ajouter les stations proches à la carte
    for station in nearby_stations:
        popup_content = f"""
        <b>{station['name']}</b><br>
        Distance : {station['distance']} m<br>
        Capacité : {station['capacity']}<br>
        Vélos  disponibles : {station['ebike']}<br>
        """
        # Ajouter un marqueur pour chaque station proche
        folium.Marker(
            location=[station['lat'], station['lon']],  # Position du marqueur
            popup=popup_content,  # Contenu du popup avec détails sur la station
            icon=folium.Icon(color="blue", icon="bicycle")  # Icône pour le marqueur (bicyclette bleue)
        ).add_to(folium_map)

    # Enregistrer la carte générée sous forme de fichier HTML dans le dossier templates
    map_file = "templates/map.html"
    folium_map.save(map_file)  # Sauvegarder la carte dans le fichier map.html

    # Retourner les stations proches avec leur information et l'URL de la carte générée
    return jsonify({"stations": nearby_stations, "map_url": "/map"})

# Route pour afficher la carte générée
@app.route('/map')
def show_map():
    return render_template('map.html')  # Rendu de la carte (map.html) à partir du fichier généré

# Exécution de l'application Flask en mode debug (serveur de développement)
if __name__ == '__main__':
    app.run(debug=True)
