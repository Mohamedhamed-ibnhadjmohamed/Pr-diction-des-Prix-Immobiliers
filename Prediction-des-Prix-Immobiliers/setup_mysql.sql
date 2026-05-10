-- Script de configuration pour la base de données MySQL
-- Créez cette base de données avant de lancer les migrations Django

-- Création de la base de données
CREATE DATABASE IF NOT EXISTS prediction_immobiliers 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- Afficher les bases de données pour vérification
SHOW DATABASES;

-- Utiliser la base de données
USE prediction_immobiliers;
