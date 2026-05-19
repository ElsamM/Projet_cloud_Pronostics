import sqlite3

print("Création du calendrier COMPLET de la Coupe du Monde 2026...")

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

conn = sqlite3.connect('database.db')
conn.execute('DELETE FROM Matchs') 

calendrier = [
    # JOURNÉE 1
    ("Journée 1", "2026-06-11", "15:00", "Mexique", "Afrique du Sud", "En attente"),
    ("Journée 1", "2026-06-11", "22:00", "République de Corée", "Tchéquie", "En attente"),
    ("Journée 1", "2026-06-12", "15:00", "Canada", "Bosnie-et-Herzégovine", "En attente"),
    ("Journée 1", "2026-06-12", "21:00", "États-Unis", "Paraguay", "En attente"),
    ("Journée 1", "2026-06-13", "15:00", "Qatar", "Suisse", "En attente"),
    ("Journée 1", "2026-06-13", "18:00", "Brésil", "Maroc", "En attente"),
    ("Journée 1", "2026-06-13", "21:00", "Haïti", "Écosse", "En attente"),
    ("Journée 1", "2026-06-13", "00:00", "Australie", "Turquie", "En attente"),
    ("Journée 1", "2026-06-14", "13:00", "Allemagne", "Curaçao", "En attente"),
    ("Journée 1", "2026-06-14", "16:00", "Pays-Bas", "Japon", "En attente"),
    ("Journée 1", "2026-06-14", "19:00", "Côte d'Ivoire", "Équateur", "En attente"),
    ("Journée 1", "2026-06-14", "22:00", "Suède", "Tunisie", "En attente"),
    ("Journée 1", "2026-06-15", "12:00", "Espagne", "Cap-Vert", "En attente"),
    ("Journée 1", "2026-06-15", "15:00", "Belgique", "Égypte", "En attente"),
    ("Journée 1", "2026-06-15", "18:00", "Arabie saoudite", "Uruguay", "En attente"),
    ("Journée 1", "2026-06-15", "21:00", "RI Iran", "Nouvelle-Zélande", "En attente"),
    ("Journée 1", "2026-06-16", "15:00", "France", "Sénégal", "En attente"),
    ("Journée 1", "2026-06-16", "18:00", "Irak", "Norvège", "En attente"),
    ("Journée 1", "2026-06-16", "21:00", "Argentine", "Algérie", "En attente"),
    ("Journée 1", "2026-06-16", "00:00", "Autriche", "Jordanie", "En attente"),
    ("Journée 1", "2026-06-17", "13:00", "Portugal", "RD Congo", "En attente"),
    ("Journée 1", "2026-06-17", "16:00", "Angleterre", "Croatie", "En attente"),
    ("Journée 1", "2026-06-17", "19:00", "Ghana", "Panamá", "En attente"),
    ("Journée 1", "2026-06-17", "22:00", "Ouzbékistan", "Colombie", "En attente"),

    # JOURNÉE 2
    ("Journée 2", "2026-06-18", "12:00", "Tchéquie", "Afrique du Sud", "En attente"),
    ("Journée 2", "2026-06-18", "15:00", "Suisse", "Bosnie-et-Herzégovine", "En attente"),
    ("Journée 2", "2026-06-18", "18:00", "Canada", "Qatar", "En attente"),
    ("Journée 2", "2026-06-18", "21:00", "Mexique", "République de Corée", "En attente"),
    ("Journée 2", "2026-06-19", "15:00", "États-Unis", "Australie", "En attente"),
    ("Journée 2", "2026-06-19", "18:00", "Écosse", "Maroc", "En attente"),
    ("Journée 2", "2026-06-19", "20:30", "Brésil", "Haïti", "En attente"),
    ("Journée 2", "2026-06-19", "23:00", "Turquie", "Paraguay", "En attente"),
    ("Journée 2", "2026-06-20", "13:00", "Pays-Bas", "Suède", "En attente"),
    ("Journée 2", "2026-06-20", "16:00", "Allemagne", "Côte d'Ivoire", "En attente"),
    ("Journée 2", "2026-06-20", "20:00", "Équateur", "Curaçao", "En attente"),
    ("Journée 2", "2026-06-20", "00:00", "Tunisie", "Japon", "En attente"),
    ("Journée 2", "2026-06-21", "12:00", "Espagne", "Arabie saoudite", "En attente"),
    ("Journée 2", "2026-06-21", "15:00", "Belgique", "RI Iran", "En attente"),
    ("Journée 2", "2026-06-21", "18:00", "Uruguay", "Cap-Vert", "En attente"),
    ("Journée 2", "2026-06-21", "21:00", "Nouvelle-Zélande", "Égypte", "En attente"),
    ("Journée 2", "2026-06-22", "13:00", "Argentine", "Autriche", "En attente"),
    ("Journée 2", "2026-06-22", "17:00", "France", "Irak", "En attente"),
    ("Journée 2", "2026-06-22", "20:00", "Norvège", "Sénégal", "En attente"),
    ("Journée 2", "2026-06-22", "23:00", "Jordanie", "Algérie", "En attente"),
    ("Journée 2", "2026-06-23", "13:00", "Portugal", "Ouzbékistan", "En attente"),
    ("Journée 2", "2026-06-23", "16:00", "Angleterre", "Ghana", "En attente"),
    ("Journée 2", "2026-06-23", "19:00", "Panamá", "Croatie", "En attente"),
    ("Journée 2", "2026-06-23", "22:00", "Colombie", "RD Congo", "En attente"),

    # JOURNÉE 3
    ("Journée 3", "2026-06-24", "15:00", "Suisse", "Canada", "En attente"),
    ("Journée 3", "2026-06-24", "15:00", "Bosnie-et-Herzégovine", "Qatar", "En attente"),
    ("Journée 3", "2026-06-24", "18:00", "Écosse", "Brésil", "En attente"),
    ("Journée 3", "2026-06-24", "18:00", "Maroc", "Haïti", "En attente"),
    ("Journée 3", "2026-06-24", "21:00", "Tchéquie", "Mexique", "En attente"),
    ("Journée 3", "2026-06-24", "21:00", "Afrique du Sud", "République de Corée", "En attente"),
    ("Journée 3", "2026-06-25", "16:00", "Équateur", "Allemagne", "En attente"),
    ("Journée 3", "2026-06-25", "16:00", "Curaçao", "Côte d'Ivoire", "En attente"),
    ("Journée 3", "2026-06-25", "19:00", "Tunisie", "Pays-Bas", "En attente"),
    ("Journée 3", "2026-06-25", "19:00", "Japon", "Suède", "En attente"),
    ("Journée 3", "2026-06-25", "22:00", "Turquie", "États-Unis", "En attente"),
    ("Journée 3", "2026-06-25", "22:00", "Paraguay", "Australie", "En attente"),
    ("Journée 3", "2026-06-26", "15:00", "Norvège", "France", "En attente"),
    ("Journée 3", "2026-06-26", "15:00", "Sénégal", "Irak", "En attente"),
    ("Journée 3", "2026-06-26", "20:00", "Uruguay", "Espagne", "En attente"),
    ("Journée 3", "2026-06-26", "20:00", "Cap-Vert", "Arabie saoudite", "En attente"),
    ("Journée 3", "2026-06-26", "23:00", "Nouvelle-Zélande", "Belgique", "En attente"),
    ("Journée 3", "2026-06-26", "23:00", "Égypte", "RI Iran", "En attente"),
    ("Journée 3", "2026-06-27", "17:00", "Panamá", "Angleterre", "En attente"),
    ("Journée 3", "2026-06-27", "17:00", "Croatie", "Ghana", "En attente"),
    ("Journée 3", "2026-06-27", "19:30", "Colombie", "Portugal", "En attente"),
    ("Journée 3", "2026-06-27", "19:30", "RD Congo", "Ouzbékistan", "En attente"),
    ("Journée 3", "2026-06-27", "22:00", "Jordanie", "Argentine", "En attente"),
    ("Journée 3", "2026-06-27", "22:00", "Algérie", "Autriche", "En attente")
]

for match in calendrier:
    phase, date_m, heure, eq1, eq2, statut = match
    logo1 = DRAPEAUX.get(eq1, "https://flagcdn.com/w80/un.png")
    logo2 = DRAPEAUX.get(eq2, "https://flagcdn.com/w80/un.png")
    
    conn.execute('''
        INSERT INTO Matchs (phase, date, heure, eq1, logo1, eq2, logo2, statut)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (phase, date_m, heure, eq1, logo1, eq2, logo2, statut))

conn.commit()
conn.close()

print("Les 72 VRAIS matchs de la Coupe du Monde ont été injectés avec succès !")