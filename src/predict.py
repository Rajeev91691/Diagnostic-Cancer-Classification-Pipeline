import os
import sys
import joblib
import numpy as np
import pandas as pd

# Resolve project root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def predict_single_sample(sample_dict: dict = None):
    """
    Loads saved scaler and trained model, runs inference on a new sample.
    """
    model_path = os.path.join(BASE_DIR, "models", "trained_model.pkl")
    scaler_path = os.path.join(BASE_DIR, "models", "scaler.pkl")
    
    if not os.path.exists(model_path) or not os.path.exists(scaler_path):
        raise FileNotFoundError("Model or Scaler not found! Please run train.py first.")
        
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    
    # If no sample is passed, take a sample from the raw dataset
    if sample_dict is None:
        raw_df = pd.read_csv(os.path.join(BASE_DIR, "data", "raw", "breast_cancer.csv"))
        sample_row = raw_df.drop(columns=['target']).iloc[0:1]
        sample_label = raw_df['target'].iloc[0]
        print(f"[DEMO] Using sample 0 from dataset. Ground Truth Label: {'Benign' if sample_label == 1 else 'Malignant'} ({sample_label})")
        input_df = sample_row
    else:
        input_df = pd.DataFrame([sample_dict])
        
    # Scale input
    input_scaled = scaler.transform(input_df)
    
    # Predict
    pred_class = model.predict(input_scaled)[0]
    pred_proba = model.predict_proba(input_scaled)[0]
    
    label_map = {0: "Malignant (Cancerous)", 1: "Benign (Non-Cancerous)"}
    
    print("\n" + "="*50)
    print("           INFERENCE PREDICTION RESULT            ")
    print("="*50)
    print(f"Predicted Diagnosis   : {label_map[pred_class]}")
    print(f"Confidence Score      : {pred_proba[pred_class]*100:.2f}%")
    print(f"Probability [Malignant]: {pred_proba[0]*100:.2f}%")
    print(f"Probability [Benign]   : {pred_proba[1]*100:.2f}%")
    print("="*50 + "\n")
    
    return pred_class, pred_proba

if __name__ == "__main__":
    predict_single_sample()
