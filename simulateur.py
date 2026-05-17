import sqlite3
import random
from werkzeug.security import generate_password_hash

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

print("🚀 Démarrage de la simulation du TP avec Pseudos...")

# 1. Création de faux utilisateurs avec des PSEUDOS stylés
faux_users = [
    ('Zizou_Le_Boss', 'zizou@esme.fr'),
    ('PronoMaster_26', 'master@esme.fr'),
    ('TacticienDuDimanche', 'tacticien@esme.fr'),
    ('Kiki_Mbappe_Fan', 'kiki@esme.fr'),
    ('Le_Gourou_Des_Scores', 'gourou@esme.fr')
]

for pseudo, email in faux_users:
    try:
        # On donne des points aléatoires pour avoir un beau classement
        points = random.randint(10, 45)
        cursor.execute('INSERT INTO Utilisateurs (pseudo, email, mot_de_passe_hash, points_totaux) VALUES (?, ?, ?, ?)',
                       (pseudo, email, generate_password_hash('password123'), points))
    except sqlite3.IntegrityError:
        pass # Ignore si le faux joueur existe déjà

print("✅ Faux utilisateurs générés pour le classement.")

# 2. Simulation de la phase de groupes (Générer des scores aléatoires)
# On récupère tous les matchs de groupes de 2026
matchs_poules = cursor.execute("SELECT id FROM Matchs WHERE phase LIKE '%Journée%' OR phase LIKE '%Group%'").fetchall()

for m in matchs_poules:
    score1 = random.randint(0, 4)
    score2 = random.randint(0, 4)
    cursor.execute('''UPDATE Matchs 
                      SET vrai_score_eq1 = ?, vrai_score_eq2 = ?, statut = 'Terminé' 
                      WHERE id = ?''', (score1, score2, m[0]))

conn.commit()
conn.close()
print(f"✅ {len(matchs_poules)} matchs de poules terminés avec succès !")
print("🏆 Va voir la page Classement, tu auras de beaux pseudos maintenant !")