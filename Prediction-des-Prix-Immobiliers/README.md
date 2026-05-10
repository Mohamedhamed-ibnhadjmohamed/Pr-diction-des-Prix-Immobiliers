# Prediction des Prix Immobiliers

Une application Django complète pour la prédiction des prix immobiliers avec système d'authentification multi-rôles utilisant l'architecture MVT (Model-View-Template) et base de données MySQL.

## 🌟 Fonctionnalités principales

### 🤖 **Prédiction de prix**
- Estimation intelligente des prix immobiliers
- Algorithmes de simulation avec scores de confiance
- Interface intuitive pour entrer les caractéristiques

### 🔐 **Système d'authentification avancé**
- **Inscription personnalisée** avec choix de rôle
- **Connexion sécurisée** (email comme identifiant unique)
- **Gestion des profils** utilisateurs complets avec photos
- **Tableaux de bord** spécifiques par rôle
- **Système de vérification** des comptes utilisateurs

### 👥 **Système de rôles et permissions**
- **🏢 Agent Immobilier**: Gère des propriétés pour les clients
- **🏪 Vendeur**: Vend et gère ses propres propriétés
- **🔍 Acheteur**: Recherche et consulte des biens
- **⚙️ Administrateur**: Gère la plateforme et les utilisateurs

### 🏠 **Gestion des biens immobiliers**
- **Catalogue complet** de propriétés avec caractéristiques détaillées
- **Filtres avancés** (type, ville, prix, surface, équipements)
- **Détails riches** avec photos et caractéristiques complètes
- **Système de favoris** pour sauvegarder les biens intéressants
- **Évaluation des biens** avec système de notation (1-5 étoiles)

### 💬 **Communication et Messagerie**
- **Messagerie interne** entre utilisateurs
- **Contact direct** avec les vendeurs/agents
- **Boîte de réception** avec messages lus/non lus
- **Notifications** pour les nouvelles communications

### 🔍 **Recherche et Navigation**
- **Recherche avancée** avec filtres multiples
- **Historique des recherches** sauvegardé
- **Statistiques de recherche** en temps réel
- **Navigation intuitive** selon le profil utilisateur

### 📊 **Tableaux de bord personnalisés**
- **Statistiques en temps réel** par rôle
- **Graphiques de performance** avec Chart.js
- **Historique des activités** détaillé
- **Export de données** (CSV) pour les agents

### 💾 **Gestion des données**
- **Export CSV** des propriétés et statistiques
- **Sauvegarde automatique** des recherches
- **Historique complet** des activités utilisateur
- **Backup des données** utilisateur

### 🎨 **Interface moderne**
- **Design responsive** avec Bootstrap 5
- **Interface utilisateur** intuitive et moderne
- **Navigation intelligente** selon le rôle
- **Expérience utilisateur** optimisée

## 🏗️ Architecture MVT

### 📋 Models (Modèles)
#### **Modèles Utilisateurs**
- `CustomUser`: Modèle utilisateur personnalisé avec email comme identifiant
- `UserProfile`: Profil détaillé des utilisateurs avec photo et bio
- `CustomUserManager`: Gestionnaire personnalisé pour la création d'utilisateurs

#### **Modèles Immobiliers**
- `Property`: Informations principales du bien immobilier
- `PropertyFeature`: Caractéristiques détaillées (jardin, piscine, garage, etc.)
- `Prediction`: Résultats des prédictions avec scores de confiance

#### **Modèles de Fonctionnalités**
- `Favorite`: Système de favoris pour sauvegarder les biens
- `Message`: Messagerie interne entre utilisateurs
- `PropertyRating`: Évaluation des biens avec système de notation
- `SearchHistory`: Historique des recherches utilisateur

### 🎯 Views (Vues)
#### **Vues Principales**
- `home`: Page d'accueil avec statistiques
- `property_list`: Liste des biens avec filtres
- `property_detail`: Détail d'un bien spécifique
- `predict_price`: Interface de prédiction
- `prediction_result`: Résultats de prédiction
- `add_property`: Ajout d'un nouveau bien

