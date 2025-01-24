import requests
import folium

# URL de l'API
API_URL = "https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/velib-disponibilite-en-temps-reel/records"

# Paramètres de la requête pour limiter le nombre de résultats
params = {'limit': 100, 'offset': 0}
# Récupération des données depuis l'API
response = requests.get(API_URL, params=params)
if response.status_code == 200:
    data = response.json()
    # Inspection de la structure des données pour mieux comprendre le format
    print(data)
else:
    print("Erreur lors de la récupération des données :", response.status_code)
    data = {"records": []}  # Valeur par défaut en cas d'échec de l'API

# Initialisation de la carte Folium centrée sur Paris
paris_map = folium.Map(location=[48.8566, 2.3522], zoom_start=13)

# Parcours des stations dans les résultats
i = 0
print("results", len(data.get("results", [])))
for record in data.get("results", []):
    # Certaines clés peuvent être imbriquées dans 'fields'
    station_name = record.get("name", "Station inconnue")  # Nom de la station ajusté
    print("station_name",station_name)
    capacity = record.get("capacity", 0)
    num_bikes = record.get("numbikesavailable", 0)
    mechanical_bikes = record.get("mechanical", 0)
    ebikes = record.get("ebike", 0)
    geo_coordinates = record.get("coordonnees_geo", None)  # Coordonnées géographiques
    print(geo_coordinates)

    # Vérification si les coordonnées sont valides (si c'est un dictionnaire)
    if geo_coordinates and isinstance(geo_coordinates, dict):
        lat = geo_coordinates.get("lat")
        lon = geo_coordinates.get("lon")

        # Vérifier que les deux coordonnées existent
        if lat is not None and lon is not None:
            # Création du contenu du popup
            popup_content = f"""
            <b>{station_name}</b><br>
            Capacité : {capacity}<br>
            Vélos disponibles : {num_bikes}<br>
            Vélos mécaniques : {mechanical_bikes}<br>
            Vélos électriques : {ebikes}<br>
            """
            print(popup_content)
            # Ajout d'un marqueur pour chaque station sur la carte
            folium.Marker(
                location=[lat, lon],
                popup=popup_content,
                icon=folium.Icon(color="blue", icon="bicycle")
            ).add_to(paris_map)
        else:
            print(f"Coordonnées manquantes pour la station : {station_name}")
    else:
        # Affichage des stations avec coordonnées manquantes ou mal formatées
        print(f"Station sans coordonnées valides : {station_name}, Données complètes : {record}")

# Enregistrement de la carte dans un fichier HTML
paris_map.save("velib_station_map.html")
print("Carte générée : ouvrez le fichier 'velib_station_map.html' dans un navigateur.")
