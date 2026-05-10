#!/usr/bin/env python
"""
Script to set up MySQL database for Django project
"""
import MySQLdb
from MySQLdb import Error

def setup_mysql_database():
    """Create MySQL database if it doesn't exist"""
    try:
        # Connect to MySQL server (without specifying database)
        connection = MySQLdb.connect(
            host='localhost',
            user='root',
            password='',
            charset='utf8mb4'
        )
        
        cursor = connection.cursor()
        
        # Create database if it doesn't exist
        cursor.execute("CREATE DATABASE IF NOT EXISTS prediction_immobiliers CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print("✅ Database 'prediction_immobiliers' created or already exists")
        
        # Show databases to confirm
        cursor.execute("SHOW DATABASES")
        databases = cursor.fetchall()
        print("📋 Available databases:")
        for db in databases:
            if 'prediction_immobiliers' in db[0]:
                print(f"  ✅ {db[0]}")
            else:
                print(f"  📁 {db[0]}")
        
        cursor.close()
        connection.close()
        
        return True
        
    except Error as e:
        print(f"❌ Error setting up MySQL database: {e}")
        return False

def test_django_connection():
    """Test Django database connection"""
    try:
        import django
        from django.conf import settings
        from django.db import connection
        
        # Setup Django
        import os
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'prediction_prix_immobiliers.settings')
        django.setup()
        
        # Test connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            if result[0] == 1:
                print("✅ Django MySQL connection successful!")
                return True
            else:
                print("❌ Django MySQL connection test failed")
                return False
                
    except Exception as e:
        print(f"❌ Error testing Django connection: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Setting up MySQL database for Django project...")
    print("=" * 50)
    
    # Step 1: Create database
    if setup_mysql_database():
        print("\n" + "=" * 50)
        print("🧪 Testing Django connection...")
        
        # Step 2: Test Django connection
        if test_django_connection():
            print("\n✅ MySQL setup completed successfully!")
            print("🎉 You can now run Django migrations:")
            print("   python manage.py migrate")
        else:
            print("\n❌ Django connection test failed")
            print("💡 Please check your MySQL server status and credentials")
    else:
        print("\n❌ Failed to set up MySQL database")
        print("💡 Please ensure MySQL server is running and accessible")