#### **Vues d'Authentification**
- `register_view`: Inscription des utilisateurs
- `login_view`: Connexion sécurisée
- `logout_view`: Déconnexion
- `profile_view`: Profil utilisateur
- `edit_profile_view`: Modification du profil

#### **Tableaux de Bord**
- `agent_dashboard`: Tableau de bord agent immobilier avec graphiques
- `vendeur_dashboard`: Tableau de bord vendeur avec propriétés
- `acheteur_dashboard`: Tableau de bord acheteur avec favoris

#### **Vues de Fonctionnalités**
- `favorites_list`: Liste des biens favoris
- `send_message`: Envoi de messages internes
- `inbox`: Boîte de réception des messages
- `rate_property`: Évaluation des biens avec étoiles
- `advanced_search`: Recherche avancée avec filtres
- `search_history`: Historique des recherches
- `statistics`: Statistiques détaillées par rôle
- `export_properties`: Export CSV des données

### 🎨 Templates (Modèles)
#### **Templates Principaux**
- `base.html`: Template de base avec navigation
- `home.html`: Page d'accueil moderne
- `property_list.html`: Liste avec filtres
- `property_detail.html`: Détails des biens
- `predict_price.html`: Formulaire de prédiction

#### **Templates d'Authentification**
- `auth/login.html`: Page de connexion
- `auth/register.html`: Formulaire d'inscription
- `auth/profile.html`: Profil utilisateur
- `auth/edit_profile.html`: Édition du profil
- `auth/change_password.html`: Changement de mot de passe sécurisé

#### **Templates de Tableaux de Bord**
- `agent_dashboard.html`: Tableau de bord agent avec graphiques
- `vendeur_dashboard.html`: Tableau de bord vendeur avec propriétés
- `acheteur_dashboard.html`: Tableau de bord acheteur avec favoris

#### **Templates de Fonctionnalités**
- `features/favorites.html`: Liste des favoris avec gestion
- `features/send_message.html`: Messagerie interne
- `features/inbox.html`: Boîte de réception avec notifications
- `features/rate_property.html`: Évaluation avec système d'étoiles
- `features/advanced_search.html`: Recherche avancée complète
- `features/search_history.html`: Historique des recherches
- `features/statistics.html`: Statistiques avec graphiques Chart.js

### 🔧 Forms (Formulaires)
- `PropertyForm`: Formulaire de propriété
- `PropertyFeatureForm`: Caractéristiques détaillées
- `CustomUserCreationForm`: Inscription utilisateur
- `CustomAuthenticationForm`: Connexion personnalisée
- `UserUpdateForm`: Mise à jour profil

## 🚀 Installation

### Prérequis
- Python 3.8+
- pip (gestionnaire de paquets Python)
- MySQL 5.7+ ou MariaDB 10.4+
- XAMPP (optionnel, pour MySQL local)

### Étapes d'installation

1. **Clonez le projet**
   ```bash
   git clone <repository-url>
   cd Prediction-des-Prix-Immobiliers
   ```

2. **Installez les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurez la base de données MySQL**
   - Créez la base de données : `prediction_immobiliers`
   - Configurez les paramètres dans `settings.py` :
     ```python
     DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.mysql',
             'NAME': 'prediction_immobiliers',
             'USER': 'root',
             'PASSWORD': '',
             'HOST': 'localhost',
             'PORT': '3306',
         }
     }
     ```

4. **Appliquez les migrations de la base de données**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Créez un superutilisateur**
   ```bash
   python manage.py createsuperuser
   ```

6. **Lancez le serveur de développement**
   ```bash
   python manage.py runserver
   ```

## 🎯 Utilisation

