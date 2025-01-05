import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import HistGradientBoostingClassifier, VotingClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score, roc_curve, auc
from imblearn.over_sampling import SMOTE
import matplotlib.pyplot as plt
import numpy as np
import pickle
import os

# Load the dataset
file_path = r"C:\\Users\\jwright\\Documents\\GitHub\\sevLandsPublicData\\data\\replay_data\\transformed_replay_data_win_probability\\all_set_200k_games.csv"
data = pd.read_csv(file_path)
print('data loaded')

print('adding extra columns')
data['life_difference'] = data['user_life'] - data['oppo_life']

# Count non-null values in user hand and creature columns
data['user_cards_in_hand'] = data[[col for col in data.columns if 'user_hand' in col]].notnull().sum(axis=1)
data['user_creatures_in_play'] = data[[col for col in data.columns if 'user_creature' in col]].notnull().sum(axis=1)
data['opponent_creatures_in_play'] = data[[col for col in data.columns if 'oppo_creature' in col]].notnull().sum(axis=1)

# Drop irrelevant columns
irrelevant_columns = ['game_id', 'chunk_index']  # Add other irrelevant columns if needed
target = 'won'
X = data.drop(columns=irrelevant_columns + [target])
y = data[target]

# Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Handle class imbalance using SMOTE (exclude rows with NaN values for SMOTE)
print("Applying SMOTE for class balancing...")
non_nan_indices = X_train.dropna().index
X_train_non_nan = X_train.loc[non_nan_indices]
y_train_non_nan = y_train.loc[non_nan_indices]

if X_train_non_nan.empty:
    print("No non-NaN rows available for SMOTE. Skipping SMOTE.")
    X_train_resampled, y_train_resampled = X_train, y_train
else:
    smote = SMOTE(random_state=42)
    X_train_resampled, y_train_resampled = smote.fit_resample(X_train_non_nan, y_train_non_nan)

# --- HistGradientBoostingClassifier ---
print("Training HistGradientBoostingClassifier...")
hist_model = HistGradientBoostingClassifier(random_state=42, max_iter=200, learning_rate=0.1, max_depth=5)
hist_model.fit(X_train, y_train)
hist_predictions = hist_model.predict_proba(X_test)[:, 1]

# --- XGBoost ---
print("Training XGBoost...")
xgb_model = XGBClassifier(eval_metric='logloss', random_state=42, max_depth=5, learning_rate=0.1, n_estimators=200)
xgb_model.fit(X_train_resampled, y_train_resampled)
xgb_predictions = xgb_model.predict_proba(X_test)[:, 1]

# Save the XGBoost model
model_save_path = r"C:\\Users\\jwright\\Documents\\GitHub\\sevLandsPublicData\\models\\win_probability\\xgb_win_prob_model.pkl"
os.makedirs(os.path.dirname(model_save_path), exist_ok=True)
with open(model_save_path, 'wb') as model_file:
    pickle.dump(xgb_model, model_file)
print(f"XGBoost model saved to {model_save_path}")

# --- LightGBM ---
print("Training LightGBM...")
lgbm_model = LGBMClassifier(random_state=42, max_depth=5, learning_rate=0.1, n_estimators=200)
lgbm_model.fit(X_train_resampled, y_train_resampled)
lgbm_predictions = lgbm_model.predict_proba(X_test)[:, 1]

# --- Logistic Regression (Naive Model) ---
print("Training Logistic Regression (Naive Model)...")
logistic_X = X[['turn', 'user_life', 'oppo_life']].dropna()
logistic_y = y.loc[logistic_X.index]
logistic_X_train, logistic_X_test, logistic_y_train, logistic_y_test = train_test_split(
    logistic_X, logistic_y, test_size=0.2, random_state=42
)
logistic_model = LogisticRegression(random_state=42)
logistic_model.fit(logistic_X_train, logistic_y_train)
logistic_predictions = logistic_model.predict_proba(logistic_X_test)[:, 1]

# --- Turn-Based Models ---
def train_turn_based_model(data, turn_range):
    print(f"Training model for turns {turn_range}...")
    turn_data = data[data['turn'].between(*turn_range)]
    X_turn = turn_data.drop(columns=irrelevant_columns + [target])
    y_turn = turn_data[target]
    X_train_turn, X_test_turn, y_train_turn, y_test_turn = train_test_split(X_turn, y_turn, test_size=0.2, random_state=42)

    turn_model = HistGradientBoostingClassifier(random_state=42, max_iter=200, learning_rate=0.1, max_depth=5)
    turn_model.fit(X_train_turn, y_train_turn)
    predictions = turn_model.predict_proba(X_test_turn)[:, 1]

    print(f"Turn {turn_range} Classification Report:")
    print(classification_report(y_test_turn, (predictions > 0.5).astype(int)))
    return turn_model

