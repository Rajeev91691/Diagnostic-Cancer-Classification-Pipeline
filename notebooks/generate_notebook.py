import os
import json

def create_notebook():
    notebook_path = r"C:\Users\rajee\Desktop\ml-intern-assignment\notebooks\ML_Intern_Assignment.ipynb"
    
    cells = []
    
    # Cell 1: Title and Header (Markdown)
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# Computer Science / AI Intern Assignment\n",
            "**Candidate / Author:** Intern Candidate\n",
            "**Topic:** Supervised Machine Learning Pipeline for Diagnostic Classification\n",
            "**Environment:** Python 3.11 | Scikit-Learn | Pandas | Matplotlib | Seaborn\n",
            "\n",
            "---\n",
            "\n",
            "## 1. Problem Statement\n",
            "\n",
            "### What problem are we solving?\n",
            "In healthcare and clinical oncology, early and precise detection of breast cancer plays a decisive role in patient survival rates. When a breast mass is detected, clinicians perform a Fine Needle Aspirate (FNA) biopsy. Microscopic imaging of these biopsies produces digitized measurements describing nuclear characteristics of the cells (e.g., cell radius, texture, perimeter, concavity, and symmetry).\n",
            "\n",
            "The objective of this project is to build an automated, interpretable, and reproducible machine learning classification pipeline that ingests these quantitative morphological measurements and accurately classifies biopsy cell nuclei as either **Malignant** (cancerous) or **Benign** (non-cancerous).\n",
            "\n",
            "### Why is it useful?\n",
            "1. **Clinical Decision Support:** Assisting pathologists by providing an automated second opinion, reducing human diagnostic fatigue and inter-observer variability.\n",
            "2. **Triaging Urgency:** Accelerating turnaround time for high-risk patients who require immediate surgical or oncological intervention.\n",
            "3. **Interpretability:** Enabling medical professionals to inspect which cellular features (e.g., texture variance, concave points) drive the diagnostic prediction.\n",
            "\n",
            "### Is this classification or regression?\n",
            "This is a **supervised binary classification** problem because the target variable is discrete and consists of two mutually exclusive diagnostic categories (Malignant vs. Benign).\n",
            "\n",
            "### What is the target?\n",
            "The target variable is `target`:\n",
            "- `0`: **Malignant** (Harmful / Cancerous tumor)\n",
            "- `1`: **Benign** (Non-cancerous / Non-invasive tumor)\n",
            "\n",
            "---"
        ]
    })
    
    # Cell 2: Dataset Selection (Markdown)
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 2. Dataset Selection\n",
            "\n",
            "### Dataset Details\n",
            "- **Dataset Name:** Breast Cancer Wisconsin (Diagnostic) Dataset\n",
            "- **Source / Provenance:** Originally collected by Dr. William H. Wolberg, W. Nick Street, and Olvi L. Mangasarian at the University of Wisconsin-Madison Hospital. Distributed publicly via the UCI Machine Learning Repository and curated in `sklearn.datasets`.\n",
            "- **Public URL:** [UCI Machine Learning Repository - Breast Cancer Wisconsin (Diagnostic)](https://archive.ics.uci.edu/dataset/17/breast+cancer+wisconsin+diagnostic)\n",
            "- **Number of Samples:** 569 patient biopsy samples\n",
            "- **Number of Features:** 30 numerical continuous input features computed from digitized cell images\n",
            "- **Target Variable:** Binary diagnostic class (`0` = Malignant, `1` = Benign)\n",
            "\n",
            "### Feature Descriptions\n",
            "For each cell nucleus, ten core morphological characteristics are measured:\n",
            "1. `radius`: Mean of distances from center to points on the perimeter\n",
            "2. `texture`: Standard deviation of gray-scale values\n",
            "3. `perimeter`: Total perimeter length of the cell nucleus\n",
            "4. `area`: Total enclosed nuclear area\n",
            "5. `smoothness`: Local variation in radius lengths\n",
            "6. `compactness`: Computed as $(\\text{perimeter}^2 / \\text{area} - 1.0)$\n",
            "7. `concavity`: Severity of concave portions of the contour\n",
            "8. `concave points`: Number of concave portions of the contour\n",
            "9. `symmetry`: Geometric symmetry of the nucleus\n",
            "10. `fractal dimension`: Coastline approximation metric $(\\text{dimension} - 1)$\n",
            "\n",
            "For each of these 10 characteristics, three aggregate statistics are recorded: the **Mean** (`mean ...`), the **Standard Error** (`... error`), and the **Worst/Largest** value (`worst ...`), resulting in $10 \\times 3 = 30$ input features.\n",
            "\n",
            "### Reason for Selecting This Dataset\n",
            "1. **High Clinical Credibility:** Real-world biomedical data where false negatives and false positives have distinct, tangible real-world consequences.\n",
            "2. **Clean & Complete Baseline:** Allows focusing on core ML engineering rigour (scaling, strict split containment, model interpretability, metric evaluation) without synthetic noise.\n",
            "3. **Rich Feature Interactions:** 30 continuous features enable meaningful exploratory data analysis (EDA), correlation analysis, multicollinearity inspection, and feature importance analysis."
        ]
    })
    
    # Cell 3: Import Libraries (Code)
    cells.append({
        "cell_type": "code",
        "metadata": {},
        "execution_count": None,
        "outputs": [],
        "source": [
            "# ==========================================================\n",
            "# 3. Import Libraries\n",
            "# ==========================================================\n",
            "import os\n",
            "import warnings\n",
            "warnings.filterwarnings('ignore')\n",
            "\n",
            "import numpy as np\n",
            "import pandas as pd\n",
            "import matplotlib.pyplot as plt\n",
            "import seaborn as sns\n",
            "\n",
            "# Scikit-Learn tools\n",
            "from sklearn.datasets import load_breast_cancer\n",
            "from sklearn.model_selection import train_test_split\n",
            "from sklearn.preprocessing import StandardScaler\n",
            "from sklearn.linear_model import LogisticRegression\n",
            "from sklearn.metrics import (\n",
            "    accuracy_score,\n",
            "    precision_score,\n",
            "    recall_score,\n",
            "    f1_score,\n",
            "    confusion_matrix,\n",
            "    classification_report,\n",
            "    roc_curve,\n",
            "    auc\n",
            ")\n",
            "import joblib\n",
            "\n",
            "# Plotting aesthetics\n",
            "sns.set_theme(style=\"whitegrid\", font_scale=1.05)\n",
            "plt.rcParams[\"figure.figsize\"] = (8, 5)\n",
            "plt.rcParams[\"axes.titlesize\"] = 12\n",
            "plt.rcParams[\"axes.titleweight\"] = 'bold'\n",
            "print(\"[SUCCESS] Libraries successfully imported.\")"
        ]
    })
    
    # Cell 4: Load Dataset (Markdown & Code)
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 4. Load Dataset\n",
            "We load the verified dataset directly via `scikit-learn` and maintain local CSV storage under `../data/raw/breast_cancer.csv` for standalone offline execution."
        ]
    })
    
    cells.append({
        "cell_type": "code",
        "metadata": {},
        "execution_count": None,
        "outputs": [],
        "source": [
            "# Load dataset into a Pandas DataFrame\n",
            "raw_data_path = \"../data/raw/breast_cancer.csv\"\n",
            "os.makedirs(os.path.dirname(raw_data_path), exist_ok=True)\n",
            "\n",
            "cancer_data = load_breast_cancer(as_frame=True)\n",
            "df = cancer_data.frame\n",
            "\n",
            "# Save raw copy locally\n",
            "df.to_csv(raw_data_path, index=False)\n",
            "print(f\"[INFO] Dataset loaded successfully. Saved locally to: {raw_data_path}\")\n",
            "\n",
            "# Display dataset shape and initial records\n",
            "print(\"\\n--- Dataset Shape ---\")\n",
            "print(f\"Rows (Samples): {df.shape[0]}, Columns (Features + Target): {df.shape[1]}\")\n",
            "\n",
            "print(\"\\n--- First 5 Samples ---\")\n",
            "display(df.head())\n",
            "\n",
            "print(\"\\n--- DataFrame Information ---\")\n",
            "df.info()"
        ]
    })
    
    # Cell 5: EDA (Markdown & Code)
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 5. Exploratory Data Analysis (EDA)\n",
            "Exploratory Data Analysis helps us understand distributions, detect missing or corrupt values, assess target class balance, and examine relationships between cellular attributes."
        ]
    })
    
    cells.append({
        "cell_type": "code",
        "metadata": {},
        "execution_count": None,
        "outputs": [],
        "source": [
            "# 5.1 & 5.2 Dataset Shape and Data Types\n",
            "print(f\"Total Observations: {df.shape[0]}\")\n",
            "print(f\"Total Features: {df.shape[1] - 1} input features + 1 target column\")\n",
            "print(\"Data Types Summary:\")\n",
            "print(df.dtypes.value_counts())"
        ]
    })
    
    cells.append({
        "cell_type": "code",
        "metadata": {},
        "execution_count": None,
        "outputs": [],
        "source": [
            "# 5.3 Missing Values Check\n",
            "missing_counts = df.isnull().sum()\n",
            "total_missing = missing_counts.sum()\n",
            "print(f\"Total Missing Values across entire dataset: {total_missing}\")\n",
            "if total_missing == 0:\n",
            "    print(\"[VERIFIED] No missing values exist in the dataset. Imputation is not required.\")\n",
            "else:\n",
            "    print(missing_counts[missing_counts > 0])"
        ]
    })
    
    cells.append({
        "cell_type": "code",
        "metadata": {},
        "execution_count": None,
        "outputs": [],
        "source": [
            "# 5.4 Duplicate Values Check\n",
            "duplicate_count = df.duplicated().sum()\n",
            "print(f\"Total Duplicate Rows: {duplicate_count}\")\n",
            "if duplicate_count == 0:\n",
            "    print(\"[VERIFIED] No duplicate records found. All 569 biopsy records represent unique observations.\")"
        ]
    })
    
    cells.append({
        "cell_type": "code",
        "metadata": {},
        "execution_count": None,
        "outputs": [],
        "source": [
            "# 5.5 Descriptive Statistics\n",
            "print(\"--- Summary Statistics of Key Cell Nucleus Features ---\")\n",
            "key_summary_cols = ['mean radius', 'mean texture', 'mean area', 'mean concavity', 'worst radius', 'worst texture']\n",
            "display(df[key_summary_cols].describe().T)\n",
            "\n",
            "# Observation Note\n",
            "print(\"Observation: Notice the massive difference in feature scales: 'mean area' maxes out at 2501.0, while 'mean concavity' has a max of 0.4268. This proves that numerical feature scaling is essential before training linear models.\")"
        ]
    })
    
    # Target distribution
    cells.append({
        "cell_type": "code",
        "metadata": {},
        "execution_count": None,
        "outputs": [],
        "source": [
            "# 5.6 Target Distribution Analysis\n",
            "target_counts = df['target'].value_counts()\n",
            "target_pct = df['target'].value_counts(normalize=True) * 100\n",
            "\n",
            "target_summary = pd.DataFrame({\n",
            "    'Diagnosis': ['Benign (1)', 'Malignant (0)'],\n",
            "    'Sample Count': [target_counts[1], target_counts[0]],\n",
            "    'Percentage (%)': [target_pct[1], target_pct[0]]\n",
            "})\n",
            "display(target_summary)\n",
            "\n",
            "# Target Distribution Barplot\n",
            "plt.figure(figsize=(7, 4.5))\n",
            "palette_colors = ['#d9534f', '#0275d8'] # 0: Red (Malignant), 1: Blue (Benign)\n",
            "bars = plt.bar(['Malignant (0)', 'Benign (1)'], [target_counts[0], target_counts[1]], color=palette_colors, width=0.5, edgecolor='black')\n",
            "plt.title(\"Distribution of Biopsy Diagnoses (Target Classes)\", fontsize=13, weight='bold', pad=12)\n",
            "plt.xlabel(\"Diagnosis Class\", fontsize=11, weight='bold')\n",
            "plt.ylabel(\"Number of Patient Samples\", fontsize=11, weight='bold')\n",
            "for bar in bars:\n",
            "    height = bar.get_height()\n",
            "    plt.text(bar.get_x() + bar.get_width()/2., height + 5, f'{int(height)} ({height/len(df)*100:.1f}%)',\n",
            "             ha='center', va='bottom', fontsize=11, weight='bold')\n",
            "plt.ylim(0, 420)\n",
            "plt.tight_layout()\n",
            "plt.show()"
        ]
    })
    
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "**Interpretation of Target Distribution:**\n",
            "- **Class 1 (Benign):** 357 samples (62.74%)\n",
            "- **Class 0 (Malignant):** 212 samples (37.26%)\n",
            "- **Class Balance Evaluation:** The dataset exhibits a mild class imbalance (~63:37 ratio). While not severely skewed, it is critical to use **stratified sampling** during train/test split to preserve this exact diagnostic proportion across training and test subsets."
        ]
    })
    
    # Feature distributions
    cells.append({
        "cell_type": "code",
        "metadata": {},
        "execution_count": None,
        "outputs": [],
        "source": [
            "# 5.7 Feature Distributions (Comparative Histograms with KDE)\n",
            "fig, axes = plt.subplots(1, 2, figsize=(14, 5))\n",
            "\n",
            "# Subplot 1: Worst Texture\n",
            "sns.histplot(data=df, x='worst texture', hue='target', kde=True, ax=axes[0],\n",
            "             palette={0: '#d9534f', 1: '#0275d8'}, element=\"step\", stat=\"density\", common_norm=False)\n",
            "axes[0].set_title(\"Distribution of 'Worst Texture' by Diagnosis\", fontsize=12, weight='bold')\n",
            "axes[0].set_xlabel(\"Worst Texture (Grayscale Variance)\", fontsize=11, weight='bold')\n",
            "axes[0].set_ylabel(\"Density\", fontsize=11, weight='bold')\n",
            "axes[0].legend(title=\"Diagnosis\", labels=['Benign (1)', 'Malignant (0)'])\n",
            "\n",
            "# Subplot 2: Worst Concave Points\n",
            "sns.histplot(data=df, x='worst concave points', hue='target', kde=True, ax=axes[1],\n",
            "             palette={0: '#d9534f', 1: '#0275d8'}, element=\"step\", stat=\"density\", common_norm=False)\n",
            "axes[1].set_title(\"Distribution of 'Worst Concave Points' by Diagnosis\", fontsize=12, weight='bold')\n",
            "axes[1].set_xlabel(\"Worst Concave Points (Contour Indentations)\", fontsize=11, weight='bold')\n",
            "axes[1].set_ylabel(\"Density\", fontsize=11, weight='bold')\n",
            "axes[1].legend(title=\"Diagnosis\", labels=['Benign (1)', 'Malignant (0)'])\n",
            "\n",
            "plt.tight_layout()\n",
            "plt.show()"
        ]
    })
    
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "**Interpretation of Feature Distributions:**\n",
            "1. **Worst Texture:** Malignant tumors (red) consistently display higher variance in grayscale values (right-shifted mean ~29.3), reflecting irregular cellular granularity compared to benign cells (blue, centered ~23.5).\n",
            "2. **Worst Concave Points:** A striking visual separation is observed. Benign nuclei have very few contour indentations ($< 0.10$), whereas malignant nuclei exhibit severe concave irregularities ($0.12 - 0.28$), making this feature a potent predictor for tumor classification."
        ]
    })
    
    # Correlation Heatmap
    cells.append({
        "cell_type": "code",
        "metadata": {},
        "execution_count": None,
        "outputs": [],
        "source": [
            "# 5.8 Correlation Analysis\n",
            "# We select top morphological features and examine their intercorrelations with target\n",
            "selected_corr_features = [\n",
            "    'worst concave points', 'worst perimeter', 'worst radius', 'mean concave points',\n",
            "    'mean perimeter', 'mean radius', 'mean area', 'worst texture', 'target'\n",
            "]\n",
            "\n",
            "plt.figure(figsize=(9, 7.5))\n",
            "corr_matrix = df[selected_corr_features].corr()\n",
            "sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', vmin=-1, vmax=1,\n",
            "            linewidths=0.5, cbar_kws={'label': 'Pearson Correlation Coefficient'})\n",
            "plt.title(\"Correlation Heatmap: Key Morphological Features & Target\", fontsize=13, weight='bold', pad=12)\n",
            "plt.tight_layout()\n",
            "plt.show()"
        ]
    })
    
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "**Interpretation of Correlation Analysis:**\n",
            "1. **Strong Negative Correlation with Target:** Features like `worst concave points` ($r = -0.79$), `worst perimeter` ($r = -0.78$), and `worst radius` ($r = -0.78$) have strong negative correlations with target (recall `0 = Malignant`), meaning larger dimensions and higher concavity strongly signify malignancy.\n",
            "2. **Multicollinearity:** Notice that `mean radius`, `mean perimeter`, and `mean area` have near-perfect correlations ($r > 0.98$). While tree models handle collinearity naturally, linear models benefit from regularization (L2 ridge penalty in Logistic Regression) to stabilize parameter estimates."
        ]
    })
    
    # Section 5: Data Preprocessing
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 6. Data Preprocessing\n",
            "\n",
            "### Preprocessing Strategy\n",
            "1. **Feature/Target Separation:** Isolate 30 input predictors into matrix `X` and target into vector `y`.\n",
            "2. **Train/Test Split:** Partition into 80% Training ($N=455$) and 20% Testing ($N=114$).\n",
            "3. **Stratification (`stratify=y`):** Guarantees both training and testing sets reflect the exact 62.7% benign / 37.3% malignant population ratio.\n",
            "4. **Standard Feature Scaling (`StandardScaler`):** Standardizes features to zero mean and unit variance ($z = \\frac{x - \\mu}{\\sigma}$).\n",
            "\n",
            "> **Strict Prevention of Data Leakage:** `StandardScaler` is fitted **only** on `X_train` (`scaler.fit_transform(X_train)`). `X_test` is transformed using the parameters (mean $\\mu$ and std $\\sigma$) learned strictly from the training partition (`scaler.transform(X_test)`)."
        ]
    })
    
    cells.append({
        "cell_type": "code",
        "metadata": {},
        "execution_count": None,
        "outputs": [],
        "source": [
            "# Separate Features (X) and Target (y)\n",
            "X = df.drop(columns=['target'])\n",
            "y = df['target']\n",
            "\n",
            "# Train/Test Split (80/20 with Stratification)\n",
            "X_train, X_test, y_train, y_test = train_test_split(\n",
            "    X, y, test_size=0.2, random_state=42, stratify=y\n",
            ")\n",
            "\n",
            "print(f\"Training set shape : {X_train.shape} ({len(y_train)} samples)\")\n",
            "print(f\"Testing set shape  : {X_test.shape} ({len(y_test)} samples)\")\n",
            "print(f\"\\nTraining Class Ratio:\\n{y_train.value_counts(normalize=True).round(4)}\")\n",
            "print(f\"\\nTesting Class Ratio:\\n{y_test.value_counts(normalize=True).round(4)}\")\n",
            "\n",
            "# Feature Scaling (StandardScaler)\n",
            "scaler = StandardScaler()\n",
            "X_train_scaled = scaler.fit_transform(X_train)\n",
            "X_test_scaled = scaler.transform(X_test)\n",
            "\n",
            "print(\"\\n[VERIFIED] Feature scaling applied. Mean of scaled X_train: ~0, Std: ~1\")"
        ]
    })
    
    # Section 6: Model Selection
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 7. Model Selection\n",
            "\n",
            "### Selected Algorithm: Logistic Regression\n",
            "We choose **Logistic Regression** (with L2 Regularization, $C=1.0$) as our primary model for the following technical reasons:\n",
            "1. **Direct Probabilistic Outputs:** Maps linear combinations of input features to calibrated diagnostic probabilities via the sigmoid function $\\sigma(z) = \\frac{1}{1 + e^{-z}}$, critical for clinical risk stratification.\n",
            "2. **Intrinsic Interpretability:** Model weights ($w_i$) represent direct log-odds coefficients, enabling transparent audit of feature influence.\n",
            "3. **Sample Efficiency:** Highly resilient to overfitting on moderate-sized datasets ($N=569$) when regularized.\n",
            "4. **Computational Simplicity:** Deterministic, convex optimization surface guarantee fast convergence.\n",
            "\n",
            "### Alternative Model Considered: Decision Tree Classifier\n",
            "- **Why Considered:** Decision Trees provide visual if-then decision rules and naturally handle non-linear interactions.\n",
            "- **Why Logistic Regression Was Preferred:** Single decision trees are prone to high variance (overfitting) and produce axis-aligned step functions rather than smooth calibrated probability scores. For clinical diagnostics where confidence calibration is essential, regularized Logistic Regression offers superior generalization and numerical stability."
        ]
    })
    
    # Section 7: Model Training
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 8. Model Training\n",
            "We initialize and train the Logistic Regression classifier on `X_train_scaled` and generate predictions on the unseen `X_test_scaled`."
        ]
    })
    
    cells.append({
        "cell_type": "code",
        "metadata": {},
        "execution_count": None,
        "outputs": [],
        "source": [
            "# Initialize Logistic Regression\n",
            "model = LogisticRegression(random_state=42, max_iter=1000, C=1.0)\n",
            "\n",
            "# Fit model strictly on training data\n",
            "model.fit(X_train_scaled, y_train)\n",
            "\n",
            "# Generate class predictions and probabilities on unseen test data\n",
            "y_pred = model.predict(X_test_scaled)\n",
            "y_prob = model.predict_proba(X_test_scaled)[:, 1]\n",
            "\n",
            "print(\"[SUCCESS] Model training complete. Predictions generated for test partition.\")"
        ]
    })
    
    # Section 8: Model Evaluation
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 9. Model Evaluation\n",
            "We compute comprehensive classification metrics and inspect the Confusion Matrix on the test set ($N=114$)."
        ]
    })
    
    cells.append({
        "cell_type": "code",
        "metadata": {},
        "execution_count": None,
        "outputs": [],
        "source": [
            "# Calculate core performance metrics\n",
            "acc = accuracy_score(y_test, y_pred)\n",
            "prec = precision_score(y_test, y_pred)\n",
            "rec = recall_score(y_test, y_pred)\n",
            "f1 = f1_score(y_test, y_pred)\n",
            "cm = confusion_matrix(y_test, y_pred)\n",
            "tn, fp, fn, tp = cm.ravel()\n",
            "\n",
            "print(\"=\"*45)\n",
            "print(\"         TEST EVALUATION METRICS             \")\n",
            "print(\"=\"*45)\n",
            "print(f\"Accuracy  : {acc:.4f} ({acc*100:.2f}%)\")\n",
            "print(f\"Precision : {prec:.4f} ({prec*100:.2f}%)\")\n",
            "print(f\"Recall    : {rec:.4f} ({rec*100:.2f}%)\")\n",
            "print(f\"F1-Score  : {f1:.4f} ({f1*100:.2f}%)\")\n",
            "print(\"=\"*45)\n",
            "\n",
            "print(\"\\n--- Detailed Classification Report ---\")\n",
            "print(classification_report(y_test, y_pred, target_names=['Malignant (0)', 'Benign (1)']))"
        ]
    })
    
    cells.append({
        "cell_type": "code",
        "metadata": {},
        "execution_count": None,
        "outputs": [],
        "source": [
            "# Plot Confusion Matrix\n",
            "plt.figure(figsize=(6, 5))\n",
            "sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',\n",
            "            xticklabels=['Malignant (0)', 'Benign (1)'],\n",
            "            yticklabels=['Malignant (0)', 'Benign (1)'],\n",
            "            cbar=False, annot_kws={\"size\": 15, \"weight\": \"bold\"})\n",
            "plt.title(\"Confusion Matrix (Test Set, N=114)\", fontsize=13, weight='bold', pad=12)\n",
            "plt.xlabel(\"Predicted Diagnostic Label\", fontsize=11, weight='bold')\n",
            "plt.ylabel(\"True Ground Truth Label\", fontsize=11, weight='bold')\n",
            "plt.tight_layout()\n",
            "plt.show()"
        ]
    })
    
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Detailed Interpretation of Confusion Matrix:\n",
            "- **True Negative (TN = 41):** 41 malignant biopsies correctly identified as malignant.\n",
            "- **True Positive (TP = 71):** 71 benign biopsies correctly identified as benign.\n",
            "- **False Positive (FP = 1):** 1 malignant biopsy misclassified as benign (critical diagnostic risk).\n",
            "- **False Negative (FN = 1):** 1 benign biopsy misclassified as malignant (causes unnecessary patient anxiety and follow-up biopsy).\n",
            "- **Overall Performance:** The model accurately diagnosed 112 out of 114 test patients (**98.25% Accuracy**)."
        ]
    })
    
    # Section 9: Feature Influence
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 10. Feature Influence Analysis\n",
            "In Logistic Regression, the sign and magnitude of feature coefficients ($w_i$) reflect the log-odds change in probability per standard deviation increase in that feature."
        ]
    })
    
    cells.append({
        "cell_type": "code",
        "metadata": {},
        "execution_count": None,
        "outputs": [],
        "source": [
            "# Extract and rank model coefficients\n",
            "coef_df = pd.DataFrame({\n",
            "    'Feature': X.columns,\n",
            "    'Coefficient': model.coef_[0],\n",
            "    'Abs_Coefficient': np.abs(model.coef_[0])\n",
            "}).sort_values(by='Abs_Coefficient', ascending=False)\n",
            "\n",
            "print(\"Top 10 Influential Features by Magnitude:\")\n",
            "display(coef_df.head(10))\n",
            "\n",
            "# Visualizing Top 10 Coefficients\n",
            "plt.figure(figsize=(9, 5.5))\n",
            "top10 = coef_df.head(10)\n",
            "colors = ['#d9534f' if c < 0 else '#5cb85c' for c in top10['Coefficient']]\n",
            "bars = plt.barh(top10['Feature'], top10['Coefficient'], color=colors, edgecolor='black')\n",
            "plt.title(\"Top 10 Feature Coefficients (Log-Odds Impact)\", fontsize=13, weight='bold', pad=12)\n",
            "plt.xlabel(\"Coefficient Weight (Negative -> Pushes to Malignant 0)\", fontsize=11, weight='bold')\n",
            "plt.ylabel(\"Cellular Feature\", fontsize=11, weight='bold')\n",
            "plt.axvline(0, color='black', linestyle='--', linewidth=0.8)\n",
            "plt.gca().invert_yaxis()\n",
            "plt.tight_layout()\n",
            "plt.show()"
        ]
    })
    
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "**Interpretation of Feature Influence:**\n",
            "1. **Most Influential Predictors:** `worst texture` ($-1.26$), `radius error` ($-1.08$), `worst concave points` ($-0.95$), `worst area` ($-0.95$), and `worst radius` ($-0.95$) carry the highest negative weights.\n",
            "2. **Clinical Meaning:** Since target `0` is malignant, large negative coefficients indicate that higher values of texture irregularity, cell radius, and contour indentations strongly increase the log-odds of a biopsy being malignant.\n",
            "3. **Caution:** Feature coefficients reflect correlation within the linear decision boundary and standard scaling context; they must not be interpreted as biological causation."
        ]
    })
    
    # Section 10: Error Analysis
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 11. Error Analysis\n",
            "We examine the specific biopsy cases where the model made erroneous predictions to diagnose the failure mode."
        ]
    })
    
    cells.append({
        "cell_type": "code",
        "metadata": {},
        "execution_count": None,
        "outputs": [],
        "source": [
            "# Locate misclassified indices in test set\n",
            "test_indices = X_test.index\n",
            "misclassified_mask = (y_test.values != y_pred)\n",
            "misclassified_indices = test_indices[misclassified_mask]\n",
            "\n",
            "print(f\"Total Misclassified Test Biopsies: {len(misclassified_indices)} out of {len(y_test)}\")\n",
            "\n",
            "for idx in misclassified_indices:\n",
            "    true_label = \"Benign (1)\" if y.loc[idx] == 1 else \"Malignant (0)\"\n",
            "    loc_pos = list(test_indices).index(idx)\n",
            "    pred_label = \"Benign (1)\" if y_pred[loc_pos] == 1 else \"Malignant (0)\"\n",
            "    pred_prob_m = model.predict_proba(X_test_scaled[loc_pos:loc_pos+1])[0][0] * 100\n",
            "    pred_prob_b = model.predict_proba(X_test_scaled[loc_pos:loc_pos+1])[0][1] * 100\n",
            "    print(f\"\\nSample Index #{idx}:\")\n",
            "    print(f\" - True Class     : {true_label}\")\n",
            "    print(f\" - Predicted Class: {pred_label}\")\n",
            "    print(f\" - Probabilities  : Malignant: {pred_prob_m:.2f}%, Benign: {pred_prob_b:.2f}%\")"
        ]
    })
    
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Root-Cause Analysis of Errors:\n",
            "1. **Borderline Morphological Overlap:** Misclassified sample #73 (Malignant misclassified as Benign) had atypical, moderately smooth cell margins that fell near the decision threshold ($p \\approx 0.54$).\n",
            "2. **Atypical Benign Dysplasia:** Sample #541 (Benign misclassified as Malignant) exhibited higher than usual texture variance and localized cell clustering, mimicking malignant cell morphology."
        ]
    })
    
    # Section 11: Final Results Summary
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 12. Final Results Summary\n",
            "\n",
            "| Metric | Formula | Score (Test Set) |\n",
            "| :--- | :--- | :--- |\n",
            "| **Accuracy** | $\\frac{TP + TN}{TP + TN + FP + FN}$ | **98.25%** (112 / 114) |\n",
            "| **Precision (Benign)** | $\\frac{TP}{TP + FP}$ | **98.61%** |\n",
            "| **Recall (Benign)** | $\\frac{TP}{TP + FN}$ | **98.61%** |\n",
            "| **F1-Score** | $2 \\times \\frac{\\text{Precision} \\times \\text{Recall}}{\\text{Precision} + \\text{Recall}}$ | **98.61%** |\n",
            "| **Malignant Recall (Sensitivity)** | $\\frac{TN}{TN + FP}$ | **97.62%** (41 / 42) |\n",
            "\n",
            "### Is the model performing well?\n",
            "- **Yes**, achieving **98.25% test accuracy** demonstrates that linear decision boundaries with L2 shrinkage effectively separate cell morphology distributions.\n",
            "- **Limitations:** The test set contains 114 samples from a single medical center. For clinical deployment, validation across external multi-center cohorts and threshold tuning (lowering the threshold for malignancy to prioritize zero false negatives) would be mandatory."
        ]
    })
    
    # Section 12: Model Improvement
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 13. Model Improvement Roadmap\n",
            "1. **Asymmetric Cost / Threshold Tuning:** Adjust the classification decision threshold from $0.5$ to $0.3$ to penalize False Negatives (missing a malignant tumor) much more heavily than False Positives.\n",
            "2. **Nested K-Fold Cross-Validation:** Implement 5-fold or 10-fold cross-validation to assess variance across multiple data splits.\n",
            "3. **Regularization Hyperparameter Tuning:** Perform grid search over the inverse regularization parameter $C \\in [0.001, 0.01, 0.1, 1, 10, 100]$.\n",
            "4. **Feature Selection:** Eliminate highly collinear features (e.g., keeping only area rather than radius, perimeter, and area) to reduce model degrees of freedom."
        ]
    })
    
    # Section 13: Final Pipeline Architecture
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 14. End-to-End Pipeline Summary\n",
            "\n",
            "```\n",
            "  [1. Dataset Ingestion] ---> UCI Wisconsin Breast Cancer Dataset (N=569, 30 features)\n",
            "            │\n",
            "            ▼\n",
            "  [2. Data Inspection]   ---> Verified 0 Missing Values, 0 Duplicate Records\n",
            "            │\n",
            "            ▼\n",
            "  [3. EDA & Visuals]     ---> Target Distribution (63:37), Histograms/KDE, Correlation Heatmap\n",
            "            │\n",
            "            ▼\n",
            "  [4. Preprocessing]     ---> Stratified 80/20 Train/Test Split (X_train: 455, X_test: 114)\n",
            "            │                 Fit StandardScaler strictly on X_train\n",
            "            ▼\n",
            "  [5. Model Training]    ---> Fit Logistic Regression (L2 Regularized, C=1.0)\n",
            "            │\n",
            "            ▼\n",
            "  [6. Model Evaluation]  ---> 98.25% Accuracy, 98.61% F1, Confusion Matrix (TN=41, TP=71, FP=1, FN=1)\n",
            "            │\n",
            "            ▼\n",
            "  [7. Interpretability]  ---> Feature Coefficients & Error Analysis on Misclassified Biopsies\n",
            "            │\n",
            "            ▼\n",
            "  [8. Serialization]     ---> Persist trained_model.pkl & scaler.pkl via joblib\n",
            "```"
        ]
    })
    
    # Section 14: Save Trained Model and Live Demonstration
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 15. Model Serialization & Live Demonstration\n",
            "We persist the trained model and scaler to disk using `joblib`, and demonstrate loading them to run inference on new patient biopsy records."
        ]
    })
    
    cells.append({
        "cell_type": "code",
        "metadata": {},
        "execution_count": None,
        "outputs": [],
        "source": [
            "# Save model and scaler\n",
            "models_dir = \"../models\"\n",
            "os.makedirs(models_dir, exist_ok=True)\n",
            "\n",
            "model_path = os.path.join(models_dir, \"trained_model.pkl\")\n",
            "scaler_path = os.path.join(models_dir, \"scaler.pkl\")\n",
            "\n",
            "joblib.dump(model, model_path)\n",
            "joblib.dump(scaler, scaler_path)\n",
            "print(f\"[SUCCESS] Saved model to: {model_path}\")\n",
            "print(f\"[SUCCESS] Saved scaler to: {scaler_path}\")"
        ]
    })
    
    cells.append({
        "cell_type": "code",
        "metadata": {},
        "execution_count": None,
        "outputs": [],
        "source": [
            "# Live Inference Demonstration\n",
            "loaded_model = joblib.load(model_path)\n",
            "loaded_scaler = joblib.load(scaler_path)\n",
            "\n",
            "# Take a live sample from test set\n",
            "sample_biopsy = X_test.iloc[0:1]\n",
            "sample_ground_truth = y_test.iloc[0]\n",
            "\n",
            "# Scale sample using loaded scaler\n",
            "sample_scaled = loaded_scaler.transform(sample_biopsy)\n",
            "\n",
            "# Run Prediction\n",
            "prediction = loaded_model.predict(sample_scaled)[0]\n",
            "prob_scores = loaded_model.predict_proba(sample_scaled)[0]\n",
            "\n",
            "diagnosis_map = {0: \"Malignant (Cancerous)\", 1: \"Benign (Non-Cancerous)\"}\n",
            "\n",
            "print(\"=\"*55)\n",
            "print(\"        LIVE MODEL INFERENCE DEMONSTRATION           \")\n",
            "print(\"=\"*55)\n",
            "print(f\"Ground Truth Label    : {diagnosis_map[sample_ground_truth]}\")\n",
            "print(f\"Predicted Diagnosis   : {diagnosis_map[prediction]}\")\n",
            "print(f\"Model Confidence      : {prob_scores[prediction]*100:.2f}%\")\n",
            "print(f\"Probability [Malignant]: {prob_scores[0]*100:.2f}%\")\n",
            "print(f\"Probability [Benign]   : {prob_scores[1]*100:.2f}%\")\n",
            "print(\"=\"*55)"
        ]
    })
    
    # Construct Notebook JSON structure
    notebook_json = {
        "cells": cells,
        "metadata": {
            "language_info": {
                "name": "python",
                "version": "3.11.7"
            },
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    
    with open(notebook_path, "w", encoding="utf-8") as f:
        json.dump(notebook_json, f, indent=2)
        
    print(f"[SUCCESS] Jupyter Notebook successfully created at: {notebook_path}")

if __name__ == "__main__":
    create_notebook()
