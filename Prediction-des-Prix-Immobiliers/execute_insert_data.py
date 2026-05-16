#!/usr/bin/env python
"""
Script pour exécuter le fichier SQL d'insertion de données d'exemple
"""
import MySQLdb
import os

def execute_sql_file():
    """Exécuter le fichier SQL d'insertion de données"""
    try:
        print("🚀 Insertion des données d'exemple en cours...")
        
        # Connexion à la base de données
        conn = MySQLdb.connect(
            host='localhost',
            user='root',
            password='',
            database='prediction_immobiliers'
        )
        cursor = conn.cursor()
        
        # Lire le fichier SQL
        sql_file = 'insert_sample_data.sql'
        if not os.path.exists(sql_file):
            print(f"❌ Fichier {sql_file} introuvable")
            return False
        
        with open(sql_file, 'r', encoding='utf-8') as file:
            sql_content = file.read()
        
        # Exécuter les commandes SQL
        sql_commands = sql_content.split(';')
        
        for i, command in enumerate(sql_commands):
            command = command.strip()
            if command and not command.startswith('--'):
                try:
                    cursor.execute(command)
                    if i < len(sql_commands) - 2:  # Ne pas afficher la commande SELECT finale
                        print(f"  ✅ Commande {i+1} exécutée")
                except Exception as e:
                    if "already exists" not in str(e) and "Duplicate entry" not in str(e):
                        print(f"  ⚠️  Erreur commande {i+1}: {e}")
        
        conn.commit()
        
        # Afficher le résumé
        print("\n📊 Résumé de l'insertion:")
        cursor.execute("""
            SELECT 
                'customuser' as table_name, COUNT(*) as row_count FROM customuser
            UNION ALL
            SELECT 'userprofile', COUNT(*) FROM userprofile
            UNION ALL
            SELECT 'property', COUNT(*) FROM property
            UNION ALL
            SELECT 'propertyfeature', COUNT(*) FROM propertyfeature
            UNION ALL
            SELECT 'prediction', COUNT(*) FROM prediction
            UNION ALL
            SELECT 'favorite', COUNT(*) FROM favorite
            UNION ALL
            SELECT 'message', COUNT(*) FROM message
            UNION ALL
            SELECT 'propertyrating', COUNT(*) FROM propertyrating
            UNION ALL
            SELECT 'searchhistory', COUNT(*) FROM searchhistory
            UNION ALL
            SELECT 'notification', COUNT(*) FROM notification
            UNION ALL
            SELECT 'userreview', COUNT(*) FROM userreview
            UNION ALL
            SELECT 'report', COUNT(*) FROM report
            UNION ALL
            SELECT 'propertycomparison', COUNT(*) FROM propertycomparison
            UNION ALL
            SELECT 'document', COUNT(*) FROM document
            UNION ALL
            SELECT 'recommendation', COUNT(*) FROM recommendation
        """)
        
        results = cursor.fetchall()
        for table_name, count in results:
            print(f"  ✓ {table_name}: {count} lignes")
        
        cursor.close()
        conn.close()
        
        print("\n🎉 Données d'exemple insérées avec succès!")
        print("\n📋 Données créées:")
        print("  • 10 utilisateurs avec différents rôles (agent, vendeur, acheteur)")
        print("  • 10 propriétés (appartements, villas, studios, maisons, terrains)")
        print("  • 10 caractéristiques de propriétés")
        print("  • 10 prédictions de prix")
        print("  • 10 favoris")
        print("  • 10 messages entre utilisateurs")
        print("  • 10 évaluations de propriétés")
        print("  • 10 historiques de recherche")
        print("  • 10 notifications")
        print("  • 10 avis utilisateurs")
        print("  • 10 signalements")
        print("  • 10 comparaisons de propriétés")
        print("  • 10 documents")
        print("  • 10 recommandations")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    execute_sql_file()
