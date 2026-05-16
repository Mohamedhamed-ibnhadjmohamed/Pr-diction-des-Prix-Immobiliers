import MySQLdb
import json
from datetime import datetime, timedelta

# Connexion à la base de données
conn = MySQLdb.connect(host='localhost', user='root', password='', database='prediction_immobiliers')
cursor = conn.cursor()

print("🚀 Insertion des données d'exemple...")

# 1. Insertion des utilisateurs
print("\n📋 Insertion des utilisateurs...")
users_data = [
    (1, 'mohamed.benali@email.com', 'Mohamed', 'Ben Ali', 'agent', '216 22 123 456', 1),
    (2, 'sarra.mansour@email.com', 'Sarra', 'Mansour', 'vendeur', '216 71 987 654', 1),
    (3, 'karim.trabelsi@email.com', 'Karim', 'Trabelsi', 'acheteur', '216 55 456 789', 0),
    (4, 'leila.hammami@email.com', 'Leila', 'Hammami', 'acheteur', '216 98 321 654', 1),
    (5, 'nizar.khaled@email.com', 'Nizar', 'Khaled', 'agent', '216 23 789 456', 1),
    (6, 'rym.baccouche@email.com', 'Rym', 'Baccouche', 'vendeur', '216 41 654 321', 1),
    (7, 'amine.gharbi@email.com', 'Amine', 'Gharbi', 'acheteur', '216 76 123 987', 0),
    (8, 'mariem.saidi@email.com', 'Mariem', 'Saidi', 'vendeur', '216 50 789 123', 1),
    (9, 'walid.bensalem@email.com', 'Walid', 'Ben Salem', 'acheteur', '216 29 456 789', 0),
    (10, 'imen.mansouri@email.com', 'Imen', 'Mansouri', 'agent', '216 94 321 654', 1)
]

for user in users_data:
    try:
        cursor.execute("""
            INSERT INTO customuser (id, email, first_name, last_name, role, phone, is_verified, created_at, date_joined, is_active, is_staff, is_superuser, username)
            VALUES (%s, %s, %s, %s, %s, %s, %s, NOW(), NOW(), 1, 0, 0, %s)
        """, (user[0], user[1], user[2], user[3], user[4], user[5], user[6], user[1]))
        print(f"  ✅ {user[1]}")
    except Exception as e:
        print(f"  ⚠️ Erreur {user[1]}: {e}")

# 2. Insertion des propriétés
print("\n🏠 Insertion des propriétés...")
properties_data = [
    (1, 'Appartement spacieux au centre-ville', 'appartement', 'Avenue Habib Bourguiba, Centre Ville', 'Tunis', '1000', 120.0, 3, 2, 1, 'Bel appartement de 120m² avec balcon et vue sur la ville', 450000.00, 2),
    (2, 'Villa moderne avec piscine', 'villa', 'Rue du Lac, Les Berges du Lac', 'Tunis', '1053', 350.0, 5, 4, 3, 'Superbe villa avec jardin et piscine privée', 1200000.00, 6),
    (3, 'Studio meublé à Sfax', 'studio', 'Avenue Farhat Hached', 'Sfax', '3000', 45.0, 1, 1, 1, 'Studio entièrement meublé idéal pour étudiant', 180000.00, 8),
    (4, 'Maison traditionnelle à Sousse', 'maison', 'Rue Medina', 'Sousse', '4000', 200.0, 4, 3, 2, 'Maison de caractère avec patio traditionnel', 550000.00, 6),
    (5, 'Appartement de luxe à Gammarth', 'appartement', 'Rue de la Corniche', 'Tunis', '2026', 180.0, 4, 3, 2, 'Appartement haut de gamme avec vue mer', 750000.00, 1),
    (6, 'Terrain constructible à Kairouan', 'terrain', 'Zone Industrielle Nord', 'Kairouan', '3100', 500.0, 0, 0, 0, 'Terrain plat de 500m² prêt à construire', 150000.00, 6),
    (7, 'Duplex à Monastir', 'appartement', 'Avenue Bourguiba', 'Monastir', '5000', 150.0, 4, 3, 2, 'Duplex lumineux avec terrasse privative', 380000.00, 10),
    (8, 'Maison avec jardin à Bizerte', 'maison', 'Rue de la Marine', 'Bizerte', '7000', 250.0, 5, 4, 2, 'Belle maison avec grand jardin et garage', 420000.00, 8),
    (9, 'Studio économique à Tunis', 'studio', 'Rue El Menzah', 'Tunis', '1004', 35.0, 1, 1, 1, 'Petit studio idéal pour premier investissement', 120000.00, 2),
    (10, 'Penthouse de luxe à Les Berges du Lac', 'appartement', 'Immeuble Le Palais', 'Tunis', '1053', 220.0, 4, 3, 2, 'Penthouse exceptionnel avec rooftop privé', 950000.00, 5)
]

for prop in properties_data:
    try:
        cursor.execute("""
            INSERT INTO property (id, title, property_type, address, city, postal_code, surface, rooms, bedrooms, bathrooms, description, price, created_by_id, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
        """, prop)
        print(f"  ✅ {prop[1]}")
    except Exception as e:
        print(f"  ⚠️ Erreur {prop[1]}: {e}")

