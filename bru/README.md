# Prédiction des Prix Immobiliers - Machine Learning

## 🏠 Description

Ce projet utilise le Machine Learning pour prédire les prix des biens immobiliers à partir de divers caractéristiques (surface, localisation, nombre de pièces, etc.). L'objectif est de fournir un outil d'aide à la décision pour les agents immobiliers et les acheteurs potentiels.

## 📁 Structure du Projet

```
├── data/                    # Données brutes et traitées
│   ├── real_estate_processed.csv
│   └── ...
├── notebooks/               # Jupyter notebooks d'analyse
│   ├── 01_Data_Exploration.ipynb
│   ├── 02_Feature_Engineering.ipynb
│   ├── 03_Model_Training.ipynb
│   └── ...
├── models/                  # Modèles entraînés
│   ├── linear_regression.pkl
│   ├── random_forest.pkl
│   └── xgboost_model.pkl
├── requirements.txt         # Dépendances Python
├── environment.yml          # Environnement Conda
└── README.md               # Ce fichier
```

## 🚀 Installation

### Avec Conda (recommandé) :
```bash
conda env create -f environment.yml
conda activate immobilier-ml
```

### Avec pip :
```bash
pip install -r requirements.txt
```

## 📊 Modèles Utilisés

- **Régression Linéaire** : Modèle de base pour benchmark
- **Random Forest** : Robuste aux outliers et non-linéarités
- **XGBoost** : Haute performance, gestion efficace des features
- **Gradient Boosting** : Alternative à XGBoost

## 📈 Métriques d'Évaluation

- **RMSE** (Root Mean Square Error) : Erreur quadratique moyenne
- **MAE** (Mean Absolute Error) : Erreur absolue moyenne
- **R²** (Coefficient de détermination) : Qualité d'ajustement

## 🔧 Utilisation

### 1. Préparation des données
```python
import pandas as pd
from sklearn.model_selection import train_test_split

# Charger les données
data = pd.read_csv('data/real_estate_processed.csv')

# Séparation features/target
X = data.drop('price', axis=1)
y = data['price']

# Split train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
```

### 2. Entraînement d'un modèle
```python
from sklearn.ensemble import RandomForestRegressor

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
```

### 3. Prédiction
```python
predictions = model.predict(X_test)
```

## 📋 Notebooks d'Analyse

### 📊 Exploration et Analyse
- `01_Data_Exploration.ipynb` : Analyse exploratoire des données
- `02_Feature_Engineering.ipynb` : Ingénierie des caractéristiques
- `08_Dataset_Analysis_Improvement.ipynb` : Amélioration du dataset

### 🤖 Modélisation
- `03_Linear_Regression.ipynb` : Régression linéaire
- `04_Random_Forest.ipynb` : Random Forest
- `05_XGBoost.ipynb` : XGBoost
- `06_Gradient_Boosting.ipynb` : Gradient Boosting

### 📈 Évaluation et Optimisation
- `07_Model_Comparison.ipynb` : Comparaison des modèles
- `09_Hyperparameter_Tuning.ipynb` : Optimisation des hyperparamètres

## 🎯 Features Principales

- **Surface** : Surface habitable en m²
- **Localisation** : Code postal, quartier
- **Nombre de pièces** : Chambres, salles de bain
- **Âge du bien** : Année de construction
- **Équipements** : Garage, jardin, balcon, etc.

## 📝 Résultats

Les meilleurs modèles atteignent :
- **RMSE** : ~15-20% du prix moyen
- **R²** : 0.75-0.85
- **MAE** : ~10-15% du prix moyen

## 🔬 Améliorations Futures

- Intégration de données externes (prix du m² par quartier)
- Modèles de Deep Learning (Neural Networks)
- Interface web pour les prédictions
- Déploiement en production (API REST)

## 🛠️ Dépendances Principales

- pandas : Manipulation des données
- numpy : Calcul numérique
- scikit-learn : Machine Learning
- xgboost : Gradient Boosting optimisé
- matplotlib/seaborn : Visualisation
- jupyter : Notebooks interactifs

## 👥 Auteurs

Projet réalisé dans le cadre de l'étude du Machine Learning appliqué à l'immobilier.

## 📄 Licence

MIT License

---

**Note** : Ce projet est à but éducatif et démontre l'application complète du Machine Learning à un problème réel de prédiction de prix.
