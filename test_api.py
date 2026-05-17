import requests

# L'adresse pour récupérer les ÉQUIPES
url = "https://v3.football.api-sports.io/teams"

# On demande la Coupe du Monde Homme (league 1) pour l'année 2026
querystring = {"league": "1", "season": "2022"}

headers = {
    "x-apisports-key": "416d2747169fbdfe930be165152be272" # Ta clé API
}

print("Interrogation de l'API pour les équipes de la Coupe du Monde 2026...")

response = requests.get(url, headers=headers, params=querystring)
data = response.json()
print("RÉPONSE BRUTE DE L'API :", data)
# On vérifie combien d'équipes l'API a trouvé
nb_equipes = data['results']
print(f"\nSuccès ! {nb_equipes} équipes trouvées pour 2022 :\n")

# On affiche chaque équipe avec le lien de son drapeau
for item in data['response']:
    equipe = item['team']
    nom = equipe['name']
    drapeau = equipe['logo'] # C'est le lien magique de l'image !
    print(f"- {nom} | Drapeau : {drapeau}")