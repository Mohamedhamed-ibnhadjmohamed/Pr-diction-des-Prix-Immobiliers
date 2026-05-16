import MySQLdb

conn = MySQLdb.connect(host='localhost', user='root', password='', database='prediction_immobiliers')
cursor = conn.cursor()

# Désactiver les contraintes de clés étrangères
cursor.execute('SET FOREIGN_KEY_CHECKS = 0')

# Liste de toutes les tables à supprimer
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
    try:
        cursor.execute(f'DROP TABLE IF EXISTS {table}')
        print(f'Table {table} supprimée')
    except Exception as e:
        print(f'Erreur suppression {table}: {e}')

# Réactiver les contraintes de clés étrangères
cursor.execute('SET FOREIGN_KEY_CHECKS = 1')

conn.commit()
conn.close()
print('Nettoyage terminé')
