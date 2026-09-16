import os
import numpy as np
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib

# Resolve project root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_and_save_raw_data(raw_data_path: str = None) -> pd.DataFrame:
    """
    Loads Breast Cancer Wisconsin dataset from scikit-learn and saves it to CSV.
    """
    if raw_data_path is None:
        raw_data_path = os.path.join(BASE_DIR, "data", "raw", "breast_cancer.csv")
        
    os.makedirs(os.path.dirname(raw_data_path), exist_ok=True)
    cancer = load_breast_cancer(as_frame=True)
    df = cancer.frame
    df.to_csv(raw_data_path, index=False)
    print(f"[INFO] Raw dataset saved to {raw_data_path} with shape {df.shape}")
    return df

def prepare_data(data_path: str = None,
                 test_size: float = 0.2,
                 random_state: int = 42):
    """
    Loads raw CSV, splits features/target, performs stratified train/test split,
    and applies standard scaling fitted strictly on training data.
    """
    if data_path is None:
        data_path = os.path.join(BASE_DIR, "data", "raw", "breast_cancer.csv")
        
    df = pd.read_csv(data_path)
    X = df.drop(columns=['target'])
    y = df['target']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Save processed splits and scaler for reproducibility
    processed_dir = os.path.join(BASE_DIR, "data", "processed")
    models_dir = os.path.join(BASE_DIR, "models")
    os.makedirs(processed_dir, exist_ok=True)
    os.makedirs(models_dir, exist_ok=True)
    
    joblib.dump(scaler, os.path.join(models_dir, "scaler.pkl"))
    np.save(os.path.join(processed_dir, "X_train.npy"), X_train_scaled)
    np.save(os.path.join(processed_dir, "X_test.npy"), X_test_scaled)
    np.save(os.path.join(processed_dir, "y_train.npy"), y_train.to_numpy())
    np.save(os.path.join(processed_dir, "y_test.npy"), y_test.to_numpy())
    
    print(f"[INFO] Preprocessing complete. Train: {X_train_scaled.shape}, Test: {X_test_scaled.shape}")
    return X_train, X_test, X_train_scaled, X_test_scaled, y_train, y_test, scaler, X.columns

if __name__ == "__main__":
    load_and_save_raw_data()
    prepare_data()
