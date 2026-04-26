import numpy as np
import pandas as pd
import os
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.datasets import load_iris

# 1. Load the dataset
file_path = input("Enter dataset CSV file path (or press Enter to use sample Iris data): ").strip()

if file_path == "" or not os.path.exists(file_path):
    print("\nNo valid file provided. Loading sample Iris dataset...")
    iris = load_iris()
    data = pd.DataFrame(data=iris.data, columns=iris.feature_names)
    data['target'] = iris.target
else:
    data = pd.read_csv(file_path)

# --- PREPROCESSING ---
cols_to_drop = ['ID', 'Left-Fundus', 'Right-Fundus', 'Left-Diagnostic Keywords', 
                'Right-Diagnostic Keywords', 'filepath', 'labels', 'filename']
data = data.drop(columns=[c for c in cols_to_drop if c in data.columns])

if 'Patient Sex' in data.columns:
    data['Patient Sex'] = data['Patient Sex'].map({'Male': 1, 'Female': 0})

data = data.select_dtypes(include=[np.number]) 
data = data.dropna()

num_records = len(data)
num_features = data.shape[1] - 1
print(f"\nDataset Cleaned!")
print(f"Total Records: {num_records}")
print(f"Total Features: {num_features}")

# 2. Separate Features (X) and Target (Y)
X = data.iloc[:, :-1]
Y = data.iloc[:, -1]

# --- ADDED: User-defined training percentage ---
try:
    train_perc = input("\nEnter percentage of records for training (e.g., 80 for 80%): ")
    # Convert to decimal test_size (e.g., 80% train = 0.2 test)
    t_size = 1 - (float(train_perc) / 100) if train_perc.strip() else 0.2
    if not (0 < t_size < 1):
        raise ValueError
except ValueError:
    print("Invalid input. Using default 80% training / 20% testing.")
    t_size = 0.2

# 3. Split into training and testing sets
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=t_size, random_state=42)
print(f"Training with {len(X_train)} records. Testing with {len(X_test)} records.")

# 4. Get model hyperparameters
try:
    n_est = input("\nEnter number of trees (default 100): ")
    m_estimators = int(n_est) if n_est.strip() else 100
    
    crit = input("Enter criterion (gini/entropy, default gini): ").lower().strip()
    crit = crit if crit in ['gini', 'entropy'] else 'gini'
except ValueError:
    m_estimators = 100
    crit = 'gini'

# 5. Build and train
model = RandomForestClassifier(n_estimators=m_estimators, criterion=crit, random_state=42)
model.fit(X_train, Y_train)

# 6. Evaluate
Y_pred = model.predict(X_test)
print("\n--- Evaluation Metrics ---")
print(f"Accuracy:  {accuracy_score(Y_test, Y_pred):.4f}")
print(f"Precision: {precision_score(Y_test, Y_pred, average='weighted', zero_division=0):.4f}")
print(f"Recall:    {recall_score(Y_test, Y_pred, average='weighted', zero_division=0):.4f}")
print(f"F1-Score:  {f1_score(Y_test, Y_pred, average='weighted', zero_division=0):.4f}")

print("\n--- Confusion Matrix ---")
cm = confusion_matrix(Y_test, Y_pred)
print(cm)

# 7. K-Fold
try:
    k_input = input("\nEnter number of folds for K-Fold (default 5): ")
    k = int(k_input) if k_input.strip() else 5
    kf = KFold(n_splits=k, shuffle=True, random_state=42) 
    cv_scores = cross_val_score(model, X, Y, cv=kf)
    print(f"\nMean Accuracy ({k} folds): {np.mean(cv_scores):.4f}")
except Exception as e:
    print(f"K-Fold failed: {e}")
