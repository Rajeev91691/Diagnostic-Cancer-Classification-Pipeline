# Breast Cancer Diagnostic Classification: Supervised Machine Learning Pipeline

A clean, reproducible, and production-structured Machine Learning internship project demonstrating the complete supervised classification lifecycle—from exploratory data analysis and leak-free preprocessing to model training, probabilistic evaluation, interpretability analysis, and serialized inference.

---

## 📌 Project Overview & Problem Statement

In clinical oncology, early and accurate classification of breast lesions is critical for patient survival. When a patient undergoes a Fine Needle Aspirate (FNA) biopsy, digital imaging extracts 30 quantitative geometric and morphological features of the cell nuclei (radius, texture, perimeter, area, smoothness, compactness, concavity, concave points, symmetry, and fractal dimension).

**Objective:** Build an interpretable, robust, and reproducible binary classification pipeline that accurately classifies biopsy samples as either:
* **`0` = Malignant** (Cancerous / High-risk)
* **`1` = Benign** (Non-cancerous / Safe)

---

## 🔬 Dataset Information

* **Dataset Name:** Breast Cancer Wisconsin (Diagnostic) Dataset
* **Source:** Originally collected by Dr. William H. Wolberg, W. Nick Street, and Olvi L. Mangasarian (University of Wisconsin-Madison). Distributed via the [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/17/breast+cancer+wisconsin+diagnostic) and curated in Scikit-Learn.
* **Samples:** 569 patient biopsy records
* **Features:** 30 continuous real-valued numerical features (10 cell nucleus characteristics $\times$ 3 metrics: Mean, Standard Error, and Worst/Largest Value).
* **Missing Values:** `0` (Zero missing values detected)
* **Duplicate Rows:** `0` (Zero duplicate records)
* **Class Distribution:** 357 Benign (62.74%), 212 Malignant (37.26%)

---

## 🛠️ Technologies Used

* **Language:** Python 3.11+
* **Data Processing & Analysis:** `pandas`, `numpy`
* **Machine Learning & Preprocessing:** `scikit-learn` (`StandardScaler`, `LogisticRegression`, `train_test_split`, `metrics`)
* **Data Visualization:** `matplotlib`, `seaborn`
* **Model Persistence & Artifacts:** `joblib`
* **Interactive Notebook:** `Jupyter Notebook`

---

## 📁 Project Directory Structure

```text
ml-intern-assignment/
│
├── data/
│   ├── raw/
│   │   └── breast_cancer.csv         # Raw tabular dataset (569 rows x 31 cols)
│   └── processed/
│       ├── X_train.npy               # Scaled training feature array (455 x 30)
│       ├── X_test.npy                # Scaled test feature array (114 x 30)
│       ├── y_train.npy               # Training labels
│       └── y_test.npy                # Testing labels
│
├── notebooks/
│   ├── ML_Intern_Assignment.ipynb    # Fully executed, end-to-end Jupyter Notebook
│   └── generate_notebook.py          # Notebook compilation and generation script
│
├── src/
│   ├── preprocessing.py              # Modular data loader, stratification & scaling
│   ├── train.py                      # Model training, metric logging & plot generation
│   └── predict.py                    # Inference script on new sample biopsies
│
├── models/
│   ├── trained_model.pkl             # Serialized Logistic Regression classifier
│   └── scaler.pkl                    # Serialized StandardScaler
│
├── results/
│   ├── confusion_matrix.png          # High-resolution confusion matrix plot
│   ├── feature_importance.png        # Top 10 feature coefficients bar chart
│   ├── feature_distribution.png      # Comparative KDE/Histograms by diagnosis
│   ├── correlation_heatmap.png       # Multicollinearity & target correlation heatmap
│   └── metrics.txt                   # Complete text report with precision/recall/F1
│
├── report/
│   ├── Internship_Assignment_Report.pdf  # Professional 3-page publication-ready PDF report
│   └── generate_pdf_report.py        # Automated PDF compiler script using ReportLab
│
├── requirements.txt                  # Clean project dependencies
├── README.md                         # Comprehensive documentation and run guide
└── .gitignore                        # Git configuration
```

