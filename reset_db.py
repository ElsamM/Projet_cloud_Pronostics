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

# 4. Injecter les 104 matchs de la Coupe du Monde 2026
print("⚽ Création du calendrier COMPLET des 104 matchs...")

# Réinitialiser les IDs de la table Matchs pour être sûr que le premier match est ID=1
conn.execute("DELETE FROM sqlite_sequence WHERE name='Matchs'") 

DRAPEAUX = {
    "Mexique": "https://flagcdn.com/w80/mx.png", "Afrique du Sud": "https://flagcdn.com/w80/za.png", "République de Corée": "https://flagcdn.com/w80/kr.png", "Tchéquie": "https://flagcdn.com/w80/cz.png",
    "Canada": "https://flagcdn.com/w80/ca.png", "Bosnie-et-Herzégovine": "https://flagcdn.com/w80/ba.png", "Qatar": "https://flagcdn.com/w80/qa.png", "Suisse": "https://flagcdn.com/w80/ch.png",
    "Brésil": "https://flagcdn.com/w80/br.png", "Maroc": "https://flagcdn.com/w80/ma.png", "Haïti": "https://flagcdn.com/w80/ht.png", "Écosse": "https://flagcdn.com/w80/gb-sct.png",
    "États-Unis": "https://flagcdn.com/w80/us.png", "Paraguay": "https://flagcdn.com/w80/py.png", "Australie": "https://flagcdn.com/w80/au.png", "Turquie": "https://flagcdn.com/w80/tr.png",
    "Allemagne": "https://flagcdn.com/w80/de.png", "Curaçao": "https://flagcdn.com/w80/cw.png", "Côte d'Ivoire": "https://flagcdn.com/w80/ci.png", "Équateur": "https://flagcdn.com/w80/ec.png",
    "Pays-Bas": "https://flagcdn.com/w80/nl.png", "Japon": "https://flagcdn.com/w80/jp.png", "Suède": "https://flagcdn.com/w80/se.png", "Tunisie": "https://flagcdn.com/w80/tn.png",
    "Belgique": "https://flagcdn.com/w80/be.png", "Égypte": "https://flagcdn.com/w80/eg.png", "RI Iran": "https://flagcdn.com/w80/ir.png", "Nouvelle-Zélande": "https://flagcdn.com/w80/nz.png",
    "Espagne": "https://flagcdn.com/w80/es.png", "Cap-Vert": "https://flagcdn.com/w80/cv.png", "Arabie saoudite": "https://flagcdn.com/w80/sa.png", "Uruguay": "https://flagcdn.com/w80/uy.png",
    "France": "https://flagcdn.com/w80/fr.png", "Sénégal": "https://flagcdn.com/w80/sn.png", "Irak": "https://flagcdn.com/w80/iq.png", "Norvège": "https://flagcdn.com/w80/no.png",
    "Argentine": "https://flagcdn.com/w80/ar.png", "Algérie": "https://flagcdn.com/w80/dz.png", "Autriche": "https://flagcdn.com/w80/at.png", "Jordanie": "https://flagcdn.com/w80/jo.png",
    "Portugal": "https://flagcdn.com/w80/pt.png", "RD Congo": "https://flagcdn.com/w80/cd.png", "Ouzbékistan": "https://flagcdn.com/w80/uz.png", "Colombie": "https://flagcdn.com/w80/co.png",
    "Angleterre": "https://flagcdn.com/w80/gb-eng.png", "Croatie": "https://flagcdn.com/w80/hr.png", "Ghana": "https://flagcdn.com/w80/gh.png", "Panamá": "https://flagcdn.com/w80/pa.png"
}

