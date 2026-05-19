DROP TABLE IF EXISTS Utilisateurs;
DROP TABLE IF EXISTS Matchs;
DROP TABLE IF EXISTS Pronostics;

CREATE TABLE Utilisateurs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    prenom TEXT NOT NULL,
    pseudo TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    mot_de_passe_hash TEXT NOT NULL,
    points_totaux INTEGER DEFAULT 0
);

CREATE TABLE Matchs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    phase TEXT NOT NULL,
    date TEXT NOT NULL,
    heure TEXT NOT NULL,
    eq1 TEXT NOT NULL,
    logo1 TEXT NOT NULL,
    eq2 TEXT NOT NULL,
    logo2 TEXT NOT NULL,
    vrai_score_eq1 INTEGER,
    vrai_score_eq2 INTEGER,
    statut TEXT DEFAULT 'En attente'
);

CREATE TABLE Pronostics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_utilisateur INTEGER,
    id_match INTEGER,
    prono_score_eq1 INTEGER,
    prono_score_eq2 INTEGER,
    points_obtenus INTEGER DEFAULT 0,
    FOREIGN KEY (id_utilisateur) REFERENCES Utilisateurs(id),
    FOREIGN KEY (id_match) REFERENCES Matchs(id)