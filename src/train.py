import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report
)
import joblib

# Resolve project root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, os.path.join(BASE_DIR, "src"))

from preprocessing import load_and_save_raw_data, prepare_data

def train_and_evaluate(data_path: str = None):
    """
    Trains Logistic Regression model, calculates metrics, saves artifacts and plots.
    """
    if data_path is None:
        data_path = os.path.join(BASE_DIR, "data", "raw", "breast_cancer.csv")
        
    if not os.path.exists(data_path):
        load_and_save_raw_data(data_path)
        
    X_train, X_test, X_train_scaled, X_test_scaled, y_train, y_test, scaler, feature_names = prepare_data(data_path)
    
    # 1. Initialize & Train Model
    clf = LogisticRegression(random_state=42, max_iter=1000, C=1.0)
    clf.fit(X_train_scaled, y_train)
    
    # 2. Predictions
    y_pred = clf.predict(X_test_scaled)
    y_prob = clf.predict_proba(X_test_scaled)[:, 1]
    
    # 3. Metrics Calculation
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)
    tn, fp, fn, tp = cm.ravel()
    
    results_dir = os.path.join(BASE_DIR, "results")
    models_dir = os.path.join(BASE_DIR, "models")
    os.makedirs(results_dir, exist_ok=True)
    os.makedirs(models_dir, exist_ok=True)
    
    # Save Model
    model_save_path = os.path.join(models_dir, "trained_model.pkl")
    joblib.dump(clf, model_save_path)
    print(f"[INFO] Model saved to {model_save_path}")
    
    # Save Metrics text
    report_str = classification_report(y_test, y_pred, target_names=['malignant', 'benign'])
    metrics_path = os.path.join(results_dir, "metrics.txt")
    with open(metrics_path, "w") as f:
        f.write("=== Model Evaluation Metrics ===\n")
        f.write(f"Accuracy:        {acc:.4f} ({acc*100:.2f}%)\n")
        f.write(f"Precision:       {prec:.4f} ({prec*100:.2f}%)\n")
        f.write(f"Recall:          {rec:.4f} ({rec*100:.2f}%)\n")
        f.write(f"F1-Score:        {f1:.4f} ({f1*100:.2f}%)\n\n")
        f.write("=== Confusion Matrix Breakdown ===\n")
        f.write(f"True Negatives (TN - Malignant as Malignant): {tn}\n")
        f.write(f"False Positives (FP - Malignant as Benign):   {fp}\n")
        f.write(f"False Negatives (FN - Benign as Malignant):   {fn}\n")
        f.write(f"True Positives (TP - Benign as Benign):       {tp}\n\n")
        f.write("=== Full Classification Report ===\n")
        f.write(report_str)
    
    print(f"[INFO] Metrics saved to {metrics_path}")
    print(f"Accuracy: {acc:.4f} | Precision: {prec:.4f} | Recall: {rec:.4f} | F1: {f1:.4f}")
    
    # 4. Generate Visualizations
    sns.set_theme(style="whitegrid")
    
    # Confusion Matrix Plot
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=['Malignant (0)', 'Benign (1)'],
                yticklabels=['Malignant (0)', 'Benign (1)'],
                cbar=False, annot_kws={"size": 14, "weight": "bold"})
    plt.title("Confusion Matrix - Logistic Regression", fontsize=13, weight='bold', pad=12)
    plt.xlabel("Predicted Class", fontsize=11, weight='bold')
    plt.ylabel("True Class", fontsize=11, weight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, "confusion_matrix.png"), dpi=300)
    plt.close()
    
    # Feature Importance (Coefficients) Plot
    coef_df = pd.DataFrame({
        'Feature': feature_names,
        'Coefficient': clf.coef_[0],
        'Abs_Coefficient': np.abs(clf.coef_[0])
    }).sort_values(by='Abs_Coefficient', ascending=False)
    
    plt.figure(figsize=(9, 6))
    top_features = coef_df.head(10)
    colors = ['#d9534f' if c < 0 else '#5cb85c' for c in top_features['Coefficient']]
    sns.barplot(x='Coefficient', y='Feature', data=top_features, palette=colors)
    plt.title("Top 10 Feature Weights (Logistic Regression Coefficients)", fontsize=13, weight='bold', pad=12)
    plt.xlabel("Coefficient Value (Negative -> Malignant, Positive -> Benign)", fontsize=11, weight='bold')
    plt.ylabel("Feature Name", fontsize=11, weight='bold')
    plt.axvline(0, color='black', linestyle='--', linewidth=0.8)
    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, "feature_importance.png"), dpi=300)
    plt.close()
    
    # Feature Distributions for Top Key Features
    df = pd.read_csv(data_path)
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    
    sns.histplot(data=df, x='worst texture', hue='target', kde=True, ax=axes[0],
                 palette={0: '#d9534f', 1: '#0275d8'}, element="step")
    axes[0].set_title("Distribution of Worst Texture by Class", fontsize=12, weight='bold')
    axes[0].set_xlabel("Worst Texture", fontsize=10, weight='bold')
    axes[0].set_ylabel("Count", fontsize=10, weight='bold')
    axes[0].legend(title="Target", labels=['Benign (1)', 'Malignant (0)'])
    
    sns.histplot(data=df, x='worst concave points', hue='target', kde=True, ax=axes[1],
                 palette={0: '#d9534f', 1: '#0275d8'}, element="step")
    axes[1].set_title("Distribution of Worst Concave Points by Class", fontsize=12, weight='bold')
    axes[1].set_xlabel("Worst Concave Points", fontsize=10, weight='bold')
    axes[1].set_ylabel("Count", fontsize=10, weight='bold')
    axes[1].legend(title="Target", labels=['Benign (1)', 'Malignant (0)'])
    
    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, "feature_distribution.png"), dpi=300)
    plt.close()
    
    # Correlation Heatmap for Top Influential Features
    plt.figure(figsize=(8, 6.5))
    top_cols = list(top_features['Feature'][:8]) + ['target']
    corr_mat = df[top_cols].corr()
    sns.heatmap(corr_mat, annot=True, fmt='.2f', cmap='coolwarm', vmin=-1, vmax=1,
                linewidths=0.5, cbar_kws={'label': 'Pearson Correlation'})
    plt.title("Correlation Heatmap (Top Predictors & Target)", fontsize=13, weight='bold', pad=12)
    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, "correlation_heatmap.png"), dpi=300)
    plt.close()
    
    print(f"[INFO] All result plots generated and saved to {results_dir}")

if __name__ == "__main__":
    train_and_evaluate()
