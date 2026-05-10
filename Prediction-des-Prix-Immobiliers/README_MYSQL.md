# Configuration MySQL pour l'application Django (XAMPP)

## Étapes de configuration avec XAMPP

### 1. Installation des dépendances
```bash
pip install -r requirements.txt
```

### 2. Démarrer XAMPP et MySQL
1. Ouvrez le **Panneau de configuration XAMPP**
2. Cliquez sur **Start** pour le service **MySQL**
3. Vérifiez que MySQL est bien démarré (vert)

### 3. Accéder à phpMyAdmin (optionnel)
- Ouvrez votre navigateur: http://localhost/phpmyadmin
- Identifiant: `root`
- Mot de passe: (vide)
- Port: `3306`

### 4. Créer la base de données
**Méthode 1: Via phpMyAdmin**
1. Allez dans phpMyAdmin
2. Cliquez sur "Nouvelle base de données"
3. Nom: `prediction_immobiliers`
4. Interclassement: `utf8mb4_unicode_ci`
5. Cliquez sur "Créer"

**Méthode 2: Via ligne de commande**
```bash
# Ouvrez le terminal XAMPP ou cmd
mysql -u root -p < setup_mysql.sql
```

**Méthode 3: Manuellement dans MySQL**
```sql
CREATE DATABASE prediction_immobiliers CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 5. Configuration (si nécessaire)
Modifiez les paramètres dans `prediction_prix_immobiliers/settings.py` si vous utilisez:
- Un autre nom d'utilisateur que `root`
- Un mot de passe
- Un autre hôte que `localhost`
- Un autre port que `3306`

### 6. Faire les migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Créer un superutilisateur
```bash
python manage.py createsuperuser
```

### 8. Tester l'application
```bash
python manage.py runserver
```

## Configuration XAMPP par défaut
Les paramètres actuels dans settings.py sont optimisés pour XAMPP:
- **Base de données**: `prediction_immobiliers`
- **Utilisateur**: `root`
- **Mot de passe**: (vide - par défaut XAMPP)
- **Hôte**: `localhost`
- **Port**: `3306` (port MySQL par défaut XAMPP)

## Dépannage spécifique à XAMPP

### Erreur de connexion MySQL
1. **Vérifiez que MySQL est démarré** dans le panneau XAMPP
2. **Vérifiez le port**: XAMPP utilise parfois le port 3306 ou 3307
3. **Testez la connexion**: Ouvrez http://localhost/phpmyadmin
4. **Redémarrez les services** XAMPP si nécessaire

### Si le port 3306 ne fonctionne pas
Modifiez le port dans settings.py:
```python
"PORT": "3307",  # Essayez ce port si 3306 ne fonctionne pas
```

### Erreur mysqlclient avec XAMPP
```bash
# Windows (recommandé avec XAMPP)
pip install --only-binary :all: mysqlclient

# Alternative si problème de compilation
pip install mysql-connector-python
# Et modifiez ENGINE dans settings.py:
# "ENGINE": "django.db.backends.mysql.connector.python"
```

### Services XAMPP qui ne démarrent pas
1. **Vérifiez que Skype** n'utilise pas le port 80/443
2. **Arrêtez d'autres services** Apache/MySQL
3. **Exécutez XAMPP en tant qu'administrateur**
4. **Vérifiez les logs** dans le panneau XAMPP

### Migration depuis SQLite vers XAMPP MySQL
Si vous avez des données dans SQLite:
1. Exportez vos données de SQLite
2. Créez la base MySQL dans phpMyAdmin
3. Faites les migrations Django
4. Importez vos données manuellement

## Commandes utiles XAMPP
```bash
# Démarrer/arrêter MySQL via ligne de commande
cd C:\xampp\mysql\bin
mysql -u root -p  # Connexion
mysqladmin -u root shutdown  # Arrêt
```
