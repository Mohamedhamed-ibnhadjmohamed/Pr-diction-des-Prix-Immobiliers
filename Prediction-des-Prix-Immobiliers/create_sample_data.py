#!/usr/bin/env python
"""
Script pour créer des données d'exemple pour toutes les tables
"""
import MySQLdb
from datetime import datetime, timedelta

def create_sample_data():
    """Créer des données d'exemple pour tester l'application"""
    try:
        print("🚀 Création des données d'exemple...")
        
        # Connexion à la base de données
        conn = MySQLdb.connect(
            host='localhost',
            user='root',
            password='',
            database='prediction_immobiliers'
        )
        cursor = conn.cursor()
        
        # 1. Créer les utilisateurs
        print("\n👥 Création des utilisateurs...")
        users = [
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
        
        for user in users:
            try:
                cursor.execute("""
                    INSERT INTO customuser (id, email, first_name, last_name, role, phone, is_verified, 
                                         created_at, date_joined, is_active, is_staff, is_superuser, 
                                         username, password)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, NOW(), NOW(), 1, 0, 0, %s, 'password123')
                """, (user[0], user[1], user[2], user[3], user[4], user[5], user[6], user[1]))
                print(f"  ✅ {user[1]}")
            except Exception as e:
                if "Duplicate" not in str(e):
                    print(f"  ⚠️ Erreur {user[1]}: {e}")
        
        # 2. Créer les propriétés
        print("\n🏠 Création des propriétés...")
        properties = [
            (1, 'Appartement spacieux au centre-ville', 'appartement', 'Avenue Habib Bourguiba, Centre Ville', 'Tunis', '1000', 120.0, 3, 2, 1, 'Bel appartement de 120m² avec balcon et vue sur la ville', 450000.00, 2),
            (2, 'Villa moderne avec piscine', 'villa', 'Rue du Lac, Les Berges du Lac', 'Tunis', '1053', 350.0, 5, 4, 3, 'Superbe villa avec jardin et piscine privée', 1200000.00, 6),
            (3, 'Studio meublé à Sfax', 'studio', 'Avenue Farhat Hached', 'Sfax', '3000', 45.0, 1, 1, 1, 'Studio entièrement meublé idéal pour étudiant ou jeune professionnel', 180000.00, 8),
            (4, 'Maison traditionnelle à Sousse', 'maison', 'Rue Medina', 'Sousse', '4000', 200.0, 4, 3, 2, 'Maison de caractère avec patio traditionnel', 550000.00, 6),
            (5, 'Appartement de luxe à Gammarth', 'appartement', 'Rue de la Corniche', 'Tunis', '2026', 180.0, 4, 3, 2, 'Appartement haut de gamme avec vue mer', 750000.00, 1),
            (6, 'Terrain constructible à Kairouan', 'terrain', 'Zone Industrielle Nord', 'Kairouan', '3100', 500.0, 0, 0, 0, 'Terrain plat de 500m² prêt à construire', 150000.00, 6),
            (7, 'Duplex à Monastir', 'appartement', 'Avenue Bourguiba', 'Monastir', '5000', 150.0, 4, 3, 2, 'Duplex lumineux avec terrasse privative', 380000.00, 10),
            (8, 'Maison avec jardin à Bizerte', 'maison', 'Rue de la Marine', 'Bizerte', '7000', 250.0, 5, 4, 2, 'Belle maison avec grand jardin et garage', 420000.00, 8),
            (9, 'Studio économique à Tunis', 'studio', 'Rue El Menzah', 'Tunis', '1004', 35.0, 1, 1, 1, 'Petit studio idéal pour premier investissement', 120000.00, 2),
            (10, 'Penthouse de luxe à Les Berges du Lac', 'appartement', 'Immeuble Le Palais', 'Tunis', '1053', 220.0, 4, 3, 2, 'Penthouse exceptionnel avec rooftop privé', 950000.00, 5)
        ]
        
        for prop in properties:
            try:
                cursor.execute("""
                    INSERT INTO property (id, title, property_type, address, city, postal_code, surface, 
                                       rooms, bedrooms, bathrooms, description, price, created_by_id, 
                                       created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
                """, prop)
                print(f"  ✅ {prop[1]}")
            except Exception as e:
                if "Duplicate" not in str(e):
                    print(f"  ⚠️ Erreur {prop[1]}: {e}")
        
        conn.commit()
        
        # 3. Créer les caractéristiques
        print("\n⚙️ Création des caractéristiques...")
        features = [
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
        
        for feature in features:
            try:
                cursor.execute("""
                    INSERT INTO propertyfeature (id, property_id, has_garden, has_pool, has_garage, 
                                              has_balcony, has_elevator, floor, total_floors, 
                                              construction_year, energy_efficiency)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, feature)
                print(f"  ✅ Caractéristiques propriété {feature[1]}")
            except Exception as e:
                if "Duplicate" not in str(e):
                    print(f"  ⚠️ Erreur caractéristiques {feature[1]}: {e}")
        
        # 4. Créer les prédictions
        print("\n🤖 Création des prédictions...")
        predictions = [
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
        
        for pred in predictions:
            try:
                cursor.execute("""
                    INSERT INTO prediction (id, property_id, predicted_price, confidence_score, 
                                         model_version, created_at)
                    VALUES (%s, %s, %s, %s, %s, NOW())
                """, pred)
                print(f"  ✅ Prédiction propriété {pred[1]}")
            except Exception as e:
                if "Duplicate" not in str(e):
                    print(f"  ⚠️ Erreur prédiction {pred[1]}: {e}")
        
        conn.commit()
        
        # 5. Créer les favoris
        print("\n❤️ Création des favoris...")
        favorites = [
            (1, 3, 1), (2, 4, 2), (3, 3, 5), (4, 7, 3), (5, 9, 8),
            (6, 4, 10), (7, 7, 7), (8, 3, 4), (9, 9, 9), (10, 7, 6)
        ]
        
        for fav in favorites:
            try:
                cursor.execute("""
                    INSERT INTO favorite (id, user_id, property_id, created_at)
                    VALUES (%s, %s, %s, NOW())
                """, fav)
                print(f"  ✅ Favori utilisateur {fav[1]} - propriété {fav[2]}")
            except Exception as e:
                if "Duplicate" not in str(e):
                    print(f"  ⚠️ Erreur favori {fav[1]}-{fav[2]}: {e}")
        
        conn.commit()
        
        # 6. Créer les messages
        print("\n💬 Création des messages...")
        messages = [
            (1, 3, 1, 1, 'Question sur l\'appartement', 'Bonjour, je suis intéressé par votre appartement. Est-il encore disponible ?', 0),
            (2, 1, 3, 1, 'Re: Question appartement', 'Bonjour Oui, l\'appartement est toujours disponible. Quand souhaitez-vous le visiter ?', 1),
            (3, 4, 5, 2, 'Visite villa', 'Bonjour, j\'aimerais visiter la villa. Samedi prochain serait-il possible ?', 0),
            (4, 7, 2, 3, 'Prix du studio', 'Bonjour, le prix est-il négociable ? Je suis très intéressé.', 1),
            (5, 9, 8, 8, 'Maison avec jardin', 'Bonjour, quelles sont les caractéristiques exactes du jardin ?', 0),
            (6, 4, 10, 10, 'Penthouse de luxe', 'Bonjour, y a-t-il des frais de copropriété mensuels ?', 1),
            (7, 3, 6, 4, 'Maison traditionnelle', 'Bonjour, la maison nécessite-t-elle des travaux ?', 0),
            (8, 7, 1, 5, 'Appartement Gammarth', 'Bonjour, y a-t-il une place de parking incluse ?', 1),
            (9, 9, 2, 9, 'Studio économique', 'Bonjour, quel est le montant des charges mensuelles ?', 0),
            (10, 4, 5, 2, 'Proposition d\'achat', 'Bonjour, je souhaite faire une offre de 1150000 DT pour la villa.', 1)
        ]
        
        for msg in messages:
            try:
                cursor.execute("""
                    INSERT INTO message (id, sender_id, recipient_id, property_id, subject, 
                                      content, is_read, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
                """, msg)
                print(f"  ✅ Message de {msg[1]} à {msg[2]}")
            except Exception as e:
                if "Duplicate" not in str(e):
                    print(f"  ⚠️ Erreur message {msg[1]}-{msg[2]}: {e}")
        
        conn.commit()
        
        # 7. Créer les évaluations
        print("\n⭐ Création des évaluations...")
        ratings = [
            (1, 3, 1, 4, 'Bel appartement bien situé, mais un peu cher'),
            (2, 4, 2, 5, 'Villa exceptionnelle, très belle piscine'),
            (3, 7, 3, 3, 'Studio correct mais un peu petit'),
            (4, 9, 8, 4, 'Belle maison avec grand jardin, bien entretenue'),
            (5, 4, 10, 5, 'Penthouse de luxe, vue imprenable sur la mer'),
            (6, 7, 7, 4, 'Duplex bien agencé, terrasse agréable'),
            (7, 3, 4, 3, 'Maison de caractère mais nécessite quelques rénovations'),
            (8, 9, 9, 2, 'Studio très petit, pas très lumineux'),
            (9, 7, 5, 5, 'Appartement de luxe avec services premium'),
            (10, 3, 6, 4, 'Bon terrain bien situé, prêt à construire')
        ]
        
        for rating in ratings:
            try:
                cursor.execute("""
                    INSERT INTO propertyrating (id, user_id, property_id, rating, comment, created_at)
                    VALUES (%s, %s, %s, %s, %s, NOW())
                """, rating)
                print(f"  ✅ Évaluation propriété {rating[2]} par utilisateur {rating[1]}")
            except Exception as e:
                if "Duplicate" not in str(e):
                    print(f"  ⚠️ Erreur évaluation {rating[1]}-{rating[2]}: {e}")
        
        conn.commit()
        
        # 8. Créer les historiques de recherche
        print("\n🔍 Création des historiques de recherche...")
        searches = [
            (1, 3, '{"city": "Tunis", "property_type": "appartement", "min_price": 300000, "max_price": 500000}', 15),
            (2, 4, '{"city": "Tunis", "property_type": "villa", "min_price": 1000000}', 8),
            (3, 7, '{"city": "Sfax", "property_type": "studio", "max_price": 200000}', 12),
            (4, 9, '{"city": "Bizerte", "property_type": "maison", "min_surface": 200}', 6),
            (5, 3, '{"property_type": "terrain", "max_price": 200000}', 10),
            (6, 4, '{"city": "Tunis", "has_pool": true, "min_surface": 150}', 7),
            (7, 7, '{"city": "Monastir", "property_type": "appartement"}', 9),
            (8, 9, '{"city": "Sousse", "property_type": "maison", "min_bedrooms": 3}', 5),
            (9, 3, '{"city": "Tunis", "property_type": "studio", "max_price": 150000}', 18),
            (10, 7, '{"min_surface": 100, "max_price": 400000}', 22)
        ]
        
        for search in searches:
            try:
                cursor.execute("""
                    INSERT INTO searchhistory (id, user_id, query_params, results_count, created_at)
                    VALUES (%s, %s, %s, %s, NOW())
                """, search)
                print(f"  ✅ Historique recherche utilisateur {search[1]}")
            except Exception as e:
                if "Duplicate" not in str(e):
                    print(f"  ⚠️ Erreur historique {search[1]}: {e}")
        
        conn.commit()
        
        # 9. Créer les notifications
        print("\n🔔 Création des notifications...")
        notifications = [
            (1, 1, 'message', 'Nouveau message', 'Vous avez reçu un nouveau message concernant votre appartement', 0, 1, 3),
            (2, 3, 'message', 'Réponse à votre question', 'L\'agent a répondu à votre question sur l\'appartement', 1, 1, 1),
            (3, 5, 'favorite', 'Bien ajouté aux favoris', 'Quelqu\'un a ajouté votre villa à ses favoris', 0, 2, 4),
            (4, 2, 'message', 'Nouvelle demande de visite', 'Un acheteur souhaite visiter votre studio', 1, 3, 7),
            (5, 8, 'rating', 'Nouvelle évaluation', 'Votre maison a reçu une nouvelle évaluation', 0, 8, 9),
            (6, 10, 'message', 'Demande d\'information', 'Un acheteur a des questions sur votre penthouse', 1, 10, 4),
            (7, 6, 'favorite', 'Nouveau favori', 'Votre maison traditionnelle est dans les favoris', 0, 4, 3),
            (8, 1, 'message', 'Question sur parking', 'Un acheteur demande sur le parking de l\'appartement', 1, 5, 7),
            (9, 2, 'message', 'Question sur charges', 'Quelqu\'un demande sur les charges du studio', 0, 9, 9),
            (10, 5, 'message', 'Proposition d\'achat', 'Vous avez reçu une offre d\'achat pour votre villa', 1, 2, 4)
        ]
        
        for notif in notifications:
            try:
                cursor.execute("""
                    INSERT INTO notification (id, user_id, notification_type, title, message, 
                                           is_read, property_id, sender_id, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW())
                """, notif)
                print(f"  ✅ Notification pour utilisateur {notif[1]}")
            except Exception as e:
                if "Duplicate" not in str(e):
                    print(f"  ⚠️ Erreur notification {notif[1]}: {e}")
        
        conn.commit()
        
        # 10. Créer les autres tables (userreview, report, document, recommendation, propertycomparison)
        print("\n📋 Création des autres tables...")
        
        # User reviews
        reviews = [
            (1, 3, 1, 5, 'Excellent agent, très professionnel et disponible', 1),
            (2, 4, 5, 4, 'Bon agent, a bien compris mes besoins', 1),
            (3, 7, 2, 3, 'Vendeur correct mais un peu lent à répondre', 0),
            (4, 9, 8, 5, 'Vendeur très arrangeant et honnête', 1),
            (5, 4, 10, 5, 'Agent exceptionnel, a trouvé le bien parfait', 1)
        ]
        
        for review in reviews:
            try:
                cursor.execute("""
                    INSERT INTO userreview (id, reviewer_id, reviewed_user_id, rating, comment, is_verified, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s, NOW())
                """, review)
                print(f"  ✅ Avis utilisateur {review[2]}")
            except Exception as e:
                if "Duplicate" not in str(e):
                    print(f"  ⚠️ Erreur avis {review[2]}: {e}")
        
        conn.commit()
        
        # Vérification finale
        print("\n📊 Vérification finale des données:")
        tables_to_check = [
            'customuser', 'property', 'propertyfeature', 'prediction', 
            'favorite', 'message', 'propertyrating', 'searchhistory', 
            'notification', 'userreview'
        ]
        
        for table in tables_to_check:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"  ✓ {table}: {count} lignes")
        
        cursor.close()
        conn.close()
        
        print("\n🎉 Données d'exemple créées avec succès!")
        print("\n📋 Résumé des données créées:")
        print("  • 10 utilisateurs (agents, vendeurs, acheteurs)")
        print("  • 10 propriétés (appartements, villas, studios, maisons, terrains)")
        print("  • 10 caractéristiques de propriétés")
        print("  • 10 prédictions de prix")
        print("  • 10 favoris")
        print("  • 10 messages entre utilisateurs")
        print("  • 10 évaluations de propriétés")
        print("  • 10 historiques de recherche")
        print("  • 10 notifications")
        print("  • 5 avis utilisateurs")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    create_sample_data()
