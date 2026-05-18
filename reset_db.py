import sqlite3
import os
from werkzeug.security import generate_password_hash

print("🧹 Nettoyage en cours...")

# 1. Supprimer l'ancienne base
if os.path.exists('database.db'):
    os.remove('database.db')
    print("🗑️ Ancienne base supprimée.")

# 2. Créer la nouvelle base avec le fichier schema.sql
conn = sqlite3.connect('database.db')
with open('schema.sql', 'r', encoding='utf-8') as f:
    conn.executescript(f.read())

# 3. Ajouter des joueurs avec Vrais Noms / Prénoms
print("👤 Création des joueurs avec Noms et Prénoms...")
joueurs = [
    ("Mbappé", "Kylian", "Kiki", "kylian@esme.fr", "mdp123", 36),
    ("Renard", "Wendie", "CaptainW", "wendie@esme.fr", "mdp123", 31),
    ("Griezmann", "Antoine", "Grizou", "antoine@esme.fr", "mdp123", 30),
    ("Zidane", "Zinédine", "Zizou", "zinedine@esme.fr", "mdp123", 26)
]

for j in joueurs:
    conn.execute('''
        INSERT INTO Utilisateurs (nom, prenom, pseudo, email, mot_de_passe_hash, points_totaux)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (j[0], j[1], j[2], j[3], generate_password_hash(j[4]), j[5]))

# 4. Recréer le compte Administrateur
conn.execute('''
    INSERT INTO Utilisateurs (nom, prenom, pseudo, email, mot_de_passe_hash) 
    VALUES (?, ?, ?, ?, ?)
''', ('Admin', 'ESME', 'Admin', 'admin@esme.fr', generate_password_hash('admin123')))

conn.commit()
conn.close()

print("✅ Base de données recréée à NEUF avec les nouveaux joueurs !")