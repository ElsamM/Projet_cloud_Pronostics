import sqlite3
import os

print("🧹 Nettoyage en cours...")

# 1. Supprimer l'ancienne base corrompue
if os.path.exists('database.db'):
    os.remove('database.db')
    print("🗑️ Ancienne base supprimée.")

# 2. Créer la nouvelle base avec le fichier schema.sql
conn = sqlite3.connect('database.db')
with open('schema.sql', 'r', encoding='utf-8') as f:
    conn.executescript(f.read())
conn.close()

print("✅ Base de données recréée à NEUF avec la colonne pseudo !")