turn_ranges = [(1, 5), (6, 15), (16, data['turn'].max())]
turn_models = {range_: train_turn_based_model(data, range_) for range_ in turn_ranges}

# --- Ensemble Model ---
print("Training Ensemble Model...")
ensemble_model = VotingClassifier(
    estimators=[('xgb', xgb_model), ('lgbm', lgbm_model), ('hist', hist_model)],
    voting='soft'
)
ensemble_model.fit(X_train_resampled, y_train_resampled)
ensemble_predictions = ensemble_model.predict_proba(X_test)[:, 1]

# --- Evaluation and ROC Curves ---
def plot_roc_curve(y_true, y_pred, model_name):
    fpr, tpr, _ = roc_curve(y_true, y_pred)
    auc_score = auc(fpr, tpr)
    plt.plot(fpr, tpr, label=f'{model_name} (AUC = {auc_score:.2f})')

plt.figure(figsize=(10, 6))

# Plot ROC curves
plot_roc_curve(y_test, hist_predictions, 'HistGradientBoosting')
plot_roc_curve(y_test, xgb_predictions, 'XGBoost')
plot_roc_curve(y_test, lgbm_predictions, 'LightGBM')
plot_roc_curve(logistic_y_test, logistic_predictions, 'Logistic Regression')
plot_roc_curve(y_test, ensemble_predictions, 'Ensemble Model')

# Finalize Plot
plt.plot([0, 1], [0, 1], 'k--', label='Random Chance')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve Comparison')
plt.legend()
plt.grid()
plt.show()

# Accuracy by turn
if 'turn' in data.columns:
    print("Analyzing accuracy by turn...")
    data['prediction'] = hist_model.predict(X)
    turn_accuracy = data.groupby('turn').apply(lambda x: (x['won'] == x['prediction']).mean())
    plt.figure(figsize=(10, 6))
    turn_accuracy.plot(kind='bar', color='skyblue', edgecolor='k')
    plt.title('Accuracy by Turn')
    plt.xlabel('Turn')
    plt.ylabel('Accuracy')
    plt.xticks(rotation=45, ha='right')
    plt.grid()
    plt.tight_layout()
    plt.show()
else:
    print("Turn column not found in dataset. Skipping accuracy by turn analysis.")

# Feature Importance
importances = {}

# --- XGBoost Feature Importance ---
print("\nFeature Importance: XGBoost")
xgb_importances = xgb_model.feature_importances_
importances['XGBoost'] = pd.Series(xgb_importances, index=X.columns).sort_values(ascending=False)

# --- LightGBM Feature Importance ---
print("\nFeature Importance: LightGBM")
lgbm_importances = lgbm_model.feature_importances_
importances['LightGBM'] = pd.Series(lgbm_importances, index=X.columns).sort_values(ascending=False)

# --- Visualize Feature Importance ---
def plot_feature_importance(importances, title, top_n=10):
    top_features = importances.head(top_n)
    plt.figure(figsize=(10, 6))
    top_features.plot(kind='bar', color='skyblue', edgecolor='k')
    plt.title(title)
    plt.ylabel('Importance Score')
    plt.xlabel('Features')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

# Plot top N features for each model
for model_name, importance in importances.items():
    print(f"\nTop Features for {model_name}:")
    print(importance.head(10))
    plot_feature_importance(importance, f"Top 10 Features: {model_name}")

# Print classification reports
print("\nHistGradientBoostingClassifier Classification Report:")
print(classification_report(y_test, (hist_predictions > 0.5).astype(int)))

print("\nXGBoost Classification Report:")
print(classification_report(y_test, (xgb_predictions > 0.5).astype(int)))

print("\nLightGBM Classification Report:")
print(classification_report(y_test, (lgbm_predictions > 0.5).astype(int)))

print("\nLogistic Regression Classification Report:")
print(classification_report(logistic_y_test, (logistic_predictions > 0.5).astype(int)))

print("\nEnsemble Model Classification Report:")
print(classification_report(y_test, (ensemble_predictions > 0.5).astype(int)))
