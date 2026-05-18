from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'esme_world_cup_2026_key'

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
    # Si l'utilisateur est déjà connecté, on l'envoie direct sur le dashboard
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    # Sinon, on lui affiche la nouvelle page d'atterrissage avec la vidéo !
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # MODIFICATION : On récupère le nom et le prénom depuis le formulaire HTML
        nom = request.form['nom']
        prenom = request.form['prenom']
        email = request.form['email']
        pw = request.form['password']
        pw_c = request.form['password_confirm']
        
        # ASTUCE ICI : On génère le pseudo automatiquement avec le début de l'email
        pseudo = email.split('@')[0]
        
        if "@" not in email or len(pw) < 8:
            flash("Email invalide ou mot de passe trop court.", "danger")
        elif pw != pw_c:
            flash("Les mots de passe ne correspondent pas.", "danger")
        else:
            conn = get_db_connection()
            try:
                # MODIFICATION : On insère nom et prenom dans la base de données
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
    if 'user_id' not in session:
        return redirect(url_for('login'))
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

    # 1. LOGIQUE MAGIQUE DU TP : On vérifie quelles phases sont terminées par l'Admin
    unlocked = {
        'huitiemes': conn.execute("SELECT count(*) as c FROM Matchs WHERE phase LIKE '%Journée%' AND statut != 'Terminé'").fetchone()['c'] == 0,
        'quarts': conn.execute("SELECT count(*) as c FROM Matchs WHERE phase LIKE '%Huitièmes%' AND statut != 'Terminé'").fetchone()['c'] == 0,
        'demis': conn.execute("SELECT count(*) as c FROM Matchs WHERE phase LIKE '%Quarts%' AND statut != 'Terminé'").fetchone()['c'] == 0,
        'finale': conn.execute("SELECT count(*) as c FROM Matchs WHERE phase LIKE '%Demi%' AND statut != 'Terminé'").fetchone()['c'] == 0
    }

    # 2. TRI PARFAIT DES MATCHS (Fini les doublons Journée 1)
    matchs = conn.execute('''
        SELECT m.*, e1.nom_pays as eq1, e1.logo as logo1, e2.nom_pays as eq2, e2.logo as logo2, p.prono_score_eq1, p.prono_score_eq2
        FROM Matchs m
        JOIN Equipes e1 ON m.id_equipe1 = e1.id
        JOIN Equipes e2 ON m.id_equipe2 = e2.id
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
    
    # On envoie les infos de déverrouillage au HTML !
    return render_template('dashboard.html', matchs=matchs, points_totaux=points_totaux, unlocked=unlocked)

@app.route('/calendrier')
def calendrier():
    if 'user_id' not in session: return redirect(url_for('login'))
    
    conn = get_db_connection()
    matchs = conn.execute('''
        SELECT m.*, 
               e1.nom_pays as eq1, e1.logo as logo1, 
               e2.nom_pays as eq2, e2.logo as logo2
        FROM Matchs m
        JOIN Equipes e1 ON m.id_equipe1 = e1.id
        JOIN Equipes e2 ON m.id_equipe2 = e2.id
        ORDER BY m.date ASC, m.heure ASC 
    ''').fetchall()  # CORRECTION : On a retiré m.phase ASC
    conn.close()
    
    return render_template('calendrier.html', matchs=matchs)

@app.route('/ranking')
def ranking():
    conn = get_db_connection()
    # MODIFICATION ICI : On sélectionne "nom" et "prenom" pour le classement des vrais joueurs
    users = conn.execute('''
        SELECT nom, prenom, points_totaux 
        FROM Utilisateurs 
        WHERE email != 'admin@esme.fr' 
        ORDER BY points_totaux DESC
    ''').fetchall()
    conn.close()
    return render_template('ranking.html', users=users)

# NOUVELLE ROUTE : Règlements ATNIL
@app.route('/reglement')
def reglement():
    return render_template('reglement.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    # 1. Sécurité : Vérifier si l'utilisateur est connecté ET si c'est l'admin
    if 'user_id' not in session or session.get('email') != 'admin@esme.fr':
        flash("Accès interdit. Vous devez être administrateur.")
        return redirect(url_for('dashboard'))
        
    conn = get_db_connection()
    
    if request.method == 'POST':
        match_id = request.form['match_id']
        vrai_s1 = int(request.form['vrai_score1'])
        vrai_s2 = int(request.form['vrai_score2'])
        
        # Enregistrer le vrai score du match et changer son statut en 'Terminé'
        conn.execute('''UPDATE Matchs 
                        SET vrai_score_eq1 = ?, vrai_score_eq2 = ?, statut = 'Terminé' 
                        WHERE id = ?''', (vrai_s1, vrai_s2, match_id))
        
        # 2. L'ALGORITHME DE CALCUL DES POINTS
        # On récupère tous les pronostics qui ont été faits sur ce match
        pronos = conn.execute('SELECT * FROM Pronostics WHERE id_match = ?', (match_id,)).fetchall()
        
        for prono in pronos:
            prono_id = prono['id']
            user_id = prono['id_utilisateur']
            p_s1 = prono['prono_score_eq1']
            p_s2 = prono['prono_score_eq2']
            
            points = 0
            # Condition A : Score exact -> 3 points
            if p_s1 == vrai_s1 and p_s2 == vrai_s2:
                points = 3
            # Condition B : Bon vainqueur ou bon match nul -> 1 point
            elif (vrai_s1 > vrai_s2 and p_s1 > p_s2) or \
                 (vrai_s1 < vrai_s2 and p_s1 < p_s2) or \
                 (vrai_s1 == vrai_s2 and p_s1 == p_s2):
                points = 1
            # Sinon -> 0 point
            else:
                points = 0
                
            # Mettre à jour les points obtenus pour ce pronostic précis
            conn.execute('UPDATE Pronostics SET points_obtenus = ? WHERE id = ?', (points, prono_id))
            
            # Recalculer instantanément les points totaux de cet utilisateur
            totaux = conn.execute('SELECT SUM(points_obtenus) as total FROM Pronostics WHERE id_utilisateur = ?', (user_id,)).fetchone()
            nouveau_total = totaux['total'] if totaux['total'] is not None else 0
            
            conn.execute('UPDATE Utilisateurs SET points_totaux = ? WHERE id = ?', (nouveau_total, user_id))
            
        conn.commit()
        flash("Match validé ! Les points des joueurs ont été mis à jour.")
        return redirect(url_for('admin'))

    # Récupérer tous les matchs pour les afficher sur la page admin
    matchs = conn.execute('''SELECT m.*, e1.nom_pays as eq1, e2.nom_pays as eq2 
                             FROM Matchs m
                             JOIN Equipes e1 ON m.id_equipe1 = e1.id
                             JOIN Equipes e2 ON m.id_equipe2 = e2.id
                             ORDER BY m.date ASC''').fetchall()
    conn.close()
    return render_template('admin.html', matchs=matchs)

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
    # En attendant le texte du prof, tu peux mettre un "Lorem Ipsum"
    return render_template('reglement.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)