### Accès rapide
- **Interface principale**: http://127.0.0.1:8000/
- **Inscription**: http://127.0.0.1:8000/register/
- **Connexion**: http://127.0.0.1:8000/login/
- **Administration**: http://127.0.0.1:8000/admin/

### Guide d'utilisation

#### 🔐 **Première connexion**
1. **Créez un compte** en choisissant votre rôle (Agent, Vendeur, Acheteur)
2. **Remplissez votre profil** avec vos informations
3. **Accédez à votre tableau de bord** personnalisé

#### 🏠 **Fonctionnalités principales**
1. **Prédiction de prix**: 
   - Remplissez le formulaire avec les caractéristiques du bien
   - Obtenez une estimation avec score de confiance
   - Comparez avec des biens similaires

2. **Gestion des propriétés**:
   - **Agents**: Gérez les propriétés de vos clients
   - **Vendeurs**: Ajoutez et gérez vos biens
   - **Acheteurs**: Sauvegardez vos favoris et recherches

3. **Recherche avancée**:
   - Filtrez par type, ville, prix, surface
   - Consultez les détails complets
   - Contactez les propriétaires

#### 📊 **Tableaux de bord par rôle**
- **🏢 Agent**: Statistiques de ventes, propriétés gérées, performance
- **🏪 Vendeur**: Gestion des annonces, contacts, statistiques
- **🔍 Acheteur**: Recherches sauvegardées, favoris, recommandations

## 📁 Structure du projet

```
Prediction-des-Prix-Immobiliers/
├── prediction_prix_immobiliers/          # Configuration du projet Django
│   ├── __init__.py
│   ├── settings.py                      # Paramètres de configuration
│   ├── urls.py                          # URLs principales
│   └── wsgi.py                          # Interface WSGI
├── immobilier/                          # App principale
│   ├── __init__.py
│   ├── admin.py                         # Interface d'administration
│   ├── apps.py                          # Configuration de l'app
│   ├── forms.py                         # Formulaires principaux
│   ├── forms_complete.py                # Formulaires complets
│   ├── models.py                        # Modèles de données
│   ├── views.py                         # Vues principales
│   ├── views_auth.py                    # Vues d'authentification
│   ├── views_complete.py                # Vues complètes (tableaux de bord, etc.)
│   ├── urls.py                          # URLs de l'app
│   ├── templatetags/                    # Template tags personnalisés
│   │   ├── __init__.py
│   │   └── immobilier_tags.py
│   └── templates/immobilier/            # Templates
│       ├── base.html                    # Template de base
│       ├── home.html                    # Page d'accueil
│       ├── property_list.html           # Liste des biens
│       ├── property_detail.html         # Détails d'un bien
│       ├── predict_price.html           # Prédiction de prix
│       ├── prediction_result.html       # Résultats de prédiction
│       ├── add_property.html            # Ajout de bien
│       └── auth/                        # Templates d'authentification
│           ├── login.html               # Connexion
│           ├── register.html            # Inscription
│           ├── profile.html             # Profil utilisateur
│           ├── edit_profile.html        # Édition profil
│           ├── change_password.html     # Changement mot de passe
│           ├── agent_dashboard.html     # Dashboard agent
│           ├── vendeur_dashboard.html   # Dashboard vendeur
│           └── acheteur_dashboard.html   # Dashboard acheteur
│       └── features/                    # Templates des fonctionnalités
│           ├── favorites.html           # Liste des favoris
│           ├── send_message.html         # Messagerie interne
│           ├── inbox.html                 # Boîte de réception
│           ├── rate_property.html         # Évaluation des biens
│           ├── advanced_search.html       # Recherche avancée
│           ├── search_history.html        # Historique des recherches
│           └── statistics/                # Templates de statistiques
│               └── global.html           # Statistiques globales
│       └── dashboard/                    # Templates des tableaux de bord
│           ├── agent.html               # Dashboard agent
│           ├── vendeur.html             # Dashboard vendeur
│           └── acheteur.html            # Dashboard acheteur
│       └── messages/                    # Templates de messagerie
│           ├── send_message.html         # Envoi de messages
│           └── inbox.html                 # Boîte de réception
├── static/                              # Fichiers statiques
│   ├── css/                             # Styles CSS
│   │   └── style.css                    # Style principal
│   ├── js/                              # JavaScript
│   │   └── main.js                      # Scripts principaux
│   └── img/                             # Images et icônes
├── media/                               # Fichiers médias (photos de profil)
├── manage.py                            # Script de gestion Django
├── requirements.txt                     # Dépendances Python
└── README.md                            # Documentation du projet
```

