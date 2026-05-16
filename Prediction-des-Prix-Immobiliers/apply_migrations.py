#!/usr/bin/env python
"""
Script pour appliquer les nouvelles migrations avec les noms de tables modifiés
"""
import os
import sys
import subprocess

def apply_migrations():
    """Appliquer les migrations Django"""
    try:
        print("🚀 Application des migrations en cours...")
        
        # Étape 1: Supprimer les anciennes tables
        print("\n📋 Étape 1: Suppression des anciennes tables...")
        result = subprocess.run([sys.executable, 'clean_database.py'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Anciennes tables supprimées")
        else:
            print(f"⚠️  Erreur suppression tables: {result.stderr}")
        
        # Étape 2: Créer les nouvelles migrations
        print("\n📋 Étape 2: Création des nouvelles migrations...")
        result = subprocess.run([sys.executable, 'manage.py', 'makemigrations'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Migrations créées avec succès")
            print(result.stdout)
        else:
            print(f"❌ Erreur création migrations: {result.stderr}")
            return False
        
        # Étape 3: Appliquer les migrations
        print("\n📋 Étape 3: Application des migrations...")
        result = subprocess.run([sys.executable, 'manage.py', 'migrate'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Migrations appliquées avec succès")
            print(result.stdout)
        else:
            print(f"❌ Erreur application migrations: {result.stderr}")
            return False
        
        print("\n🎉 Toutes les migrations ont été appliquées avec succès!")
        print("\n📊 Nouveaux noms de tables:")
        tables = [
            'customuser',
            'userprofile', 
            'property',
            'propertyfeature',
            'prediction',
            'favorite',
            'message',
            'propertyrating',
            'searchhistory',
            'notification',
            'userreview',
            'report',
            'propertycomparison',
            'document',
            'recommendation'
        ]
        
        for table in tables:
            print(f"  ✓ {table}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    apply_migrations()
