import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, PageBreak, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """
    Custom two-pass canvas to dynamically compute and print 'Page X of Y'
    and header on all pages.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#2C3E50"))
        
        # Header (pages 2+)
        if self._pageNumber > 1:
            self.drawString(36, 762, "Machine Learning Intern Assignment Report — Diagnostic Classification")
            self.setFont("Helvetica", 8)
            self.drawRightString(576, 762, "Supervised Learning Pipeline")
            self.setStrokeColor(colors.HexColor("#BDC3C7"))
            self.setLineWidth(0.5)
            self.line(36, 756, 576, 756)
            
        # Footer (all pages)
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#7F8C8D"))
        self.setStrokeColor(colors.HexColor("#BDC3C7"))
        self.setLineWidth(0.5)
        self.line(36, 32, 576, 32)
        
        self.drawString(36, 22, "Confidential — Evaluated for Computer Science / AI Internship")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(576, 22, page_str)
        self.restoreState()

def build_pdf_report():
    pdf_path = r"C:\Users\rajee\Desktop\ml-intern-assignment\report\Internship_Assignment_Report.pdf"
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
    
    # 0.5 in margins = 36 pt
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=38
    )
    
    styles = getSampleStyleSheet()
    
    # Custom tight styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=18,
        textColor=colors.HexColor("#1A365D"),
        spaceAfter=3,
        spaceBefore=0
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#4A5568"),
        spaceAfter=6
    )
    
    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=12,
        textColor=colors.HexColor("#2B6CB0"),
        spaceBefore=6,
        spaceAfter=3,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'ReportBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#2D3748"),
        spaceAfter=3
    )
    
    bold_body_style = ParagraphStyle(
        'BoldReportBody',
        parent=body_style,
        fontName='Helvetica-Bold'
    )
    
    table_text_style = ParagraphStyle(
        'TableText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#2D3748")
    )
    
    table_hdr_style = ParagraphStyle(
        'TableHdr',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.white
    )

    story = []
    
    # ================= PAGE 1 =================
    story.append(Paragraph("Breast Cancer Diagnostic Classification: Supervised ML Pipeline", title_style))
    story.append(Paragraph("<b>Author:</b> Intern Candidate &nbsp;|&nbsp; <b>Domain:</b> Healthcare AI / Supervised Learning &nbsp;|&nbsp; <b>Stack:</b> Python, Scikit-Learn, Pandas", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E0"), spaceBefore=0, spaceAfter=5))
    
    # 1. Abstract & Objectives
    story.append(Paragraph("1. Abstract & Problem Statement", h1_style))
    abstract_text = (
        "Early and precise detection of breast carcinoma significantly improves clinical intervention efficacy and patient survival. "
        "This project develops an end-to-end, interpretable, and reproducible supervised machine learning pipeline to classify Fine Needle Aspirate "
        "(FNA) biopsy cell nuclei into <b>Malignant (0)</b> or <b>Benign (1)</b>. Formulated as a binary classification problem, we enforce strict leak-free "
        "preprocessing, stratified train/test partitioning, and probabilistic diagnostic inference using L2-regularized Logistic Regression."
    )
    story.append(Paragraph(abstract_text, body_style))
    
    # 2. Dataset Selection & Specifications
    story.append(Paragraph("2. Dataset Selection & Provenance", h1_style))
    dataset_text = (
        "The project utilizes the <b>Breast Cancer Wisconsin (Diagnostic) Dataset</b>, originally collected by Dr. William H. Wolberg, W. Nick Street, "
        "and Olvi L. Mangasarian at the University of Wisconsin-Madison and curated in Scikit-Learn / UCI ML Repository. It comprises <b>569 biopsy samples</b> "
        "and <b>30 continuous numerical features</b> representing 10 geometric characteristics of cell nuclei: radius, texture, perimeter, area, smoothness, "
        "compactness, concavity, concave points, symmetry, and fractal dimension (each measured as Mean, Standard Error, and Worst/Largest value)."
    )
    story.append(Paragraph(dataset_text, body_style))
    
    # Dataset specs table
    ds_data = [
        [Paragraph("<b>Metric</b>", table_hdr_style), Paragraph("<b>Specification / Value</b>", table_hdr_style), Paragraph("<b>Engineering Rationale</b>", table_hdr_style)],
        [Paragraph("Total Samples", table_text_style), Paragraph("569 biopsy records", table_text_style), Paragraph("Sufficient for convex statistical modeling without synthetic bias", table_text_style)],
        [Paragraph("Total Features", table_text_style), Paragraph("30 continuous real features", table_text_style), Paragraph("Captures rich cell nuclear geometry and contour variance", table_text_style)],
        [Paragraph("Target Variable", table_text_style), Paragraph("0: Malignant (212), 1: Benign (357)", table_text_style), Paragraph("Discrete binary clinical diagnosis (62.74% Benign : 37.26% Malignant)", table_text_style)],
        [Paragraph("Missing / Duplicates", table_text_style), Paragraph("0 missing, 0 duplicates", table_text_style), Paragraph("Integrity verified via automated auditing scripts", table_text_style)]
    ]
    t_ds = Table(ds_data, colWidths=[90, 150, 300])
    t_ds.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2B6CB0")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F7FAFC")])
    ]))
    story.append(t_ds)
    story.append(Spacer(1, 4))
    
    # 3. Exploratory Data Analysis & Visualizations
    story.append(Paragraph("3. Exploratory Data Analysis (EDA)", h1_style))
    eda_text = (
        "Statistical profiling reveals distinct morphological divergences between diagnostic classes. Malignant cell nuclei display significantly higher "
        "mean radius (17.46 vs 12.15), higher texture variance (21.60 vs 17.91), and extreme concave contour indentations (worst concave points: 0.182 vs 0.074). "
        "A correlation audit revealed pronounced multicollinearity between nuclear size attributes (radius, perimeter, area have <i>r</i> &gt; 0.98)."
    )
    story.append(Paragraph(eda_text, body_style))
    
    # Embed Distribution Image
    img_dist_path = r"C:\Users\rajee\Desktop\ml-intern-assignment\results\feature_distribution.png"
    if os.path.exists(img_dist_path):
        story.append(Image(img_dist_path, width=540, height=155))
        story.append(Paragraph("<i>Figure 1: Comparative density distributions of 'Worst Texture' and 'Worst Concave Points' partitioned by diagnosis.</i>", subtitle_style))
    
    story.append(PageBreak()) # End of Page 1
    
    # ================= PAGE 2 =================
    # 4. Data Preprocessing & Leakage Prevention
    story.append(Paragraph("4. Data Preprocessing & Data Leakage Prevention", h1_style))
    prep_text = (
        "<b>1. Feature/Target Separation:</b> The 30 geometric predictors were isolated into feature matrix <i>X</i> and diagnostic labels into target vector <i>y</i>.<br/>"
        "<b>2. Stratified Train/Test Split:</b> To preserve the natural 62.7% : 37.3% class ratio, an 80/20 stratified split was applied (<i>N</i><sub>train</sub>=455, <i>N</i><sub>test</sub>=114, random state=42).<br/>"
        "<b>3. Standard Feature Scaling:</b> Because morphological dimensions span disparate scales (e.g., area &gt; 2500 vs concavity &lt; 0.5), <code>StandardScaler</code> was fitted <b>strictly on the training partition</b> (<i>z</i> = (<i>x</i> - &mu;) / &sigma;). The test partition was transformed using training parameters, strictly preventing test-set data leakage."
    )
    story.append(Paragraph(prep_text, body_style))
    
    # 5. Model Selection
    story.append(Paragraph("5. Model Selection & Theoretical Justification", h1_style))
    model_text = (
        "<b>Selected Model: Logistic Regression (L2 Regularized, C=1.0).</b> Chosen for four core reasons: (1) <i>Calibrated Probabilistic Outputs:</i> Directly estimates malignancy confidence via the sigmoid function &sigma;(<i>z</i>) = 1/(1+e<sup>-z</sup>); (2) <i>Intrinsic Interpretability:</i> Learned weights represent linear log-odds; (3) <i>Convexity:</i> Guaranteed global convergence without stochastic instability; (4) <i>Regularization:</i> Ridge penalty prevents overfitting on collinear dimensions.<br/>"
        "<b>Alternative Model Considered: Decision Tree Classifier.</b> While offering transparent if-then decision boundaries, single decision trees suffer from high variance, axis-aligned partitioning artifacts, and uncalibrated step-function outputs, making regularized Logistic Regression superior for clinical diagnostics."
    )
    story.append(Paragraph(model_text, body_style))
    
    # 6. Experimental Results & Confusion Matrix
    story.append(Paragraph("6. Model Evaluation & Quantitative Results", h1_style))
    res_text = (
        "Evaluated on the unseen test partition (<i>N</i>=114), the model demonstrated exceptional diagnostic performance across all standard metrics:"
    )
    story.append(Paragraph(res_text, body_style))
    
    # Metrics Table & Confusion Matrix Image side-by-side / sequential
    metrics_data = [
        [Paragraph("<b>Metric</b>", table_hdr_style), Paragraph("<b>Formula</b>", table_hdr_style), Paragraph("<b>Score</b>", table_hdr_style), Paragraph("<b>Clinical Interpretation</b>", table_hdr_style)],
        [Paragraph("Accuracy", table_text_style), Paragraph("(TP+TN) / Total", table_text_style), Paragraph("<b>98.25%</b>", table_text_style), Paragraph("112 of 114 test biopsy cases correctly classified", table_text_style)],
        [Paragraph("Precision (Benign)", table_text_style), Paragraph("TP / (TP+FP)", table_text_style), Paragraph("<b>98.61%</b>", table_text_style), Paragraph("98.61% of predicted benign cases were truly benign", table_text_style)],
        [Paragraph("Recall (Benign)", table_text_style), Paragraph("TP / (TP+FN)", table_text_style), Paragraph("<b>98.61%</b>", table_text_style), Paragraph("98.61% of true benign cases were correctly detected", table_text_style)],
        [Paragraph("F1-Score", table_text_style), Paragraph("2*(P*R)/(P+R)", table_text_style), Paragraph("<b>98.61%</b>", table_text_style), Paragraph("Harmonic mean confirms balanced precision and recall", table_text_style)],
        [Paragraph("Malignant Recall", table_text_style), Paragraph("TN / (TN+FP)", table_text_style), Paragraph("<b>97.62%</b>", table_text_style), Paragraph("41 of 42 true malignant cancer biopsies detected", table_text_style)]
    ]
    t_m = Table(metrics_data, colWidths=[75, 80, 55, 330])
    t_m.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2B6CB0")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F7FAFC")])
    ]))
    story.append(t_m)
    story.append(Spacer(1, 4))
    
    # Embed Confusion Matrix and Heatmap
    img_cm_path = r"C:\Users\rajee\Desktop\ml-intern-assignment\results\confusion_matrix.png"
    img_corr_path = r"C:\Users\rajee\Desktop\ml-intern-assignment\results\correlation_heatmap.png"
    
    t_imgs = Table([
        [Image(img_cm_path, width=240, height=150), Image(img_corr_path, width=280, height=150)]
    ], colWidths=[255, 285])
    t_imgs.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0)
    ]))
    story.append(t_imgs)
    story.append(Paragraph("<i>Figure 2: Confusion matrix on unseen test set (Left) and Pearson correlation heatmap of top predictors (Right).</i>", subtitle_style))
    
    story.append(PageBreak()) # End of Page 2
    
    # ================= PAGE 3 =================
    # 7. Feature Influence Analysis
    story.append(Paragraph("7. Feature Influence Analysis (Coefficients)", h1_style))
    feat_text = (
        "In Logistic Regression, standardized feature coefficients (<i>w<sub>i</sub></i>) quantify the log-odds change per unit standard deviation. "
        "Because target class 0 represents malignancy, large negative weights indicate features strongly pushing predictions toward malignancy."
    )
    story.append(Paragraph(feat_text, body_style))
    
    img_fi_path = r"C:\Users\rajee\Desktop\ml-intern-assignment\results\feature_importance.png"
    if os.path.exists(img_fi_path):
        story.append(Image(img_fi_path, width=540, height=150))
        story.append(Paragraph("<i>Figure 3: Top 10 feature coefficients of the trained Logistic Regression model.</i>", subtitle_style))
        
    feat_findings = (
        "<b>Key Influential Predictors:</b> (1) <code>worst texture</code> (-1.26), (2) <code>radius error</code> (-1.08), (3) <code>worst concave points</code> (-0.95), "
        "and (4) <code>worst area</code> (-0.95). Clinically, higher grayscale texture variance and perimeter indentations strongly indicate malignant cell proliferation."
    )
    story.append(Paragraph(feat_findings, body_style))
    
    # 8. Error Analysis
    story.append(Paragraph("8. Error & Diagnostic Failure Analysis", h1_style))
    err_text = (
        "Out of 114 test samples, exactly <b>2 errors occurred (1.75% error rate)</b>: (1) <i>Sample #73 (False Positive / True Malignant):</i> A malignant tumor with atypically smooth nuclear margins near the decision boundary (predicted benign with 53.7% probability); (2) <i>Sample #541 (False Negative / True Benign):</i> A benign lesion exhibiting severe nuclear texture granularity that mimicked malignant dysplasia."
    )
    story.append(Paragraph(err_text, body_style))
    
    # 9. Conclusion & Improvements
    story.append(Paragraph("9. Conclusion & Engineering Improvements", h1_style))
    conc_text = (
        "<b>Conclusion:</b> The developed pipeline achieves high diagnostic reliability (98.25% Accuracy, 97.62% Malignant Recall) while maintaining full mathematical interpretability and instant inference (&lt;1 ms).<br/>"
        "<b>Future Improvements:</b> (1) <i>Asymmetric Cost Tuning:</i> Lowering decision threshold to 0.30 to penalize False Negatives heavily; (2) <i>Nested Cross-Validation:</i> Validating across 10-fold CV partitions; (3) <i>Multi-Center Clinical Testing:</i> Evaluating on external clinical hospital cohorts."
    )
    story.append(Paragraph(conc_text, body_style))
    
    # 10. References
    story.append(Paragraph("10. Data Source & Academic References", h1_style))
    ref_text = (
        "1. Wolberg, W.H., Street, W.N., & Mangasarian, O.L. (1995). <i>Breast Cancer Wisconsin (Diagnostic) Data Set</i>. UCI Machine Learning Repository.<br/>"
        "2. Pedregosa et al. (2011). <i>Scikit-learn: Machine Learning in Python</i>. Journal of Machine Learning Research (JMLR), 12, 2825-2830."
    )
    story.append(Paragraph(ref_text, body_style))
    
    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[SUCCESS] PDF report successfully compiled at: {pdf_path}")

if __name__ == "__main__":
    build_pdf_report()