---

## ⚙️ Methodology & Pipeline Architecture

```
  [1. Ingestion]       UCI Wisconsin Diagnostic Dataset (N=569, 30 features)
        │
        ▼
  [2. Data Audit]      Verified 0 Missing Values, 0 Duplicate Records
        │
        ▼
  [3. EDA]             Class Imbalance Audit (63% Benign : 37% Malignant), Histograms/KDE, Multicollinearity Heatmap
        │
        ▼
  [4. Preprocessing]   Stratified 80/20 Train/Test Split (N_train=455, N_test=114)
        │              Strictly fit StandardScaler on X_train (Zero Data Leakage)
        ▼
  [5. Model Selection] L2-Regularized Logistic Regression (C=1.0) for calibrated log-odds & clinical transparency
        │
        ▼
  [6. Evaluation]      Accuracy: 98.25% | Precision: 98.61% | Recall: 98.61% | F1-Score: 98.61%
        │              Confusion Matrix: TN=41, TP=71, FP=1, FN=1
        ▼
  [7. Diagnostics]     Coefficient Ranking (`worst texture`, `radius error`, `worst concave points`) & Error Root-Cause
        │
        ▼
  [8. Deployment]      Serialized via joblib (`trained_model.pkl`, `scaler.pkl`) with standalone inference CLI
```

---

## 📊 Experimental Results (Test Set, N=114)

| Metric | Score | Clinical Interpretation |
| :--- | :--- | :--- |
| **Accuracy** | **98.25%** | 112 out of 114 test biopsy samples correctly classified. |
| **Precision (Benign)** | **98.61%** | 98.61% of samples predicted as benign were truly non-cancerous. |
| **Recall (Benign)** | **98.61%** | 98.61% of all true benign biopsies were identified. |
| **F1-Score** | **98.61%** | Harmonic mean indicating balanced performance across classes. |
| **Malignant Recall (Sensitivity)** | **97.62%** | 41 out of 42 true malignant cancer cases accurately identified. |

### Confusion Matrix Breakdown
* **True Negatives (TN):** `41` (Malignant correctly classified as Malignant)
* **True Positives (TP):** `71` (Benign correctly classified as Benign)
* **False Positives (FP):** `1` (Malignant misclassified as Benign)
* **False Negatives (FN):** `1` (Benign misclassified as Malignant)

---

## 🚀 How to Run the Project

### 1. Clone & Set Up Environment
```bash
# Clone the repository / navigate to project root
cd ml-intern-assignment

# Create and activate virtual environment (optional but recommended)
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Execute Jupyter Notebook
```bash
jupyter notebook notebooks/ML_Intern_Assignment.ipynb
```
*Run all cells from top to bottom (`Cell` -> `Run All`).*

### 3. Run Modular Scripts
```bash
# 1. Run Preprocessing (Extracts data, computes stratified splits and scaler)
python src/preprocessing.py

# 2. Train Model & Export Evaluation Plots
python src/train.py

# 3. Test Inference on Sample Biopsy
python src/predict.py
```

---

## 📄 Deliverables Summary

1. **Jupyter Notebook:** `notebooks/ML_Intern_Assignment.ipynb` (Fully executed with rich Markdown and figures)
2. **Modular Source Code:** `src/preprocessing.py`, `src/train.py`, `src/predict.py`
3. **Serialized Models:** `models/trained_model.pkl`, `models/scaler.pkl`
4. **Visualizations & Metrics:** High-resolution PNGs and metrics log in `results/`
5. **Formal Report:** Maximum 3-page publication-ready PDF in `report/Internship_Assignment_Report.pdf`
6. **Video Presentation Script & Interview Q&A:** Embedded in repository documentation.
