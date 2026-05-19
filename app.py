from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
import random

app = Flask(__name__)
app.secret_key = 'projet_world_cup_2026_key'

# LE NOUVEAU DICTIONNAIRE OFFICIEL DES 48 DRAPEAUX
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

# LES 12 VRAIS GROUPES OFFICIELS
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

def init_db():
    if not os.path.exists('database.db'):
        conn = get_db_connection()
        with open('schema.sql', 'r', encoding='utf-8') as f:
            conn.executescript(f.read())
        conn.close()

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
        conn.execute('INSERT OR REPLACE INTO Pronostics (id_utilisateur, id_match, prono_score_eq1, prono_score_eq2) VALUES (?, ?, ?, ?)', 
                     (user_id, match_id, score1, score2))
        conn.commit()
        flash("Pronostic enregistré avec succès !", "success")
        return redirect(url_for('dashboard'))

    unlocked = {
        'huitiemes': conn.execute("SELECT count(*) as c FROM Matchs WHERE phase LIKE '%Journée%' AND statut != 'Terminé'").fetchone()['c'] == 0,
        'quarts': conn.execute("SELECT count(*) as c FROM Matchs WHERE phase LIKE '%Huitièmes%' AND statut != 'Terminé'").fetchone()['c'] == 0,
        'demis': conn.execute("SELECT count(*) as c FROM Matchs WHERE phase LIKE '%Quarts%' AND statut != 'Terminé'").fetchone()['c'] == 0,
        'finale': conn.execute("SELECT count(*) as c FROM Matchs WHERE phase LIKE '%Demi%' AND statut != 'Terminé'").fetchone()['c'] == 0
    }

    matchs = conn.execute('''
        SELECT m.*, p.prono_score_eq1, p.prono_score_eq2
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

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'user_id' not in session or session.get('email') != 'admin@esme.fr':
        flash("Accès interdit. Vous devez être administrateur.")
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
            
        conn.commit()
        flash("Match validé ! Les points des joueurs ont été mis à jour.")
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
        
    conn.commit()
    conn.close()
    flash(f"Scores générés aléatoirement pour la {phase} !", "success")
    return redirect(url_for('admin'))

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
def reglement(): return render_template('reglement.html')

@app.route('/generer_arbre', methods=['POST'])
def generer_arbre():
    if 'user_id' not in session or session.get('email') != 'admin@esme.fr':
        return redirect(url_for('dashboard'))
        
    conn = get_db_connection()
    matchs = conn.execute("SELECT * FROM Matchs WHERE statut = 'Terminé' AND phase LIKE 'Journée%'").fetchall()
    
    stats = {eq: {'nom': eq, 'pts': 0, 'diff': 0, 'bp': 0, 'logo': DRAPEAUX.get(eq, "https://flagcdn.com/w80/un.png")} 
             for equipes in GROUPES_FIFA.values() for eq in equipes}
             
    for m in matchs:
        eq1, eq2, sc1, sc2 = m['eq1'], m['eq2'], m['vrai_score_eq1'], m['vrai_score_eq2']
        if sc1 is not None and sc2 is not None:
            if eq1 in stats: stats[eq1]['bp'] += sc1; stats[eq1]['diff'] += (sc1 - sc2)
            if eq2 in stats: stats[eq2]['bp'] += sc2; stats[eq2]['diff'] += (sc2 - sc1)
            if sc1 > sc2:
                if eq1 in stats: stats[eq1]['pts'] += 3
            elif sc1 < sc2:
                if eq2 in stats: stats[eq2]['pts'] += 3
            else:
                if eq1 in stats: stats[eq1]['pts'] += 1
                if eq2 in stats: stats[eq2]['pts'] += 1

    qualifies_directs = []
    tous_les_troisiemes = []
    
    for grp, equipes in GROUPES_FIFA.items():
        eqs = [stats[eq] for eq in equipes]
        eqs.sort(key=lambda x: (x['pts'], x['diff'], x['bp']), reverse=True)
        qualifies_directs.extend(eqs[:2])
        tous_les_troisiemes.append(eqs[2])
        
    tous_les_troisiemes.sort(key=lambda x: (x['pts'], x['diff'], x['bp']), reverse=True)
    meilleurs_troisiemes = tous_les_troisiemes[:8]
    
    les_32_equipes = qualifies_directs + meilleurs_troisiemes
    random.shuffle(les_32_equipes)

    conn.execute("DELETE FROM Matchs WHERE phase NOT LIKE 'Journée%'")
    
    for i in range(0, 32, 2):
        eqA, eqB = les_32_equipes[i], les_32_equipes[i+1]
        conn.execute('''
            INSERT INTO Matchs (phase, date, heure, eq1, logo1, eq2, logo2, statut)
            VALUES (?, 'À définir', 'À définir', ?, ?, ?, ?, 'En attente')
        ''', ("Seizièmes de finale", eqA['nom'], eqA['logo'], eqB['nom'], eqB['logo']))
        
    phases_futures = [("Huitièmes de finale", 8), ("Quarts de finale", 4), ("Demi-finales", 2), ("Finale", 1)]
    for phase, nb_matchs in phases_futures:
        for _ in range(nb_matchs):
             conn.execute('''
                INSERT INTO Matchs (phase, date, heure, eq1, logo1, eq2, logo2, statut)
                VALUES (?, 'À définir', 'À définir', 'À définir', 'https://flagcdn.com/w80/un.png', 'À définir', 'https://flagcdn.com/w80/un.png', 'En attente')
            ''', (phase,))

    conn.commit()
    conn.close()
    
    flash("Arbre des phases finales généré avec les 32 qualifiés !", "success")
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)