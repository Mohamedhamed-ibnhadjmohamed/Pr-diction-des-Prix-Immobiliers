#!/usr/bin/env python
"""
Script pour corriger les problèmes de migrations Django
"""
import os
import sys
import MySQLdb

# Ajouter le projet au path Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def fix_migrations():
    """Corriger les problèmes de migrations"""
    try:
        # Connexion à la base de données
        conn = MySQLdb.connect(
            host='localhost',
            user='root',
            password='',
            database='prediction_immobiliers'
        )
        cursor = conn.cursor()
        
        print("🔧 Correction des migrations en cours...")
        
        # Supprimer toutes les tables pour repartir de zéro
        tables_to_drop = [
            'django_migrations',
            'django_session',
            'django_content_type',
            'django_admin_log',
            'auth_permission',
            'auth_group_permissions',
            'auth_group',
            'auth_user_groups',
            'auth_user_user_permissions',
            'immobilier_customuser',
            'immobilier_userprofile',
            'immobilier_property',
            'immobilier_propertyfeature',
            'immobilier_prediction',
            'immobilier_favorite',
            'immobilier_message',
            'immobilier_propertyrating',
            'immobilier_searchhistory',
            'immobilier_notification',
            'immobilier_userreview',
            'immobilier_report',
            'immobilier_propertycomparison',
            'immobilier_document',
            'immobilier_recommendation'
        ]
        
        for table in tables_to_drop:
            try:
                cursor.execute(f'DROP TABLE IF EXISTS {table}')
                print(f"  ✅ Table {table} supprimée")
            except Exception as e:
                print(f"  ⚠️  Erreur suppression table {table}: {e}")
        
        conn.commit()
        
        # Supprimer le fichier de migration existant
        migration_file = 'immobilier/migrations/0001_initial.py'
        if os.path.exists(migration_file):
            os.remove(migration_file)
            print(f"  ✅ Fichier {migration_file} supprimé")
        
        cursor.close()
        conn.close()
        
        print("✅ Nettoyage terminé. Vous pouvez maintenant exécuter:")
        print("   python manage.py makemigrations")
        print("   python manage.py migrate")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    fix_migrations()
