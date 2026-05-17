import requests
import sqlite3
from datetime import datetime

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# On interroge l'API pour les Fixtures (Matchs) de la Coupe du Monde (League 1)
url = "https://v3.football.api-sports.io/fixtures"
querystring = {"league": "1", "season": "2022"} # <-- Tu changeras ça en 2026 le moment venu !
headers = {
    "x-apisports-key": "416d2747169fbdfe930be165152be272" # Ta clé API
}

print("Téléchargement des 64 matchs en cours...")
response = requests.get(url, headers=headers, params=querystring)
data = response.json()

# On vide la table Matchs de tes anciens tests pour faire propre
cursor.execute("DELETE FROM Matchs")

# On boucle sur les 64 matchs renvoyés par l'API
for item in data['response']:
    fixture = item['fixture']
    teams = item['teams']
    league = item['league']

    # 1. SAUVEGARDE DES ÉQUIPES ET DES DRAPEAUX
    home = teams['home']
    away = teams['away']
    cursor.execute("INSERT OR IGNORE INTO Equipes (id, nom_pays, logo) VALUES (?, ?, ?)", (home['id'], home['name'], home['logo']))
    cursor.execute("INSERT OR IGNORE INTO Equipes (id, nom_pays, logo) VALUES (?, ?, ?)", (away['id'], away['name'], away['logo']))

    # 2. Gestion de la Date et de l'Heure
    date_obj = datetime.fromisoformat(fixture['date'].replace('Z', '+00:00'))
    date_str = date_obj.strftime('%Y-%m-%d')
    heure_str = date_obj.strftime('%H:%M')

    # 3. Traduction des Phases
    phase = league['round']
    phase = phase.replace('Group Stage - ', 'Journée ')
    phase = phase.replace('Round of 16', 'Huitièmes de finale')
    phase = phase.replace('Quarter-finals', 'Quarts de finale')
    phase = phase.replace('Semi-finals', 'Demi-finales')
    phase = phase.replace('Final', 'Finale')
    phase = phase.replace('3rd Phase', 'Petite finale')

    # 4. Insertion du Match
    cursor.execute('''INSERT INTO Matchs (id_equipe1, id_equipe2, date, heure, phase, statut)
                      VALUES (?, ?, ?, ?, ?, 'En attente')''',
                   (home['id'], away['id'], date_str, heure_str, phase))

conn.commit()
conn.close()
print("Succès ! Les 64 matchs officiels sont enregistrés dans ta base de données.")
