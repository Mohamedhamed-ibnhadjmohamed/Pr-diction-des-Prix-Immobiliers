import MySQLdb

conn = MySQLdb.connect(host='localhost', user='root', password='', database='prediction_immobiliers')
cursor = conn.cursor()
cursor.execute('SET FOREIGN_KEY_CHECKS = 0')
cursor.execute('DROP TABLE IF EXISTS property')
cursor.execute('SET FOREIGN_KEY_CHECKS = 1')
conn.commit()
conn.close()
print('Table property supprimée')
