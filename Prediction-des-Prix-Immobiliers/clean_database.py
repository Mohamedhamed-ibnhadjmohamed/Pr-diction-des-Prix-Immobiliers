import MySQLdb

conn = MySQLdb.connect(host='localhost', user='root', password='', database='prediction_immobiliers')
cursor = conn.cursor()

# Désactiver les contraintes de clés étrangères
cursor.execute('SET FOREIGN_KEY_CHECKS = 0')

# Liste de toutes les tables à supprimer
tables = [
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
