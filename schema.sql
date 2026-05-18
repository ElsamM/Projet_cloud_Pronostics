DROP TABLE IF EXISTS Pronostics;
DROP TABLE IF EXISTS Matchs;
DROP TABLE IF EXISTS Equipes;
DROP TABLE IF EXISTS Utilisateurs;


CREATE TABLE IF NOT EXISTS Utilisateurs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    prenom TEXT NOT NULL,
    pseudo TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    mot_de_passe_hash TEXT NOT NULL,
    points_totaux INTEGER DEFAULT 0
);


CREATE TABLE Equipes (
    id INTEGER PRIMARY KEY, -- On enlève AUTOINCREMENT car on va utiliser les vrais IDs de l'API
    nom_pays TEXT NOT NULL,
    groupe TEXT DEFAULT 'À définir',
    logo TEXT -- LA NOUVELLE COLONNE EST ICI !
);


CREATE TABLE Matchs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_equipe1 INTEGER,
    id_equipe2 INTEGER,
    date TEXT,
    heure TEXT,
    phase TEXT,
    vrai_score_eq1 INTEGER DEFAULT NULL,
    vrai_score_eq2 INTEGER DEFAULT NULL,
    statut TEXT DEFAULT 'ouvert',
    FOREIGN KEY(id_equipe1) REFERENCES Equipes(id),
    FOREIGN KEY(id_equipe2) REFERENCES Equipes(id)
);

CREATE TABLE Pronostics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_utilisateur INTEGER,
    id_match INTEGER,
    prono_score_eq1 INTEGER,
    prono_score_eq2 INTEGER,
    points_obtenus INTEGER DEFAULT 0,
    UNIQUE(id_utilisateur, id_match),
    FOREIGN KEY(id_utilisateur) REFERENCES Utilisateurs(id),
    FOREIGN KEY(id_match) REFERENCES Matchs(id)
);

-- Insertion des 48 équipes (Exemple Groupes A et B)
INSERT INTO Equipes (nom_pays, groupe) VALUES 
('France', 'A'), ('Maroc', 'A'), ('Japon', 'A'), ('Pérou', 'A'),
('Brésil', 'B'), ('Croatie', 'B'), ('Sénégal', 'B'), ('Australie', 'B');