calendrier = [
    # --- POULES ---
    ("Journée 1", "2026-06-11", "15:00", "Mexique", "Afrique du Sud"), ("Journée 1", "2026-06-11", "22:00", "République de Corée", "Tchéquie"),
    ("Journée 1", "2026-06-12", "15:00", "Canada", "Bosnie-et-Herzégovine"), ("Journée 1", "2026-06-12", "21:00", "États-Unis", "Paraguay"),
    ("Journée 1", "2026-06-13", "15:00", "Qatar", "Suisse"), ("Journée 1", "2026-06-13", "18:00", "Brésil", "Maroc"),
    ("Journée 1", "2026-06-13", "21:00", "Haïti", "Écosse"), ("Journée 1", "2026-06-13", "00:00", "Australie", "Turquie"),
    ("Journée 1", "2026-06-14", "13:00", "Allemagne", "Curaçao"), ("Journée 1", "2026-06-14", "16:00", "Pays-Bas", "Japon"),
    ("Journée 1", "2026-06-14", "19:00", "Côte d'Ivoire", "Équateur"), ("Journée 1", "2026-06-14", "22:00", "Suède", "Tunisie"),
    ("Journée 1", "2026-06-15", "12:00", "Espagne", "Cap-Vert"), ("Journée 1", "2026-06-15", "15:00", "Belgique", "Égypte"),
    ("Journée 1", "2026-06-15", "18:00", "Arabie saoudite", "Uruguay"), ("Journée 1", "2026-06-15", "21:00", "RI Iran", "Nouvelle-Zélande"),
    ("Journée 1", "2026-06-16", "15:00", "France", "Sénégal"), ("Journée 1", "2026-06-16", "18:00", "Irak", "Norvège"),
    ("Journée 1", "2026-06-16", "21:00", "Argentine", "Algérie"), ("Journée 1", "2026-06-16", "00:00", "Autriche", "Jordanie"),
    ("Journée 1", "2026-06-17", "13:00", "Portugal", "RD Congo"), ("Journée 1", "2026-06-17", "16:00", "Angleterre", "Croatie"),
    ("Journée 1", "2026-06-17", "19:00", "Ghana", "Panamá"), ("Journée 1", "2026-06-17", "22:00", "Ouzbékistan", "Colombie"),
    ("Journée 2", "2026-06-18", "12:00", "Tchéquie", "Afrique du Sud"), ("Journée 2", "2026-06-18", "15:00", "Suisse", "Bosnie-et-Herzégovine"),
    ("Journée 2", "2026-06-18", "18:00", "Canada", "Qatar"), ("Journée 2", "2026-06-18", "21:00", "Mexique", "République de Corée"),
    ("Journée 2", "2026-06-19", "15:00", "États-Unis", "Australie"), ("Journée 2", "2026-06-19", "18:00", "Écosse", "Maroc"),
    ("Journée 2", "2026-06-19", "20:30", "Brésil", "Haïti"), ("Journée 2", "2026-06-19", "23:00", "Turquie", "Paraguay"),
    ("Journée 2", "2026-06-20", "13:00", "Pays-Bas", "Suède"), ("Journée 2", "2026-06-20", "16:00", "Allemagne", "Côte d'Ivoire"),
    ("Journée 2", "2026-06-20", "20:00", "Équateur", "Curaçao"), ("Journée 2", "2026-06-20", "00:00", "Tunisie", "Japon"),
    ("Journée 2", "2026-06-21", "12:00", "Espagne", "Arabie saoudite"), ("Journée 2", "2026-06-21", "15:00", "Belgique", "RI Iran"),
    ("Journée 2", "2026-06-21", "18:00", "Uruguay", "Cap-Vert"), ("Journée 2", "2026-06-21", "21:00", "Nouvelle-Zélande", "Égypte"),
    ("Journée 2", "2026-06-22", "13:00", "Argentine", "Autriche"), ("Journée 2", "2026-06-22", "17:00", "France", "Irak"),
    ("Journée 2", "2026-06-22", "20:00", "Norvège", "Sénégal"), ("Journée 2", "2026-06-22", "23:00", "Jordanie", "Algérie"),
    ("Journée 2", "2026-06-23", "13:00", "Portugal", "Ouzbékistan"), ("Journée 2", "2026-06-23", "16:00", "Angleterre", "Ghana"),
    ("Journée 2", "2026-06-23", "19:00", "Panamá", "Croatie"), ("Journée 2", "2026-06-23", "22:00", "Colombie", "RD Congo"),
    ("Journée 3", "2026-06-24", "15:00", "Suisse", "Canada"), ("Journée 3", "2026-06-24", "15:00", "Bosnie-et-Herzégovine", "Qatar"),
    ("Journée 3", "2026-06-24", "18:00", "Écosse", "Brésil"), ("Journée 3", "2026-06-24", "18:00", "Maroc", "Haïti"),
    ("Journée 3", "2026-06-24", "21:00", "Tchéquie", "Mexique"), ("Journée 3", "2026-06-24", "21:00", "Afrique du Sud", "République de Corée"),
    ("Journée 3", "2026-06-25", "16:00", "Équateur", "Allemagne"), ("Journée 3", "2026-06-25", "16:00", "Curaçao", "Côte d'Ivoire"),
    ("Journée 3", "2026-06-25", "19:00", "Tunisie", "Pays-Bas"), ("Journée 3", "2026-06-25", "19:00", "Japon", "Suède"),
    ("Journée 3", "2026-06-25", "22:00", "Turquie", "États-Unis"), ("Journée 3", "2026-06-25", "22:00", "Paraguay", "Australie"),
    ("Journée 3", "2026-06-26", "15:00", "Norvège", "France"), ("Journée 3", "2026-06-26", "15:00", "Sénégal", "Irak"),
    ("Journée 3", "2026-06-26", "20:00", "Uruguay", "Espagne"), ("Journée 3", "2026-06-26", "20:00", "Cap-Vert", "Arabie saoudite"),
    ("Journée 3", "2026-06-26", "23:00", "Nouvelle-Zélande", "Belgique"), ("Journée 3", "2026-06-26", "23:00", "Égypte", "RI Iran"),
    ("Journée 3", "2026-06-27", "17:00", "Panamá", "Angleterre"), ("Journée 3", "2026-06-27", "17:00", "Croatie", "Ghana"),
    ("Journée 3", "2026-06-27", "19:30", "Colombie", "Portugal"), ("Journée 3", "2026-06-27", "19:30", "RD Congo", "Ouzbékistan"),
    ("Journée 3", "2026-06-27", "22:00", "Jordanie", "Argentine"), ("Journée 3", "2026-06-27", "22:00", "Algérie", "Autriche"),

    # --- SEIZIÈMES DE FINALE ---
    ("Seizièmes de finale", "2026-06-28", "15:00", "Deuxième Groupe A", "Deuxième Groupe B"),
    ("Seizièmes de finale", "2026-06-29", "16:30", "Premier Groupe E", "Troisième Groupe ABCD"),
    ("Seizièmes de finale", "2026-06-29", "21:00", "Premier Groupe F", "Deuxième Groupe C"),
    ("Seizièmes de finale", "2026-06-29", "13:00", "Premier Groupe C", "Deuxième Groupe F"),
    ("Seizièmes de finale", "2026-06-30", "17:00", "Premier Groupe I", "Troisième Groupe CDFGH"),
    ("Seizièmes de finale", "2026-06-30", "13:00", "Deuxième Groupe E", "Deuxième Groupe I"),
    ("Seizièmes de finale", "2026-06-30", "21:00", "Premier Groupe A", "Troisième Groupe CEFH"),
    ("Seizièmes de finale", "2026-07-01", "12:00", "Premier Groupe L", "Troisième Groupe EHIJK"),
    ("Seizièmes de finale", "2026-07-01", "20:00", "Premier Groupe D", "Troisième Groupe BEFIJ"),
    ("Seizièmes de finale", "2026-07-01", "16:00", "Premier Groupe G", "Troisième Groupe AEHIJ"),
    ("Seizièmes de finale", "2026-07-02", "19:00", "Deuxième Groupe K", "Deuxième Groupe L"),
    ("Seizièmes de finale", "2026-07-02", "15:00", "Premier Groupe H", "Deuxième Groupe J"),
    ("Seizièmes de finale", "2026-07-02", "23:00", "Premier Groupe B", "Troisième Groupe EFGIJ"),
    ("Seizièmes de finale", "2026-07-03", "18:00", "Premier Groupe J", "Deuxième Groupe H"),
    ("Seizièmes de finale", "2026-07-03", "21:30", "Premier Groupe K", "Troisième Groupe DEIJL"),
    ("Seizièmes de finale", "2026-07-03", "14:00", "Deuxième Groupe D", "Deuxième Groupe G"),

    # --- HUITIÈMES DE FINALE ---
    ("Huitièmes de finale", "2026-07-04", "17:00", "Vainqueur Match 74", "Vainqueur Match 77"),
    ("Huitièmes de finale", "2026-07-04", "13:00", "Vainqueur Match 73", "Vainqueur Match 75"),
    ("Huitièmes de finale", "2026-07-05", "16:00", "Vainqueur Match 76", "Vainqueur Match 78"),
    ("Huitièmes de finale", "2026-07-05", "20:00", "Vainqueur Match 79", "Vainqueur Match 80"),
    ("Huitièmes de finale", "2026-07-06", "15:00", "Vainqueur Match 83", "Vainqueur Match 84"),
    ("Huitièmes de finale", "2026-07-06", "20:00", "Vainqueur Match 81", "Vainqueur Match 82"),
    ("Huitièmes de finale", "2026-07-07", "12:00", "Vainqueur Match 86", "Vainqueur Match 88"),
    ("Huitièmes de finale", "2026-07-07", "16:00", "Vainqueur Match 85", "Vainqueur Match 87"),

    # --- QUARTS DE FINALE ---
    ("Quarts de finale", "2026-07-09", "16:00", "Vainqueur Match 89", "Vainqueur Match 90"),
    ("Quarts de finale", "2026-07-10", "15:00", "Vainqueur Match 93", "Vainqueur Match 94"),
    ("Quarts de finale", "2026-07-11", "17:00", "Vainqueur Match 91", "Vainqueur Match 92"),
    ("Quarts de finale", "2026-07-11", "21:00", "Vainqueur Match 95", "Vainqueur Match 96"),

    # --- DEMI-FINALES ---
    ("Demi-finales", "2026-07-14", "15:00", "Vainqueur Match 97", "Vainqueur Match 98"),
    ("Demi-finales", "2026-07-15", "15:00", "Vainqueur Match 99", "Vainqueur Match 100"),

    # --- FINALES ---
    ("Petite finale", "2026-07-18", "17:00", "Perdant Match 101", "Perdant Match 102"),
    ("Finale", "2026-07-19", "15:00", "Vainqueur Match 101", "Vainqueur Match 102")
]

for match in calendrier:
    phase, date_m, heure, eq1, eq2 = match
    logo1 = DRAPEAUX.get(eq1, "https://flagcdn.com/w80/un.png")
    logo2 = DRAPEAUX.get(eq2, "https://flagcdn.com/w80/un.png")
    
    conn.execute('''
        INSERT INTO Matchs (phase, date, heure, eq1, logo1, eq2, logo2, statut)
        VALUES (?, ?, ?, ?, ?, ?, ?, 'En attente')
    ''', (phase, date_m, heure, eq1, logo1, eq2, logo2))

conn.commit()
conn.close()

print("✅ Base de données recréée à NEUF avec les 104 matchs, prête pour les vrais joueurs !")