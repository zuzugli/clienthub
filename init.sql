-- Exécuté automatiquement par MySQL au PREMIER démarrage (volume de données vide)

-- Lire ce fichier en UTF-8 (pour les accents)
SET NAMES utf8mb4;

CREATE TABLE IF NOT EXISTS clients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

INSERT INTO clients (name) VALUES
    ('Alice Martin'),
    ('Bob Durand'),
    ('Chloé Bernard');
