from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
import random

app = Flask(__name__)
app.secret_key = 'projet_world_cup_2026_key'

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

GROUPES_FIFA = {
    'Groupe A': ['Mexique', 'Afrique du Sud', 'République de Corée', 'Tchéquie'],
    'Groupe B': ['Canada', 'Bosnie-et-Herzégovine', 'Qatar', 'Suisse'],
    'Groupe C': ['Brésil', 'Maroc', 'Haïti', 'Écosse'],
    'Groupe D': ['États-Unis', 'Paraguay', 'Australie', 'Turquie'],
    'Groupe E': ['Allemagne', 'Curaçao', "Côte d'Ivoire", 'Équateur'],
    'Groupe F': ['Pays-Bas', 'Japon', 'Suède', 'Tunisie'],
    'Groupe G': ['Belgique', 'Égypte', 'RI Iran', 'Nouvelle-Zélande'],
    'Groupe H': ['Espagne', 'Cap-Vert', 'Arabie saoudite', 'Uruguay'],
    'Groupe I': ['France', 'Sénégal', 'Irak', 'Norvège'],
    'Groupe J': ['Argentine', 'Algérie', 'Autriche', 'Jordanie'],
    'Groupe K': ['Portugal', 'RD Congo', 'Ouzbékistan', 'Colombie'],
    'Groupe L': ['Angleterre', 'Croatie', 'Ghana', 'Panamá']
}

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    if 'user_id' in session: return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nom, prenom, email = request.form['nom'], request.form['prenom'], request.form['email']
        pw, pw_c = request.form['password'], request.form['password_confirm']
        pseudo = email.split('@')[0]
        
        if "@" not in email or len(pw) < 8:
            flash("Email invalide ou mot de passe trop court.", "danger")
        elif pw != pw_c:
            flash("Les mots de passe ne correspondent pas.", "danger")
        else:
            conn = get_db_connection()
            try:
                conn.execute('INSERT INTO Utilisateurs (nom, prenom, pseudo, email, mot_de_passe_hash) VALUES (?, ?, ?, ?, ?)', 
                             (nom, prenom, pseudo, email, generate_password_hash(pw)))
                conn.commit()
                flash("Compte créé avec succès ! Connectez-vous.", "success")
                return redirect(url_for('login'))
            except sqlite3.IntegrityError:
                flash("Cet Email est déjà utilisé.", "danger")
            finally: 
                conn.close()
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email, pw = request.form['email'], request.form['password']
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM Utilisateurs WHERE email = ?', (email,)).fetchone()
        conn.close()
        if user and check_password_hash(user['mot_de_passe_hash'], pw):
            session['user_id'], session['email'] = user['id'], user['email']
            return redirect(url_for('dashboard'))
        flash("Identifiants incorrects.")
    return render_template('login.html')

