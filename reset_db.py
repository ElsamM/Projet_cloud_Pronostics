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

# 3. Recréer le compte Administrateur (Obligatoire pour gérer le site)
conn.execute('''
    INSERT INTO Utilisateurs (nom, prenom, pseudo, email, mot_de_passe_hash) 
    VALUES (?, ?, ?, ?, ?)
''', ('Admin', 'ESME', 'Admin', 'admin@esme.fr', generate_password_hash('admin123')))

conn.commit()
conn.close()

print("✅ Base de données recréée à NEUF, prête pour les vrais joueurs !")