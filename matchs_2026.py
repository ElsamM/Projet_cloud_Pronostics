import sqlite3

print("⚽ Création du calendrier officiel de la Coupe du Monde 2026...")

# 1. Le dictionnaire infaillible des drapeaux (Noms en Français -> Drapeaux)
equipes = {
    # Groupe A
    "Mexique": "https://flagcdn.com/w80/mx.png",
    "Afrique du Sud": "https://flagcdn.com/w80/za.png",
    "Corée du Sud": "https://flagcdn.com/w80/kr.png",
    "Europe D": "https://flagcdn.com/w80/un.png",
    # Groupe B
    "Canada": "https://flagcdn.com/w80/ca.png",
    "Europe A": "https://flagcdn.com/w80/un.png",
    "Qatar": "https://flagcdn.com/w80/qa.png",
    "Suisse": "https://flagcdn.com/w80/ch.png",
    # Groupe C
    "Brésil": "https://flagcdn.com/w80/br.png",
    "Maroc": "https://flagcdn.com/w80/ma.png",
    "Haïti": "https://flagcdn.com/w80/ht.png",
    "Écosse": "https://flagcdn.com/w80/gb-sct.png",
    # Groupe D
    "États-Unis": "https://flagcdn.com/w80/us.png",
    "Paraguay": "https://flagcdn.com/w80/py.png",
    "Australie": "https://flagcdn.com/w80/au.png",
    "Europe C": "https://flagcdn.com/w80/un.png",
    # Groupe E
    "Allemagne": "https://flagcdn.com/w80/de.png",
    "Curaçao": "https://flagcdn.com/w80/cw.png",
    "Côte d'Ivoire": "https://flagcdn.com/w80/ci.png",
    "Équateur": "https://flagcdn.com/w80/ec.png",
    # Groupe F
    "Pays-Bas": "https://flagcdn.com/w80/nl.png",
    "Japon": "https://flagcdn.com/w80/jp.png",
    "Europe B": "https://flagcdn.com/w80/un.png",
    "Tunisie": "https://flagcdn.com/w80/tn.png",
    # Groupe G
    "Belgique": "https://flagcdn.com/w80/be.png",
    "Égypte": "https://flagcdn.com/w80/eg.png",
    "Iran": "https://flagcdn.com/w80/ir.png",
    "Nouvelle-Zélande": "https://flagcdn.com/w80/nz.png",
    # Groupe H
    "Espagne": "https://flagcdn.com/w80/es.png",
    "Arabie saoudite": "https://flagcdn.com/w80/sa.png",
    "Uruguay": "https://flagcdn.com/w80/uy.png",
    "Cap-Vert": "https://flagcdn.com/w80/cv.png",
    # Groupe I
    "France": "https://flagcdn.com/w80/fr.png",
    "Sénégal": "https://flagcdn.com/w80/sn.png",
    "Fifa 2": "https://flagcdn.com/w80/un.png",
    "Norvège": "https://flagcdn.com/w80/no.png",
    # Groupe J
    "Argentine": "https://flagcdn.com/w80/ar.png",
    "Algérie": "https://flagcdn.com/w80/dz.png",
    "Jordanie": "https://flagcdn.com/w80/jo.png",
    "Autriche": "https://flagcdn.com/w80/at.png",
    # Groupe K
    "Portugal": "https://flagcdn.com/w80/pt.png",
    "Fifa 1": "https://flagcdn.com/w80/un.png",
    "Ouzbékistan": "https://flagcdn.com/w80/uz.png",
    "Colombie": "https://flagcdn.com/w80/co.png",
    # Groupe L
    "Angleterre": "https://flagcdn.com/w80/gb-eng.png",
    "Croatie": "https://flagcdn.com/w80/hr.png",
    "Panama": "https://flagcdn.com/w80/pa.png",
    "Ghana": "https://flagcdn.com/w80/gh.png"
}

