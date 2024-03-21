-- USE appdb;

-- Table utilisateur
CREATE TABLE UTILISATEUR (
    id_utilisateur INT PRIMARY KEY AUTO_INCREMENT,
    prenom VARCHAR(50),
    nom VARCHAR(50)
);

-- Table TODO
CREATE TABLE TODO (
    id_todo INT PRIMARY KEY AUTO_INCREMENT,
    libelle VARCHAR(255)
    -- id_utilisateur INT,
    -- FOREIGN KEY (id_utilisateur) REFERENCES UTILISATEUR(id_utilisateur)
);

-- INSERT INTO UTILISATEUR (prenom, nom) VALUES ('Jean', 'Dupont');
-- Récupérer l'id_utilisateur généré pour le nouvel utilisateur
-- SET @last_user_id := LAST_INSERT_ID();

-- Ajouter trois tâches pour le nouvel utilisateur
-- INSERT INTO TODO (libelle, id_utilisateur) VALUES ('Acheter des carottes', @last_user_id);
-- INSERT INTO TODO (libelle, id_utilisateur) VALUES ('Acheter du beurre', @last_user_id);
-- INSERT INTO TODO (libelle, id_utilisateur) VALUES ('Renvoyer le colis', @last_user_id);