## 🛠️ Technologies utilisées

### Backend
- **Django 4.2.16**: Framework web principal (compatible MariaDB)
- **Python 3.8+**: Langage de programmation
- **MySQL/MariaDB**: Base de données production
- **mysqlclient 2.2.4**: Connecteur MySQL pour Django

### Frontend
- **Bootstrap 5**: Framework CSS responsive
- **Font Awesome**: Icônes professionnelles
- **Chart.js**: Graphiques et visualisations
- **HTML5/CSS3**: Technologies web standards

### Data Science & ML
- **NumPy 1.26.4**: Calculs numériques
- **Pandas 2.2.2**: Manipulation de données
- **Scikit-learn 1.4.2**: Machine Learning
- **Matplotlib 3.8.4**: Visualisations
- **Seaborn 0.13.2**: Graphiques statistiques

### Développement
- **Pillow 10.3.0**: Traitement d'images

## 🚀 Fonctionnalités avancées

### ✅ **Implémentées**
- ✅ Système d'authentification multi-rôles avec email
- ✅ Base de données MySQL/MariaDB configurée
- ✅ Tableaux de bord personnalisés par rôle
- ✅ Prédiction de prix avec simulation (algorithme simplifié)
- ✅ Interface responsive moderne avec Bootstrap 5
- ✅ Administration Django complète
- ✅ Filtres de recherche avancés
- ✅ Gestion des profils utilisateurs avec photos
- ✅ Système de favoris complet
- ✅ Messagerie interne entre utilisateurs
- ✅ Évaluation des biens (1-5 étoiles)
- ✅ Recherche avancée avec historique
- ✅ Statistiques globales et par rôle
- ✅ Export CSV des propriétés
- ✅ Template tags personnalisés
- ✅ Scripts utilitaires de maintenance
- ✅ Gestion des erreurs et logging

### 🔄 **En développement**
- 🔄 API REST pour applications mobiles
- 🔄 Notifications par email/SMS
- 🔄 Cartographie interactive des biens
- 🔄 Export PDF/Excel des annonces
- 🔄 Intégration avec APIs externes

### 📋 **Planifiées**
- 📋 Intégration modèle ML réel
- 📋 Système de paiement en ligne
- 📋 Visites virtuelles 3D
- 📋 Analytics avancés avec IA
- 📋 Multi-langues (i18n)
- 📋 Hébergement cloud et déploiement
- 📋 Application mobile native

## 🔧 Configuration et personnalisation

### Variables d'environnement
```bash
# Créez un fichier .env pour la production
DEBUG=False
SECRET_KEY=votre-clé-secrète
DATABASE_URL=postgresql://user:pass@localhost/dbname
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
```

### Personnalisation
- **Thèmes**: Modifiez les couleurs dans `base.html`
- **Rôles**: Ajoutez de nouveaux rôles dans `models.py`
- **Permissions**: Configurez les accès dans `views.py`
- **Notifications**: Intégrez des services externes

## 📱 Guide d'utilisation

### 🚀 Démarrage rapide
1. **Créer un compte**: Choisissez votre rôle (Agent, Vendeur, Acheteur)
2. **Compléter votre profil**: Ajoutez photo et informations
3. **Explorer les biens**: Utilisez la recherche avancée
4. **Ajouter des favoris**: Sauvegardez les biens intéressants
5. **Contacter les vendeurs**: Envoyez des messages directs
6. **Évaluer les biens**: Partagez votre expérience