# 2. Connexion à la base de données et nettoyage
conn = sqlite3.connect('database.db')
conn.execute('DELETE FROM Matchs') # On vide les anciens matchs

# 3. Le calendrier des matchs (Extrait du document PDF)
calendrier = [
    # --- JOURNÉE 1 ---
    ("Journée 1", "2026-06-11", "21:00", "Mexique", "Afrique du Sud", "En attente"),
    ("Journée 1", "2026-06-12", "04:00", "Corée du Sud", "Europe D", "En attente"),
    ("Journée 1", "2026-06-12", "21:00", "Canada", "Europe A", "En attente"),
    ("Journée 1", "2026-06-13", "00:00", "Brésil", "Maroc", "En attente"),
    ("Journée 1", "2026-06-13", "03:00", "États-Unis", "Paraguay", "En attente"),
    ("Journée 1", "2026-06-14", "19:00", "Allemagne", "Curaçao", "En attente"),
    ("Journée 1", "2026-06-15", "18:00", "France", "Sénégal", "En attente"),
    ("Journée 1", "2026-06-15", "21:00", "Argentine", "Algérie", "En attente"),
    ("Journée 1", "2026-06-16", "21:00", "Portugal", "Fifa 1", "En attente"),
    ("Journée 1", "2026-06-17", "22:00", "Angleterre", "Croatie", "En attente"),
    
    # --- JOURNÉE 2 (Exemples) ---
    ("Journée 2", "2026-06-18", "21:00", "Suisse", "Europe A", "En attente"),
    ("Journée 2", "2026-06-20", "22:00", "Allemagne", "Côte d'Ivoire", "En attente"),
    ("Journée 2", "2026-06-21", "18:00", "Espagne", "Arabie saoudite", "En attente"),
    ("Journée 2", "2026-06-22", "23:00", "France", "Fifa 2", "En attente"),
    ("Journée 2", "2026-06-23", "22:00", "Angleterre", "Ghana", "En attente"),

    # --- JOURNÉE 3 (Exemples) ---
    ("Journée 3", "2026-06-24", "21:00", "Canada", "Qatar", "En attente"),
    ("Journée 3", "2026-06-25", "22:00", "Équateur", "Allemagne", "En attente"),
    ("Journée 3", "2026-06-26", "21:00", "Norvège", "France", "En attente"),
    
    # --- PHASES FINALES ---
    ("Huitièmes de Finale", "À définir", "À définir", "À définir", "À définir", "En attente"),
    ("Huitièmes de Finale", "À définir", "À définir", "À définir", "À définir", "En attente"),
    ("Quarts de Finale", "2026-07-09", "22:00", "À définir", "À définir", "En attente"),
    ("Quarts de Finale", "2026-07-10", "21:00", "À définir", "À définir", "En attente"),
    ("Demi-finales", "2026-07-14", "21:00", "À définir", "À définir", "En attente"),
    ("Demi-finales", "2026-07-15", "21:00", "À définir", "À définir", "En attente"),
    ("3rd Place Finale", "2026-07-18", "23:00", "À définir", "À définir", "En attente"),
    ("Finale", "2026-07-19", "21:00", "À définir", "À définir", "En attente")
]

# 4. Injection dans la base de données
for match in calendrier:
    phase, date_m, heure, eq1, eq2, statut = match
    
    # On récupère le bon drapeau via notre dictionnaire. Si "À définir", on ne met pas d'image.
    logo1 = equipes.get(eq1, "https://flagcdn.com/w80/un.png") if eq1 != "À définir" else ""
    logo2 = equipes.get(eq2, "https://flagcdn.com/w80/un.png") if eq2 != "À définir" else ""
    
    conn.execute('''
        INSERT INTO Matchs (phase, date, heure, eq1, logo1, eq2, logo2, statut)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (phase, date_m, heure, eq1, logo1, eq2, logo2, statut))

conn.commit()
conn.close()

print("✅ Les vrais matchs de 2026 ont été injectés avec succès !")