@app.route('/accueil')
def accueil():
    if 'user_id' not in session: return redirect(url_for('login'))
    return render_template('accueil.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session: return redirect(url_for('login'))
    conn = get_db_connection()
    user_id = session['user_id']
    
    if request.method == 'POST':
        match_id = request.form['match_id']
        score1, score2 = request.form['score1'], request.form['score2']
        existant = conn.execute('SELECT id FROM Pronostics WHERE id_utilisateur = ? AND id_match = ?', (user_id, match_id)).fetchone()
        if existant:
            conn.execute('UPDATE Pronostics SET prono_score_eq1 = ?, prono_score_eq2 = ? WHERE id = ?', (score1, score2, existant['id']))      
        else:
            conn.execute('INSERT INTO Pronostics (id_utilisateur, id_match, prono_score_eq1, prono_score_eq2) VALUES (?, ?, ?, ?)', (user_id, match_id, score1, score2))
        conn.commit()
        flash("Pronostic enregistré avec succès !", "success")
        return redirect(url_for('dashboard'))
        
    # CORRECTION DE LA LOGIQUE DES CADENAS : On débloque si le tour PRÉCÉDENT est terminé !
    unlocked = {
        'seiziemes': conn.execute("SELECT count(*) as c FROM Matchs WHERE phase LIKE '%Journée%' AND statut != 'Terminé'").fetchone()['c'] == 0,
        'huitiemes': conn.execute("SELECT count(*) as c FROM Matchs WHERE phase LIKE '%Seizièmes%' AND statut != 'Terminé'").fetchone()['c'] == 0,
        'quarts': conn.execute("SELECT count(*) as c FROM Matchs WHERE phase LIKE '%Huitièmes%' AND statut != 'Terminé'").fetchone()['c'] == 0,
        'demis': conn.execute("SELECT count(*) as c FROM Matchs WHERE phase LIKE '%Quarts%' AND statut != 'Terminé'").fetchone()['c'] == 0,
        'petite': conn.execute("SELECT count(*) as c FROM Matchs WHERE phase LIKE '%Demi%' AND statut != 'Terminé'").fetchone()['c'] == 0,
        'finale': conn.execute("SELECT count(*) as c FROM Matchs WHERE phase LIKE '%Demi%' AND statut != 'Terminé'").fetchone()['c'] == 0
    }

    matchs = conn.execute('''
        SELECT m.*, p.prono_score_eq1, p.prono_score_eq2, p.points_obtenus
        FROM Matchs m
        LEFT JOIN Pronostics p ON m.id = p.id_match AND p.id_utilisateur = ?
        ORDER BY 
            CASE 
                WHEN m.phase LIKE '%Journée 1%' THEN 1
                WHEN m.phase LIKE '%Journée 2%' THEN 2
                WHEN m.phase LIKE '%Journée 3%' THEN 3
                WHEN m.phase LIKE '%Seizièmes%' THEN 4
                WHEN m.phase LIKE '%Huitièmes%' THEN 5
                WHEN m.phase LIKE '%Quarts%' THEN 6
                WHEN m.phase LIKE '%Demi%' THEN 7
                WHEN m.phase LIKE '%Petite finale%' THEN 8
                WHEN m.phase LIKE '%Finale%' THEN 9
                ELSE 10
            END,
            m.date ASC, m.heure ASC
    ''', (user_id,)).fetchall()
    
    user = conn.execute('SELECT points_totaux FROM Utilisateurs WHERE id = ?', (user_id,)).fetchone()
    points_totaux = user['points_totaux'] if user else 0
    conn.close()
    
    return render_template('dashboard.html', matchs=matchs, points_totaux=points_totaux, unlocked=unlocked)

@app.route('/calendrier')
def calendrier():
    if 'user_id' not in session: return redirect(url_for('login'))
    conn = get_db_connection()
    matchs = conn.execute('SELECT * FROM Matchs ORDER BY date ASC, heure ASC').fetchall()
    conn.close()
    return render_template('calendrier.html', matchs=matchs)

@app.route('/ranking')
def ranking():
    conn = get_db_connection()
    users = conn.execute("SELECT nom, prenom, points_totaux FROM Utilisateurs WHERE email != 'admin@esme.fr' ORDER BY points_totaux DESC").fetchall()
    conn.close()
    return render_template('ranking.html', users=users)

@app.route('/groupes')
def groupes():
    conn = get_db_connection()
    matchs_poules = conn.execute("SELECT * FROM Matchs WHERE statut = 'Terminé' AND phase LIKE 'Journée%'").fetchall()
    tous_les_matchs = conn.execute("SELECT * FROM Matchs").fetchall()
    conn.close()

    stats = {}
    for grp, equipes in GROUPES_FIFA.items():
        for eq in equipes:
            stats[eq] = {'nom': eq, 'groupe': grp, 'pts': 0, 'mj': 0, 'g': 0, 'n': 0, 'p': 0, 'bp': 0, 'bc': 0, 'diff': 0, 'logo': DRAPEAUX.get(eq, "https://flagcdn.com/w80/un.png")}

    for m in matchs_poules:
        eq1, eq2, sc1, sc2 = m['eq1'], m['eq2'], m['vrai_score_eq1'], m['vrai_score_eq2']
        if sc1 is not None and sc2 is not None:
            if eq1 in stats:
                stats[eq1]['mj'] += 1; stats[eq1]['bp'] += sc1; stats[eq1]['bc'] += sc2; stats[eq1]['diff'] = stats[eq1]['bp'] - stats[eq1]['bc']
            if eq2 in stats:
                stats[eq2]['mj'] += 1; stats[eq2]['bp'] += sc2; stats[eq2]['bc'] += sc1; stats[eq2]['diff'] = stats[eq2]['bp'] - stats[eq2]['bc']
            if sc1 > sc2:
                if eq1 in stats: stats[eq1]['pts'] += 3; stats[eq1]['g'] += 1
                if eq2 in stats: stats[eq2]['p'] += 1
            elif sc1 < sc2:
                if eq2 in stats: stats[eq2]['pts'] += 3; stats[eq2]['g'] += 1
                if eq1 in stats: stats[eq1]['p'] += 1
            else:
                if eq1 in stats: stats[eq1]['pts'] += 1; stats[eq1]['n'] += 1
                if eq2 in stats: stats[eq2]['pts'] += 1; stats[eq2]['n'] += 1

    classement_final = {}
    for grp, equipes in GROUPES_FIFA.items():
        eqs = [stats[eq] for eq in equipes]
        eqs.sort(key=lambda x: (x['pts'], x['diff'], x['bp']), reverse=True)
        classement_final[grp] = eqs

    return render_template('groupes.html', classement=classement_final, matchs=tous_les_matchs)

@app.route('/profil')
def profil():
    if 'user_id' not in session: return redirect(url_for('login'))
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM Utilisateurs WHERE id = ?', (session['user_id'],)).fetchone()
    conn.close()
    return render_template('profil.html', user=user)

@app.route('/preferences')
def preferences():
    if 'user_id' not in session: return redirect(url_for('login'))
    return render_template('preferences.html')

@app.route('/reglement')
def reglement(): 
    return render_template('reglement.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'user_id' not in session or session.get('email') != 'admin@esme.fr':
        flash("Accès interdit.")
        return redirect(url_for('dashboard'))
        
    conn = get_db_connection()
    if request.method == 'POST':
        match_id = request.form['match_id']
        vrai_s1 = int(request.form['vrai_score1'])
        vrai_s2 = int(request.form['vrai_score2'])
        
        conn.execute("UPDATE Matchs SET vrai_score_eq1 = ?, vrai_score_eq2 = ?, statut = 'Terminé' WHERE id = ?", (vrai_s1, vrai_s2, match_id))
        
        pronos = conn.execute('SELECT * FROM Pronostics WHERE id_match = ?', (match_id,)).fetchall()
        for prono in pronos:
            p_s1, p_s2 = prono['prono_score_eq1'], prono['prono_score_eq2']
            points = 0
            if p_s1 == vrai_s1 and p_s2 == vrai_s2: points = 3
            elif (vrai_s1 > vrai_s2 and p_s1 > p_s2) or (vrai_s1 < vrai_s2 and p_s1 < p_s2) or (vrai_s1 == vrai_s2 and p_s1 == p_s2): points = 1
            
            conn.execute('UPDATE Pronostics SET points_obtenus = ? WHERE id = ?', (points, prono['id']))
            totaux = conn.execute('SELECT SUM(points_obtenus) as total FROM Pronostics WHERE id_utilisateur = ?', (prono['id_utilisateur'],)).fetchone()
            nouveau_total = totaux['total'] if totaux['total'] is not None else 0
            conn.execute('UPDATE Utilisateurs SET points_totaux = ? WHERE id = ?', (nouveau_total, prono['id_utilisateur']))
            
        avancer_tournoi(conn)
        conn.commit()
        flash("Match validé ! L'arbre s'est mis à jour automatiquement.")
        return redirect(url_for('admin'))

    matchs = conn.execute('SELECT * FROM Matchs').fetchall()
    conn.close()
    return render_template('admin.html', matchs=matchs)

@app.route('/randomize', methods=['POST'])
def randomize():
    if 'user_id' not in session: return redirect(url_for('login'))
    phase = request.form.get('phase')
    conn = get_db_connection()
    matchs = conn.execute('SELECT id FROM Matchs WHERE phase = ? AND statut != "Terminé"', (phase,)).fetchall()
    
    for m in matchs:
        score1 = random.randint(0, 5)
        score2 = random.randint(0, 5)
        conn.execute("UPDATE Matchs SET vrai_score_eq1 = ?, vrai_score_eq2 = ?, statut = 'Terminé' WHERE id = ?", (score1, score2, m['id']))
        avancer_tournoi(conn)
        
    conn.commit()
    conn.close()
    flash(f"Scores générés aléatoirement pour la {phase} !", "success")
    return redirect(url_for('admin'))

def avancer_tournoi(conn):
    poules_terminees = conn.execute("SELECT count(*) as c FROM Matchs WHERE id <= 72 AND statut != 'Terminé'").fetchone()['c'] == 0
    if poules_terminees:
        m73 = conn.execute("SELECT eq1 FROM Matchs WHERE id = 73").fetchone()
        if m73 and ("Deuxième" in m73['eq1'] or "Premier" in m73['eq1']):
            stats = {eq: {'nom': eq, 'pts': 0, 'diff': 0, 'bp': 0, 'logo': DRAPEAUX.get(eq, "https://flagcdn.com/w80/un.png")} for eq in DRAPEAUX.keys()}
            matchs_poules = conn.execute("SELECT * FROM Matchs WHERE id <= 72 AND statut = 'Terminé'").fetchall()
            for m in matchs_poules:
                sc1, sc2 = m['vrai_score_eq1'], m['vrai_score_eq2']
                if m['eq1'] in stats and m['eq2'] in stats:
                    stats[m['eq1']]['bp'] += sc1; stats[m['eq1']]['diff'] += (sc1 - sc2)
                    stats[m['eq2']]['bp'] += sc2; stats[m['eq2']]['diff'] += (sc2 - sc1)
                    if sc1 > sc2: stats[m['eq1']]['pts'] += 3
                    elif sc1 < sc2: stats[m['eq2']]['pts'] += 3
                    else: stats[m['eq1']]['pts'] += 1; stats[m['eq2']]['pts'] += 1
            
            les_32_equipes = []
            for grp, equipes in GROUPES_FIFA.items():
                eqs = [stats[eq] for eq in equipes]
                eqs.sort(key=lambda x: (x['pts'], x['diff'], x['bp']), reverse=True)
                les_32_equipes.extend(eqs[:2])
                if grp in ['Groupe A', 'Groupe B', 'Groupe C', 'Groupe D', 'Groupe E', 'Groupe F', 'Groupe G', 'Groupe H']:
                    les_32_equipes.append(eqs[2])
            
            random.shuffle(les_32_equipes)
            match_id = 73
            for i in range(0, 32, 2):
                eqA, eqB = les_32_equipes[i], les_32_equipes[i+1]
                conn.execute("UPDATE Matchs SET eq1 = ?, logo1 = ?, eq2 = ?, logo2 = ? WHERE id = ?", 
                             (eqA['nom'], eqA['logo'], eqB['nom'], eqB['logo'], match_id))
                match_id += 1

    # LE DICTIONNAIRE PARFAIT AVEC LES BONS IDs
    progression = {
        74: (89, 'eq1'), 77: (89, 'eq2'), 73: (90, 'eq1'), 75: (90, 'eq2'),
        76: (91, 'eq1'), 78: (91, 'eq2'), 79: (92, 'eq1'), 80: (92, 'eq2'),
        83: (93, 'eq1'), 84: (93, 'eq2'), 81: (94, 'eq1'), 82: (94, 'eq2'),
        86: (95, 'eq1'), 88: (95, 'eq2'), 85: (96, 'eq1'), 87: (96, 'eq2'),
        89: (97, 'eq1'), 90: (97, 'eq2'), 93: (98, 'eq1'), 94: (98, 'eq2'),
        91: (99, 'eq1'), 92: (99, 'eq2'), 95: (100, 'eq1'), 96: (100, 'eq2'),
        97: (101, 'eq1'), 98: (101, 'eq2'), 99: (102, 'eq1'), 100: (102, 'eq2')
    }
    
    matchs_termines = conn.execute("SELECT * FROM Matchs WHERE id >= 73 AND statut = 'Terminé'").fetchall()
    for m in matchs_termines:
        if m['eq1'].startswith("Vainqueur") or m['eq1'].startswith("Perdant") or "Groupe" in m['eq1']: continue
        
        vainqueur = m['eq1'] if m['vrai_score_eq1'] > m['vrai_score_eq2'] else m['eq2']
        logo_vainqueur = m['logo1'] if m['vrai_score_eq1'] > m['vrai_score_eq2'] else m['logo2']
        perdant = m['eq2'] if m['vrai_score_eq1'] > m['vrai_score_eq2'] else m['eq1']
        logo_perdant = m['logo2'] if m['vrai_score_eq1'] > m['vrai_score_eq2'] else m['logo1']
        
        if m['id'] in progression:
            cible_id, cible_eq = progression[m['id']]
            if cible_eq == 'eq1': conn.execute("UPDATE Matchs SET eq1 = ?, logo1 = ? WHERE id = ?", (vainqueur, logo_vainqueur, cible_id))
            else: conn.execute("UPDATE Matchs SET eq2 = ?, logo2 = ? WHERE id = ?", (vainqueur, logo_vainqueur, cible_id))
        
        if m['id'] == 101:
            conn.execute("UPDATE Matchs SET eq1 = ?, logo1 = ? WHERE id = 104", (vainqueur, logo_vainqueur))
            conn.execute("UPDATE Matchs SET eq1 = ?, logo1 = ? WHERE id = 103", (perdant, logo_perdant))
        elif m['id'] == 102:
            conn.execute("UPDATE Matchs SET eq2 = ?, logo2 = ? WHERE id = 104", (vainqueur, logo_vainqueur))
            conn.execute("UPDATE Matchs SET eq2 = ?, logo2 = ? WHERE id = 103", (perdant, logo_perdant))

@app.route('/admin/reset', methods=['POST'])
def reset_competition():
    if 'user_id' not in session or session.get('email') != 'admin@esme.fr':
        flash("Accès interdit.", "danger")
        return redirect(url_for('dashboard'))
        
    # Récupérer le choix de l'administrateur concernant les joueurs
    conserver_joueurs = request.form.get('conserver_joueurs') == 'oui'
    
    conn = get_db_connection()
    
    # 1. Supprimer tous les pronostics enregistrés
    conn.execute("DELETE FROM Pronostics")
    conn.execute("DELETE FROM sqlite_sequence WHERE name='Pronostics'")
    
    # 2. Gestion des utilisateurs du classement
    if conserver_joueurs:
        # On garde les comptes mais on remet les compteurs de points à 0
        conn.execute("UPDATE Utilisateurs SET points_totaux = 0")
        flash("Compétition réinitialisée ! Les joueurs ont été conservés et leurs points remis à 0.", "success")
    else:
        # On supprime tout le monde SAUF le compte administrateur principal
        conn.execute("DELETE FROM Utilisateurs WHERE email != 'admin@esme.fr'")
        flash("Compétition réinitialisée ! Tous les joueurs ont été supprimés du classement.", "success")
    
    # 3. Réinitialisation complète des 104 matchs à l'état d'origine
    conn.execute("DELETE FROM Matchs")
    conn.execute("DELETE FROM sqlite_sequence WHERE name='Matchs'")
    
    calendrier_initial = [
        # --- JOURNÉE 1 ---
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

        # --- JOURNÉE 2 ---
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

        # --- JOURNÉE 3 ---
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
        ("Journée 3", "2026-06-27", "22:00", "Algérie", "Autriche", "En attente"),

        # --- SEIZIÈMES DE FINALE ---
        ("Seizièmes de finale", "2026-06-28", "15:00", "Deuxième Groupe A", "Deuxième Groupe B", "En attente"),
        ("Seizièmes de finale", "2026-06-29", "16:30", "Premier Groupe E", "Troisième Groupe ABCD", "En attente"),
        ("Seizièmes de finale", "2026-06-29", "21:00", "Premier Groupe F", "Deuxième Groupe C", "En attente"),
        ("Seizièmes de finale", "2026-06-29", "13:00", "Premier Groupe C", "Deuxième Groupe F", "En attente"),
        ("Seizièmes de finale", "2026-06-30", "17:00", "Premier Groupe I", "Troisième Groupe CDFGH", "En attente"),
        ("Seizièmes de finale", "2026-06-30", "13:00", "Deuxième Groupe E", "Deuxième Groupe I", "En attente"),
        ("Seizièmes de finale", "2026-06-30", "21:00", "Premier Groupe A", "Troisième Groupe CEFH", "En attente"),
        ("Seizièmes de finale", "2026-07-01", "12:00", "Premier Groupe L", "Troisième Groupe EHIJK", "En attente"),
        ("Seizièmes de finale", "2026-07-01", "20:00", "Premier Groupe D", "Troisième Groupe BEFIJ", "En attente"),
        ("Seizièmes de finale", "2026-07-01", "16:00", "Premier Groupe G", "Troisième Groupe AEHIJ", "En attente"),
        ("Seizièmes de finale", "2026-07-02", "19:00", "Deuxième Groupe K", "Deuxième Groupe L", "En attente"),
        ("Seizièmes de finale", "2026-07-02", "15:00", "Premier Groupe H", "Deuxième Groupe J", "En attente"),
        ("Seizièmes de finale", "2026-07-02", "23:00", "Premier Groupe B", "Troisième Groupe EFGIJ", "En attente"),
        ("Seizièmes de finale", "2026-07-03", "18:00", "Premier Groupe J", "Deuxième Groupe H", "En attente"),
        ("Seizièmes de finale", "2026-07-03", "21:30", "Premier Groupe K", "Troisième Groupe DEIJL", "En attente"),
        ("Seizièmes de finale", "2026-07-03", "14:00", "Deuxième Groupe D", "Deuxième Groupe G", "En attente"),

        # --- HUITIÈMES DE FINALE ---
        ("Huitièmes de finale", "2026-07-04", "17:00", "Vainqueur Match 74", "Vainqueur Match 77", "En attente"),
        ("Huitièmes de finale", "2026-07-04", "13:00", "Vainqueur Match 73", "Vainqueur Match 75", "En attente"),
        ("Huitièmes de finale", "2026-07-05", "16:00", "Vainqueur Match 76", "Vainqueur Match 78", "En attente"),
        ("Huitièmes de finale", "2026-07-05", "20:00", "Vainqueur Match 79", "Vainqueur Match 80", "En attente"),
        ("Huitièmes de finale", "2026-07-06", "15:00", "Vainqueur Match 83", "Vainqueur Match 84", "En attente"),
        ("Huitièmes de finale", "2026-07-06", "20:00", "Vainqueur Match 81", "Vainqueur Match 82", "En attente"),
        ("Huitièmes de finale", "2026-07-07", "12:00", "Vainqueur Match 86", "Vainqueur Match 88", "En attente"),
        ("Huitièmes de finale", "2026-07-07", "16:00", "Vainqueur Match 85", "Vainqueur Match 87", "En attente"),

        # --- QUARTS DE FINALE ---
        ("Quarts de finale", "2026-07-09", "16:00", "Vainqueur Match 89", "Vainqueur Match 90", "En attente"),
        ("Quarts de finale", "2026-07-10", "15:00", "Vainqueur Match 93", "Vainqueur Match 94", "En attente"),
        ("Quarts de finale", "2026-07-11", "17:00", "Vainqueur Match 91", "Vainqueur Match 92", "En attente"),
        ("Quarts de finale", "2026-07-11", "21:00", "Vainqueur Match 95", "Vainqueur Match 96", "En attente"),

        # --- DEMI-FINALES ---
        ("Demi-finales", "2026-07-14", "15:00", "Vainqueur Match 97", "Vainqueur Match 98", "En attente"),
        ("Demi-finales", "2026-07-15", "15:00", "Vainqueur Match 99", "Vainqueur Match 100", "En attente"),

        # --- FINALES ---
        ("Petite finale", "2026-07-18", "17:00", "Perdant Match 101", "Perdant Match 102", "En attente"),
        ("Finale", "2026-07-19", "15:00", "Vainqueur Match 101", "Vainqueur Match 102", "En attente")
    ]
    
    for match in calendrier_initial:
        phase, date_m, heure, eq1, eq2, statut = match
        logo1 = DRAPEAUX.get(eq1, "https://flagcdn.com/w80/un.png")
        logo2 = DRAPEAUX.get(eq2, "https://flagcdn.com/w80/un.png")
        conn.execute('''
            INSERT INTO Matchs (phase, date, heure, eq1, logo1, eq2, logo2, statut)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (phase, date_m, heure, eq1, logo1, eq2, logo2, statut))
        
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)