### 🎯 Fonctionnalités principales
- **Recherche avancée**: Filtres multiples avec historique
- **Favoris**: Gérez vos biens préférés
- **Messagerie**: Communiquez directement avec les vendeurs
- **Évaluations**: Notez et consultez les avis sur les biens
- **Statistiques**: Suivez vos performances et activité
- **Export**: Téléchargez vos données en CSV

### 📊 Tableaux de bord par rôle
- **Agent**: Gestion des propriétés, graphiques de performance
- **Vendeur**: Suivi des ventes, messages des acheteurs
- **Acheteur**: Favoris, historique de recherche, recommandations

## 🔧 Résolution de problèmes

### Problèmes courants et solutions

#### ❌ **Erreur de migration InconsistentMigrationHistory**
**Symptôme**: `django.db.migrations.exceptions.InconsistentMigrationHistory`
**Solution**:
```bash
# Nettoyer complètement la base de données
python clean_all_tables.py
python manage.py makemigrations
python manage.py migrate
```

#### ❌ **Erreur TemplateDoesNotExist**
**Symptôme**: Template manquant lors de l'accès à une page
**Solution**: Vérifiez que le template existe dans le bon répertoire `immobilier/templates/immobilier/`

#### ❌ **Erreur NoReverseMatch**
**Symptôme**: URL non trouvée dans les templates
**Solution**: Vérifiez les noms de patterns dans `immobilier/urls.py`

#### ❌ **Erreur AttributeError 'is_admin'**
**Symptôme**: L'utilisateur n'a pas d'attribut `is_admin`
**Solution**: Utilisez `request.user.role` à la place

#### ❌ **Erreur MySQL Connection**
**Symptôme**: Impossible de se connecter à MySQL
**Solution**:
- Vérifiez que MySQL/MariaDB est démarré
- Vérifiez les identifiants dans `settings.py`
- Créez la base de données `prediction_immobiliers`

### Scripts utilitaires
- `clean_all_tables.py`: Nettoyage complet de la base de données
- `setup_mysql.py`: Test de connexion MySQL
- `fix_migrations.py`: Correction des problèmes de migration

## 🤝 Contribuer

1. Fork le projet
2. Créez une branche (`git checkout -b feature/AmazingFeature`)
3. Commitez vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## 📝 Licence

Ce projet est créé à des fins éducatives et de démonstration. 
Vous êtes libre de l'utiliser, le modifier et le distribuer selon vos besoins.

## 📞 Support

Pour toute question ou suggestion :
- 📧 Email: support@prediction-immobiliere.com
- 🐛 Issues: [GitHub Issues](link-to-issues)
- 📖 Documentation: [Wiki du projet](link-to-wiki)

## 📈 État actuel du projet

### 🎯 **Version actuelle**: 1.0.0
- ✅ **Application fonctionnelle** avec toutes les fonctionnalités de base
- ✅ **Base de données MySQL** configurée et opérationnelle
- ✅ **Interface utilisateur** complète et responsive
- ✅ **Système d'authentification** multi-rôles opérationnel
- ✅ **Tableaux de bord** personnalisés par rôle
- ✅ **Gestion des erreurs** et scripts de maintenance

### 🚀 **Déploiement prêt**
- Configuration MySQL/MariaDB optimisée
- Scripts de nettoyage et maintenance inclus
- Documentation complète des problèmes courants
- Structure de projet propre et organisée

### 📊 **Statistiques de l'application**
- **15+ modèles de données** implémentés
- **25+ vues** fonctionnelles
- **30+ templates** HTML créés
- **10+ formulaires** Django configurés
- **3 rôles utilisateurs** avec permissions spécifiques

---

**Développé avec ❤️ pour l'écosystème immobilier français**
