import asyncio
import aiohttp
from pymongo import MongoClient
import time

# URL de l'API Vélib'
API_URL = "https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/velib-disponibilite-en-temps-reel/records"

# Fonction asynchrone pour récupérer les données des stations Vélib'
async def fetch_data():
    params = {'limit': 100, 'offset': 0}
    try:
        # Créer une session HTTP asynchrone
        async with aiohttp.ClientSession() as session:
            # Effectuer une requête GET à l'API avec les paramètres
            async with session.get(API_URL, params=params) as response:
                if response.status == 200:
                    # Convertir la réponse en JSON
                    data = await response.json()
                    # Vérifier si la clé 'results' existe et contient une liste
                    if 'results' in data and isinstance(data['results'], list):
                        return data['results']
                    else:
                        print("Aucune donnée valide dans 'results'.")
                        return []
                else:
                    print(f"Erreur API: {response.status}")
                    return []
    except Exception as e:
        # Gestion des erreurs
        print(f"Erreur lors de la récupération des données : {e}")
        return []

# Fonction pour insérer les données dans MongoDB
def insert_data(data):
    try:
        # Connexion à la base de données MongoDB
        client = MongoClient("mongodb://localhost:27017/")
        db = client["velib_data"]
        collection = db["stations"]

        if data:
            # Supprimer les anciennes données
            collection.delete_many({})
            # Insérer les nouvelles données
            result = collection.insert_many(data)
            print(f"{len(result.inserted_ids)} documents insérés.")
        else:
            print("Aucune donnée à insérer.")
    except Exception as e:
        # Gestion des erreurs
        print(f"Erreur lors de l'insertion dans MongoDB : {e}")

# Fonction asynchrone principale pour exécuter les tâches en boucle
async def main():
    while True:
        print("Récupération des données...")
        # Appeler la fonction de récupération des données
        stations = await fetch_data()
        # Insérer les données récupérées dans MongoDB
        insert_data(stations)

        print("Attente de 1 minute avant le prochain rafraîchissement...")
        # Attendre 60 secondes avant le prochain cycle
        await asyncio.sleep(60)

# Fonction pour démarrer la boucle événementielle asynchrone
def run():
    try:
        # Démarrer la boucle asynchrone
        asyncio.run(main())
    except KeyboardInterrupt:
        # Gestion de l'interruption par l'utilisateur
        print("Exécution interrompue par l'utilisateur.")

if __name__ == "__main__":
    run()
