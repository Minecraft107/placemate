import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pickle
import json

# Load data
df = pd.read_csv('ml/dataset.csv')

# Features and target
FEATURES = ['cgpa', 'backlogs', 'internship_done', 'projects_count', 
            'skills_count', 'ats_score', 'communication_score']

X = df[FEATURES]
y = df['placed']

# Handle missing values — beginner mistake: forgetting this step
X = X.fillna(X.mean())

# Split data — always stratify for classification
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Scale features — very important for Logistic Regression
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)  # NEVER fit on test data!

# Train Logistic Regression
lr_model = LogisticRegression(random_state=42, max_iter=1000)
lr_model.fit(X_train_scaled, y_train)
lr_preds = lr_model.predict(X_test_scaled)
lr_acc = accuracy_score(y_test, lr_preds)

print("=== Logistic Regression ===")
print(f"Accuracy: {lr_acc:.4f}")
print(classification_report(y_test, lr_preds))

# Train Random Forest — doesn't need scaling, but apply anyway for consistency
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train_scaled, y_train)
rf_preds = rf_model.predict(X_test_scaled)
rf_acc = accuracy_score(y_test, rf_preds)

print("=== Random Forest ===")
print(f"Accuracy: {rf_acc:.4f}")
print(classification_report(y_test, rf_preds))

# Feature importance (great for viva!)
importance = dict(zip(FEATURES, rf_model.feature_importances_))
print("\nFeature Importances:", json.dumps(importance, indent=2))

# Save models
with open('ml/model_lr.pkl', 'wb') as f:
    pickle.dump(lr_model, f)

with open('ml/model_rf.pkl', 'wb') as f:
    pickle.dump(rf_model, f)

with open('ml/scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)

print(f"\n Models saved! LR: {lr_acc:.2%}, RF: {rf_acc:.2%}")