# 3. Insertion des caractéristiques
print("\n⚙️ Insertion des caractéristiques...")
features_data = [
    (1, 1, 0, 0, 0, 1, 1, 3, 8, 2010, 'C'),
    (2, 2, 1, 1, 1, 1, 0, 0, 2, 2015, 'B'),
    (3, 3, 0, 0, 0, 1, 1, 5, 6, 2018, 'B'),
    (4, 4, 1, 0, 1, 0, 0, 0, 1, 2005, 'D'),
    (5, 5, 0, 1, 1, 1, 1, 8, 10, 2020, 'A'),
    (6, 6, 0, 0, 0, 0, 0, 0, 0, 0, 'N/A'),
    (7, 7, 0, 0, 0, 1, 1, 4, 5, 2012, 'C'),
    (8, 8, 1, 0, 1, 1, 0, 0, 1, 2008, 'D'),
    (9, 9, 0, 0, 0, 0, 1, 2, 4, 2016, 'B'),
    (10, 10, 0, 1, 1, 1, 1, 10, 12, 2022, 'A')
]

for feature in features_data:
    try:
        cursor.execute("""
            INSERT INTO propertyfeature (id, property_id, has_garden, has_pool, has_garage, has_balcony, has_elevator, floor, total_floors, construction_year, energy_efficiency)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, feature)
        print(f"  ✅ Caractéristiques propriété {feature[1]}")
    except Exception as e:
        print(f"  ⚠️ Erreur caractéristiques {feature[1]}: {e}")

# 4. Insertion des prédictions
print("\n🤖 Insertion des prédictions...")
predictions_data = [
    (1, 1, 465000.00, 0.85, 'v2.1.0'),
    (2, 2, 1180000.00, 0.92, 'v2.1.0'),
    (3, 3, 175000.00, 0.78, 'v2.1.0'),
    (4, 4, 560000.00, 0.88, 'v2.1.0'),
    (5, 5, 780000.00, 0.90, 'v2.1.0'),
    (6, 6, 145000.00, 0.75, 'v2.1.0'),
    (7, 7, 390000.00, 0.82, 'v2.1.0'),
    (8, 8, 435000.00, 0.86, 'v2.1.0'),
    (9, 9, 125000.00, 0.80, 'v2.1.0'),
    (10, 10, 980000.00, 0.94, 'v2.1.0')
]

for pred in predictions_data:
    try:
        cursor.execute("""
            INSERT INTO prediction (id, property_id, predicted_price, confidence_score, model_version, created_at)
            VALUES (%s, %s, %s, %s, %s, NOW())
        """, pred)
        print(f"  ✅ Prédiction propriété {pred[1]}")
    except Exception as e:
        print(f"  ⚠️ Erreur prédiction {pred[1]}: {e}")

# 5. Insertion des favoris
print("\n❤️ Insertion des favoris...")
favorites_data = [
    (1, 3, 1),
    (2, 4, 2),
    (3, 3, 5),
    (4, 7, 3),
    (5, 9, 8),
    (6, 4, 10),
    (7, 7, 7),
    (8, 3, 4),
    (9, 9, 9),
    (10, 7, 6)
]

for fav in favorites_data:
    try:
        cursor.execute("""
            INSERT INTO favorite (id, user_id, property_id, created_at)
            VALUES (%s, %s, %s, NOW())
        """, fav)
        print(f"  ✅ Favori utilisateur {fav[1]} - propriété {fav[2]}")
    except Exception as e:
        print(f"  ⚠️ Erreur favori {fav[1]}-{fav[2]}: {e}")

conn.commit()

# 6. Insertion des messages
print("\n💬 Insertion des messages...")
messages_data = [
    (1, 3, 1, 1, 'Question sur l\'appartement', 'Bonjour, je suis intéressé par votre appartement. Est-il encore disponible ?', 0),
    (2, 1, 3, 1, 'Re: Question appartement', 'Bonjour Oui, l\'appartement est toujours disponible. Quand souhaitez-vous le visiter ?', 1),
    (3, 4, 5, 2, 'Visite villa', 'Bonjour, j\'aimerais visiter la villa. Samedi prochain serait-il possible ?', 0),
    (4, 7, 2, 3, 'Prix du studio', 'Bonjour, le prix est-il négociable ? Je suis très intéressé.', 1),
    (5, 9, 8, 8, 'Maison avec jardin', 'Bonjour, quelles sont les caractéristiques exactes du jardin ?', 0)
]

for msg in messages_data:
    try:
        cursor.execute("""
            INSERT INTO message (id, sender_id, recipient_id, property_id, subject, content, is_read, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
        """, msg)
        print(f"  ✅ Message de {msg[1]} à {msg[2]}")
    except Exception as e:
        print(f"  ⚠️ Erreur message {msg[1]}-{msg[2]}: {e}")

conn.commit()

print("\n🎉 Données insérées avec succès!")

# Vérification
print("\n📊 Vérification des données insérées:")
tables = ['customuser', 'property', 'propertyfeature', 'prediction', 'favorite', 'message']
for table in tables:
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    count = cursor.fetchone()[0]
    print(f"  ✓ {table}: {count} lignes")

cursor.close()
conn.close()
