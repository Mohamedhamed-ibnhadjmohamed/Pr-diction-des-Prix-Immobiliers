#!/usr/bin/env python
"""
Script pour exécuter XGBoost Regression
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Modélisation XGBoost
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import time
import joblib
import os

print("📚 Bibliothèques importées avec succès !")
print("🚀 XGBoost Regression prêt")
print(f"📦 Version XGBoost: {xgb.__version__}")

# Charger et préparer les données
df = pd.read_csv("data/real_estate_processed.csv")
print(f"Données originales: {df.shape}")

# Nettoyage
df_clean = df[(df['price'] >= 50) & (df['price'] <= 10000000)].copy()
print(f"Données après nettoyage: {df_clean.shape}")
print(f"Supprimées: {len(df) - len(df_clean)} annonces")

df = df_clean

print(f"\nStatistiques des prix:")
print(f"Prix moyen: {df['price'].mean():.0f} DT")
print(f"Prix médian: {df['price'].median():.0f} DT")
print(f"Prix min: {df['price'].min():.0f} DT")
print(f"Prix max: {df['price'].max():.0f} DT")
print(f"Écart-type: {df['price'].std():.0f} DT")

# Feature Engineering
print("\n=== FEATURE ENGINEERING POUR XGBOOST ===")

numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
X_base = df[numeric_columns].drop('price', axis=1)
y = df['price']

X = X_base.copy()

# Features temporelles
X['quarter'] = ((X['post_month'] - 1) // 3) + 1
X['is_summer'] = (X['post_month'].isin([6, 7, 8])).astype(int)
X['is_winter'] = (X['post_month'].isin([12, 1, 2])).astype(int)
X['is_spring'] = (X['post_month'].isin([3, 4, 5])).astype(int)
X['is_autumn'] = (X['post_month'].isin([9, 10, 11])).astype(int)

# Features d'interaction
X['category_transaction_interaction'] = X['category'] * X['type_transaction']
X['category_month_interaction'] = X['category'] * X['post_month']
X['transaction_month_interaction'] = X['type_transaction'] * X['post_month']
X['category_year_interaction'] = X['category'] * X['post_year']
X['transaction_year_interaction'] = X['type_transaction'] * X['post_year']

# Features polynomiales
X['category_squared'] = X['category'] ** 2
X['type_transaction_squared'] = X['type_transaction'] ** 2
X['month_squared'] = X['post_month'] ** 2
X['year_squared'] = X['post_year'] ** 2

# Target encoding
price_by_category = df.groupby('category')['price'].agg(['mean', 'median', 'std'])
price_by_transaction = df.groupby('type_transaction')['price'].agg(['mean', 'median', 'std'])
price_by_month = df.groupby('post_month')['price'].agg(['mean', 'median', 'std'])
price_by_year = df.groupby('post_year')['price'].agg(['mean', 'median', 'std'])

# Ajouter la colonne quarter au dataframe original pour le groupby
df_with_quarter = df.copy()
df_with_quarter['quarter'] = ((df_with_quarter['post_month'] - 1) // 3) + 1
price_by_quarter = df_with_quarter.groupby('quarter')['price'].agg(['mean', 'median', 'std'])

X['category_price_mean'] = X['category'].map(price_by_category['mean'])
X['transaction_price_mean'] = X['type_transaction'].map(price_by_transaction['mean'])
X['month_price_mean'] = X['post_month'].map(price_by_month['mean'])
X['year_price_mean'] = X['post_year'].map(price_by_year['mean'])
X['quarter_price_mean'] = X['quarter'].map(price_by_quarter['mean'])

# Features logarithmiques (uniquement pour les colonnes qui existent)
X['log_category'] = np.log1p(X['category'])
X['log_month'] = np.log1p(X['post_month'])
X['log_year_diff'] = np.log1p(X['post_year'] - 2024)

# Ajouter log_rooms et log_location seulement si ces colonnes existent
if 'rooms' in X.columns:
    X['log_rooms'] = np.log1p(X['rooms'])
if 'location' in X.columns:
    X['log_location'] = np.log1p(X['location'])

# Remplir les valeurs NaN
X = X.fillna(0)

print(f"Features créées: {X_base.shape[1]} -> {X.shape[1]} (+{X.shape[1] - X_base.shape[1]} nouvelles)")

# Transformation de la target
y_log = np.log1p(y)

# Division des données
X_train, X_test, y_train, y_test = train_test_split(X, y_log, test_size=0.2, random_state=42)

print(f"Données divisées: {X_train.shape[0]} entraînement, {X_test.shape[0]} test")
print(f"Features finales: {X.shape[1]}")

# XGBoost - Version simple
print("\n=== XGBOOST - VERSION SIMPLE ===")

start_time = time.time()

xgb_simple = xgb.XGBRegressor(
    n_estimators=200,
    max_depth=6,
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    n_jobs=-1,
    objective='reg:squarederror'
)

xgb_simple.fit(X_train, y_train)
training_time = time.time() - start_time

print(f"⏱️ Temps d'entraînement: {training_time:.2f} secondes")
print(f"🌳 Nombre d'arbres: {xgb_simple.n_estimators}")
print(f"📏 Profondeur max: {xgb_simple.max_depth}")
print(f"📚 Learning rate: {xgb_simple.learning_rate}")
print(f"✅ Modèle entraîné !")

# Évaluation
print("\n=== ÉVALUATION MODÈLE ===")

# Prédictions
y_train_pred = xgb_simple.predict(X_train)
y_test_pred = xgb_simple.predict(X_test)

# Conversion à l'échelle originale
y_train_orig = np.expm1(y_train)
y_test_orig = np.expm1(y_test)
y_train_pred_orig = np.expm1(y_train_pred)
y_test_pred_orig = np.expm1(y_test_pred)

# Métriques
train_r2 = r2_score(y_train_orig, y_train_pred_orig)
test_r2 = r2_score(y_test_orig, y_test_pred_orig)
train_rmse = np.sqrt(mean_squared_error(y_train_orig, y_train_pred_orig))
test_rmse = np.sqrt(mean_squared_error(y_test_orig, y_test_pred_orig))
train_mae = mean_absolute_error(y_train_orig, y_train_pred_orig)
test_mae = mean_absolute_error(y_test_orig, y_test_pred_orig)

print(f"📊 PERFORMANCE XGBOOST:")
print(f"   R² Train: {train_r2:.4f}")
print(f"   R² Test:  {test_r2:.4f}")
print(f"   RMSE Train: {train_rmse:,.0f} DT")
print(f"   RMSE Test:  {test_rmse:,.0f} DT")
print(f"   MAE Train:  {train_mae:,.0f} DT")
print(f"   MAE Test:   {test_mae:,.0f} DT")

# Analyse de l'overfitting
overfitting_r2 = train_r2 - test_r2
print(f"\n🔍 ANALYSE OVERFITTING:")
print(f"   Différence R² (Train-Test): {overfitting_r2:.4f}")

if overfitting_r2 > 0.1:
    print(f"   ⚠️ Overfitting détecté !")
elif overfitting_r2 > 0.05:
    print(f"   🟡 Léger overfitting")
else:
    print(f"   ✅ Bon équilibre")

# Qualité du modèle
if test_r2 > 0.7:
    quality = "🌟 Excellente"
elif test_r2 > 0.5:
    quality = "✅ Bonne"
elif test_r2 > 0.3:
    quality = "⚠️ Moyenne"
else:
    quality = "📉 Faible"

print(f"\n🏆 QUALITÉ: {quality}")

# Sauvegarde
print("\n=== SAUVEGARDE DU MODÈLE ===")

# Créer le dossier models s'il n'existe pas
if not os.path.exists('models'):
    os.makedirs('models')

# Sauvegarder le modèle
joblib.dump(xgb_simple, 'models/xgboost_best_model.pkl')

# Sauvegarder les résultats
xgb_results = {
    'model_name': 'XGBoost',
    'version': 'Simple',
    'r2_train': train_r2,
    'r2_test': test_r2,
    'rmse_train': train_rmse,
    'rmse_test': test_rmse,
    'mae_train': train_mae,
    'mae_test': test_mae,
    'training_time': training_time,
    'n_features': X.shape[1],
    'feature_columns': list(X.columns),
    'xgb_version': xgb.__version__,
    'quality': quality
}

joblib.dump(xgb_results, 'models/xgboost_results.pkl')

print(f"   ✅ Modèle sauvegardé: models/xgboost_best_model.pkl")
print(f"   ✅ Résultats sauvegardés: models/xgboost_results.pkl")
print(f"\n🎉 XGBoost Regression terminé avec succès !")

# Feature importance
print("\n=== TOP 10 FEATURES IMPORTANCE ===")
feature_importance = pd.DataFrame({
    'Feature': X.columns,
    'Importance': xgb_simple.feature_importances_
}).sort_values('Importance', ascending=False).head(10)

for i, row in feature_importance.iterrows():
    print(f"{row.name+1:2d}. {row['Feature'][:35]:35s}: {row['Importance']*100:5.2f}%")
