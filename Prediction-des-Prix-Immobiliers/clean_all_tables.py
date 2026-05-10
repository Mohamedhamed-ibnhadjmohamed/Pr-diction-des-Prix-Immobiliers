import MySQLdb

conn = MySQLdb.connect(host='localhost', user='root', password='', database='prediction_immobiliers')
cursor = conn.cursor()

# Désactiver les contraintes de clés étrangères
cursor.execute('SET FOREIGN_KEY_CHECKS = 0')

# Obtenir toutes les tables de la base de données
cursor.execute('SHOW TABLES')
tables = [row[0] for row in cursor.fetchall()]

# Supprimer toutes les tables sauf celles qu'on veut garder
for table in tables:
    try:
        cursor.execute(f'DROP TABLE IF EXISTS {table}')
        print(f'Table {table} supprimée')
    except Exception as e:
        print(f'Erreur suppression {table}: {e}')

# Réactiver les contraintes de clés étrangères
cursor.execute('SET FOREIGN_KEY_CHECKS = 1')

conn.commit()
conn.close()
print('Nettoyage complet terminé')
