import sqlite3
import random
from werkzeug.security import generate_password_hash

def seed_database():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    print("Création des utilisateurs fictifs...")
    utilisateurs_fictifs = [
        ('antoine.griezmann@esme.fr', 'password123', 15),
        ('kylian.mbappe@esme.fr', 'password123', 28),
        ('olivier.giroud@esme.fr', 'password123', 10),
        ('hugo.lloris@esme.fr', 'password123', 5),
        ('didier.deschamps@esme.fr', 'password123', 35)
    ]
    
    for email, pw, points in utilisateurs_fictifs:
        try:
            cursor.execute('INSERT INTO Utilisateurs (email, mot_de_passe_hash, points_totaux) VALUES (?, ?, ?)', 
                           (email, generate_password_hash(pw), points))
        except sqlite3.IntegrityError:
            pass # L'utilisateur existe déjà

    print("Création de matchs de poule d'exemple...")
    matchs = [
        (1, 2, '2026-06-11', '21:00', 'Groupe A'), # France vs Maroc (IDs fictifs basés sur ton schema)
        (3, 4, '2026-06-12', '18:00', 'Groupe A'),
        (5, 6, '2026-06-13', '15:00', 'Groupe B'),
        (7, 8, '2026-06-13', '21:00', 'Groupe B')
    ]
    
    for m in matchs:
        # Vérifie si le match existe pour ne pas le créer en double
        cursor.execute('SELECT id FROM Matchs WHERE id_equipe1=? AND id_equipe2=?', (m[0], m[1]))
        if not cursor.fetchone():
            cursor.execute('INSERT INTO Matchs (id_equipe1, id_equipe2, date, heure, phase) VALUES (?, ?, ?, ?, ?)', m)

    conn.commit()
    conn.close()
    print("Succès : Base de données remplie avec des données fictives !")

if __name__ == '__main__':
    seed_database()