#!/usr/bin/env python
import os
import django
import MySQLdb

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'prediction_prix_immobiliers.settings')
django.setup()

# Connexion MySQL sans spécifier de base de données
try:
    connection = MySQLdb.connect(
        host='localhost',
        user='root',
        password='',
        port=3306
    )
    cursor = connection.cursor()
    
    # Créer la base de données
    cursor.execute("CREATE DATABASE IF NOT EXISTS prediction_immobiliers CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    print("✅ Base de données 'prediction_immobiliers' créée avec succès!")
    
    cursor.close()
    connection.close()
    
except MySQLdb.Error as e:
    print(f"❌ Erreur MySQL: {e}")
    print("Assurez-vous que MySQL est démarré dans XAMPP")
