import MySQLdb

conn = MySQLdb.connect(host='localhost', user='root', password='', database='prediction_immobiliers')
cursor = conn.cursor()

# Désactiver les contraintes de clés étrangères
cursor.execute('SET FOREIGN_KEY_CHECKS = 0')

# Supprimer toutes les tables
cursor.execute('SHOW TABLES')
tables = cursor.fetchall()

for table in tables:
    table_name = table[0]
    try:
        cursor.execute(f'DROP TABLE IF EXISTS {table_name}')
        print(f'Table {table_name} supprimée')
    except Exception as e:
        print(f'Erreur suppression {table_name}: {e}')

# Réactiver les contraintes de clés étrangères
cursor.execute('SET FOREIGN_KEY_CHECKS = 1')

conn.commit()
conn.close()
print('Base de données réinitialisée complètement')
