from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
import random

app = Flask(__name__)
app.secret_key = 'projet_world_cup_2026_key'

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

    # CORRECTION : On lit directement les matchs sans faire de JOIN avec une vieille table
    matchs = conn.execute('''
        SELECT m.*, p.prono_score_eq1, p.prono_score_eq2
        FROM Matchs m
        LEFT JOIN Pronostics p ON m.id = p.id_match AND p.id_utilisateur = ?
        ORDER BY 
            CASE 
                WHEN m.phase LIKE '%Journée 1%' THEN 1
                WHEN m.phase LIKE '%Journée 2%' THEN 2
                WHEN m.phase LIKE '%Journée 3%' THEN 3
                WHEN m.phase LIKE '%Huitièmes%' THEN 4
                WHEN m.phase LIKE '%Quarts%' THEN 5
                WHEN m.phase LIKE '%Demi%' THEN 6
                WHEN m.phase LIKE '%Petite finale%' THEN 7
                WHEN m.phase LIKE '%Finale%' THEN 8
                ELSE 9
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
    # CORRECTION : Idem, lecture directe
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
        score1 = random.randint(0, 5) # MODIFICATION : Scores de 0 à 5
        score2 = random.randint(0, 5)
        conn.execute("UPDATE Matchs SET vrai_score_eq1 = ?, vrai_score_eq2 = ?, statut = 'Terminé' WHERE id = ?", (score1, score2, m['id']))
        
    conn.commit()
    conn.close()
    flash(f"🎲 Scores générés aléatoirement pour la {phase} !", "success")
    return redirect(url_for('admin'))

@app.route('/groupes')
def groupes():
    conn = get_db_connection()
    # On récupère tous les matchs terminés pour calculer les points
    matchs = conn.execute("SELECT * FROM Matchs WHERE statut = 'Terminé' AND phase LIKE 'Journée%'").fetchall()
    # On récupère tous les drapeaux de la BDD pour l'affichage
    tous_les_matchs = conn.execute("SELECT eq1, logo1, eq2, logo2 FROM Matchs").fetchall()
    conn.close()

    groupes_fifa = {
        'Groupe A': ['Mexique', 'Afrique du Sud', 'Corée du Sud', 'Europe D'],
        'Groupe B': ['Canada', 'Europe A', 'Qatar', 'Suisse'],
        'Groupe C': ['Brésil', 'Maroc', 'Haïti', 'Écosse'],
        'Groupe D': ['États-Unis', 'Paraguay', 'Australie', 'Europe C'],
        'Groupe E': ['Allemagne', 'Curaçao', "Côte d'Ivoire", 'Équateur'],
        'Groupe F': ['Pays-Bas', 'Japon', 'Europe B', 'Tunisie'],
        'Groupe G': ['Belgique', 'Égypte', 'Iran', 'Nouvelle-Zélande'],
        'Groupe H': ['Espagne', 'Arabie saoudite', 'Uruguay', 'Cap-Vert'],
        'Groupe I': ['France', 'Sénégal', 'Fifa 2', 'Norvège'],
        'Groupe J': ['Argentine', 'Algérie', 'Jordanie', 'Autriche'],
        'Groupe K': ['Portugal', 'Fifa 1', 'Ouzbékistan', 'Colombie'],
        'Groupe L': ['Angleterre', 'Croatie', 'Panama', 'Ghana']
    }

    logos = {}
    for m in tous_les_matchs:
        if m['eq1'] not in logos: logos[m['eq1']] = m['logo1']
        if m['eq2'] not in logos: logos[m['eq2']] = m['logo2']

    stats = {}
    for grp, equipes in groupes_fifa.items():
        for eq in equipes:
            stats[eq] = {'nom': eq, 'groupe': grp, 'pts': 0, 'mj': 0, 'g': 0, 'n': 0, 'p': 0, 'bp': 0, 'bc': 0, 'diff': 0, 'logo': logos.get(eq, "https://flagcdn.com/w80/un.png")}

    # L'ALGORITHME DE CALCUL FIFA
    for m in matchs:
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

    # Tri des poules : 1. Points, 2. Différence de Buts, 3. Buts Pour
    classement_final = {}
    for grp, equipes in groupes_fifa.items():
        eqs = [stats[eq] for eq in equipes]
        eqs.sort(key=lambda x: (x['pts'], x['diff'], x['bp']), reverse=True)
        classement_final[grp] = eqs

    return render_template('groupes.html', classement=classement_final)

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)