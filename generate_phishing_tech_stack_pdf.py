import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
)
from reportlab.pdfgen import canvas
import pypdf

class NumberedCanvas(canvas.Canvas):
    """Canvas that enables precise 'Page X of Y' numbering and running headers/footers."""
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
        self.setFillColor(colors.HexColor("#334155"))
        
        # Header on Page 2
        if self._pageNumber > 1:
            self.drawString(36, 762, "PHISHING DETECTION SYSTEM - EASY TECH STACK & VIVA GUIDE")
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawRightString(576, 762, "Machine Learning & Web Security Architecture")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.75)
            self.line(36, 754, 576, 754)
            
        # Footer on all pages
        footer_left = "Phishing Detection System | Simple Tech Stack Guide (Viva & Interview Ready)"
        footer_right = f"Page {self._pageNumber} of {page_count}"
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(36, 18, footer_left)
        self.drawRightString(576, 18, footer_right)
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.75)
        self.line(36, 28, 576, 28)
        
        self.restoreState()


def create_phishing_tech_stack_pdf(output_filepath):
    # Printable area: 612 x 792 pt. Margins 36 pt left/right, 26 pt top/bottom
    doc = SimpleDocTemplate(
        output_filepath,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=26,
        bottomMargin=26
    )

    styles = getSampleStyleSheet()
    
    # Modern Cybersecurity Color Palette
    PRIMARY = colors.HexColor("#0F172A")       # Deep Slate / Navy
    SECONDARY = colors.HexColor("#0284C7")     # Sky Blue
    DARK_BLUE = colors.HexColor("#1E3A8A")     # Royal Navy
    BODY_TEXT = colors.HexColor("#334155")     # Slate 700
    DARK_TEXT = colors.HexColor("#0F172A")     # Slate 900
    BG_LIGHT = colors.HexColor("#F8FAFC")      # Slate 50
    BORDER_CLR = colors.HexColor("#CBD5E1")    # Slate 300
    SUCCESS_BG = colors.HexColor("#F0FDF4")    # Emerald tint
    SUCCESS_BORDER = colors.HexColor("#86EFAC")

    # Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=16.5,
        leading=19,
        textColor=PRIMARY,
        spaceAfter=1
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=11.5,
        textColor=SECONDARY,
        spaceAfter=3
    )

    sec_h1 = ParagraphStyle(
        'SecH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.8,
        leading=12,
        textColor=PRIMARY,
        spaceBefore=3,
        spaceAfter=2,
        keepWithNext=True
    )

    tech_card_title = ParagraphStyle(
        'TechCardTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.8,
        leading=11,
        textColor=PRIMARY,
        spaceBefore=2,
        spaceAfter=1,
        keepWithNext=True
    )

    point_style = ParagraphStyle(
        'PointStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.4,
        leading=9.6,
        textColor=BODY_TEXT,
        leftIndent=6,
        spaceAfter=1
    )

    tbl_head_style = ParagraphStyle(
        'TblHead',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.3,
        leading=9.2,
        textColor=colors.white
    )

    tbl_cell_style = ParagraphStyle(
        'TblCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.0,
        leading=8.9,
        textColor=DARK_TEXT
    )

    tbl_cell_bold = ParagraphStyle(
        'TblCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.1,
        leading=8.9,
        textColor=PRIMARY
    )

    card_p = ParagraphStyle(
        'CardP',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.4,
        leading=9.8,
        textColor=DARK_TEXT
    )

    story = []

    # =========================================================================
    # PAGE 1: TITLE, INTRO CARD, SUMMARY TABLE & DEEP DIVE (PYTHON, SCIKIT-LEARN, PANDAS)
    # =========================================================================
    
    # Title & Subtitle Header
    story.append(Paragraph("Phishing Detection System - Tech Stack Explained", title_style))
    story.append(Paragraph("Easy Guide: What Tech Stack is Used, For What Purpose &amp; Why It Is Better Than Alternatives", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=SECONDARY, spaceBefore=0, spaceAfter=3))

    # Introduction Card (Simple & Clear)
    intro_html = """
    <b>In Simple Words:</b> This project detects fraudulent and deceptive phishing websites in real time to protect users from credential theft and online scams. Instead of relying on slow blocklists that fail against new attacks, the system inspects <b>50 security dimensions</b> (22 lexical URL features + 28 live webpage DOM behaviors) and classifies them using Machine Learning. As highlighted in the <b>Resume</b> and <b>Project Architecture</b>, the core stack consists of <b>Python, Scikit-learn (Random Forest), Flask, React.js, and Pandas</b>, supported by <b>BeautifulSoup4</b>. Here is exactly what each technology does and why it was chosen over other options.
    """
    intro_table = Table([[Paragraph(intro_html, card_p)]], colWidths=[540])
    intro_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#EFF6FF")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#93C5FD")),
        ('LEFTPADDING', (0, 0), (-1, -1), 7),
        ('RIGHTPADDING', (0, 0), (-1, -1), 7),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(intro_table)
    story.append(Spacer(1, 3))

    # SECTION 1: QUICK SUMMARY TABLE
    story.append(Paragraph("1. Quick-Summary: What Tech Stack is Used &amp; Why?", sec_h1))

    summary_data = [
        [
            Paragraph("Technology", tbl_head_style),
            Paragraph("What is it?", tbl_head_style),
            Paragraph("What Purpose in this Project?", tbl_head_style),
            Paragraph("Why Better Than Alternatives?", tbl_head_style)
        ],
        [
            Paragraph("<b>Python</b>", tbl_cell_bold),
            Paragraph("Programming Language", tbl_cell_style),
            Paragraph("Drives data processing, feature extraction (22 URL + 28 DOM metrics), and backend orchestration.", tbl_cell_style),
            Paragraph("<b>Better than Java/C++:</b> Unrivaled ML ecosystem, fastest regex/string parsing, clean syntax, and seamless library integration.", tbl_cell_style)
        ],
        [
            Paragraph("<b>Scikit-learn</b>", tbl_cell_bold),
            Paragraph("Machine Learning (Random Forest)", tbl_cell_style),
            Paragraph("Trained on 50,000+ samples to classify URLs as Legitimate or Phishing with 50-tree consensus voting.", tbl_cell_style),
            Paragraph("<b>Better than Deep Learning / Single Trees:</b> Blazing fast (&lt;2ms), no GPU needed, handles tabular security features best, and zero overfitting.", tbl_cell_style)
        ],
        [
            Paragraph("<b>Flask</b>", tbl_cell_bold),
            Paragraph("RESTful Backend Web Framework", tbl_cell_style),
            Paragraph("Exposes JSON scanning endpoint (<code>POST /api/predict</code>), handles CORS, and serves predictions to the UI.", tbl_cell_style),
            Paragraph("<b>Better than Django/Spring Boot:</b> Lightweight micro-framework, zero ORM/database overhead, sub-second cold starts, and minimal RAM footprint.", tbl_cell_style)
        ],
        [
            Paragraph("<b>React.js</b>", tbl_cell_bold),
            Paragraph("Frontend Single Page App (SPA)", tbl_cell_style),
            Paragraph("Provides real-time cyberpunk UI with 5-stage scanning animation, consensus gauges, and 50-feature inspect tables.", tbl_cell_style),
            Paragraph("<b>Better than Plain HTML/Jinja:</b> Instant reactive updates without full page reloads, smooth modular components, and rich visual UX.", tbl_cell_style)
        ],
        [
            Paragraph("<b>Pandas</b>", tbl_cell_bold),
            Paragraph("Data Science &amp; Feature Analysis", tbl_cell_style),
            Paragraph("Cleans the 50,000+ URL dataset, normalizes feature columns, splits train/test sets, and aligns vectors.", tbl_cell_style),
            Paragraph("<b>Better than Native Dictionaries:</b> High-performance vectorized matrix math, robust missing-value handling, and instant CSV processing.", tbl_cell_style)
        ],
        [
            Paragraph("<b>BeautifulSoup</b>", tbl_cell_bold),
            Paragraph("HTML DOM Parser &amp; Web Scraper", tbl_cell_style),
            Paragraph("Fetches target webpage HTML to detect hidden iframes, fake login popups, external form actions, and broken links.", tbl_cell_style),
            Paragraph("<b>Better than Selenium/Playwright:</b> Extremely fast, lightweight parsing without the heavy overhead and 10s latency of headless browsers.", tbl_cell_style)
        ]
    ]

    t_summary = Table(summary_data, colWidths=[68, 95, 187, 190])
    t_summary.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_CLR),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, BG_LIGHT]),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_summary)
    story.append(Spacer(1, 3))

    # SECTION 2: EASY EXPLANATION OF EACH TECHNOLOGY (PART 1)
    story.append(Paragraph("2. Simple Breakdown: Why Each Tech Stack Was Chosen", sec_h1))

    # Tech 1: Python
    story.append(Paragraph("A. Python - The Core Engineering Language", tech_card_title))
    story.append(Paragraph("<b>In Simple Words:</b> Python is the universal language that powers every layer of the system from web scraping to AI modeling.", point_style))
    story.append(Paragraph("<b>Purpose in Current Project:</b> Orchestrates lexical URL parsing, connects live web requests with HTML parsing, loads the serialized model via <code>joblib</code>, and executes the Flask backend server.", point_style))
    story.append(Paragraph("<b>Why it is Better than Java / C++ / PHP:</b> Java and C++ require verbose boilerplate code, explicit types, and compilation steps that slow down rapid experimentation. Python's rich scientific ecosystem (Scikit-learn, Pandas, NumPy, Urllib) allows end-to-end AI and cybersecurity development in one unified codebase with superior regex parsing speed.", point_style))

    # Tech 2: Scikit-learn & Random Forest
    story.append(Paragraph("B. Scikit-learn (Random Forest) - The Machine Learning Engine", tech_card_title))
    story.append(Paragraph("<b>In Simple Words:</b> The AI 'brain' trained to distinguish between genuine websites and cunning phishing copies.", point_style))
    story.append(Paragraph("<b>Purpose in Current Project:</b> An ensemble of 50 Decision Trees trained on 50,000+ labeled URL samples. It evaluates the 50 extracted security metrics simultaneously, calculates tree consensus (e.g., 49/50 trees voted Legitimate), and returns a calibrated risk score.", point_style))
    story.append(Paragraph("<b>Why it is Better than Deep Learning / SVM / Single Tree:</b> (1) <i>Tabular Superiority:</i> Tree ensembles consistently outperform Deep Neural Networks on structured tabular security features. (2) <i>Speed:</i> Traverses 50 trees in under 2 milliseconds without needing expensive GPUs. (3) <i>No Overfitting:</i> Single decision trees easily memorize noise, but Random Forest uses bootstrap aggregation (bagging) and random feature subsets to generalize accurately (~97.2% test accuracy).", point_style))

    # Tech 3: Pandas
    story.append(Paragraph("C. Pandas - The Data Science &amp; Vector Alignment Toolkit", tech_card_title))
    story.append(Paragraph("<b>In Simple Words:</b> High-speed data manipulation library that handles all dataset tables and feature matrices.", point_style))
    story.append(Paragraph("<b>Purpose in Current Project:</b> Curates and balances <code>MLDataset.csv</code>, manages train/test splits (<code>X_train</code>, <code>X_test</code>, <code>y_train</code>, <code>y_test</code>), removes corrupted rows, and ensures that the live extracted 50-feature vector aligns perfectly with the model's expected column schema.", point_style))
    story.append(Paragraph("<b>Why it is Better than Raw Python Dictionaries / SQL:</b> Python native lists and loops are slow when processing tens of thousands of rows. Pandas leverages optimized C-level vectorized operations, enabling instant column filtering, feature scaling, and zero-error alignment before sending vectors to Scikit-learn.", point_style))

    # Force Page Break to Page 2
    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: TECH BREAKDOWN PART 2, COMPARISON TABLE, 30-SEC PITCH & VIVA QA
    # =========================================================================

    # Tech 4: Flask
    story.append(Paragraph("D. Flask - The RESTful Micro-Web Service", tech_card_title))
    story.append(Paragraph("<b>In Simple Words:</b> The lightweight bridge connecting the user interface in the browser to the Python AI engine in the background.", point_style))
    story.append(Paragraph("<b>Purpose in Current Project:</b> Exposes the critical REST API endpoint <code>POST /api/predict</code>, sanitizes incoming URLs, coordinates the feature extractors, and responds with structured JSON containing verdict, confidence, and tree votes in under 1.5 seconds.", point_style))
    story.append(Paragraph("<b>Why it is Better than Django / Spring Boot / FastAPI:</b> Django is a heavy monolith packed with database ORMs, admin panels, and templates that are completely unnecessary for an ML API. Spring Boot (Java) consumes 400MB+ RAM and has slow boot times. Flask is minimalist (~40MB RAM), boots instantly, and connects directly to Python ML memory without serialization bottlenecks.", point_style))

    # Tech 5: React.js + Vite
    story.append(Paragraph("E. React.js &amp; Vite - The CyberGuard User Interface", tech_card_title))
    story.append(Paragraph("<b>In Simple Words:</b> The interactive, high-tech dashboard that users interact with to scan URLs and inspect security verdicts.", point_style))
    story.append(Paragraph("<b>Purpose in Current Project:</b> Renders a modern cyberpunk dark-mode interface with neon accents, a dynamic 5-stage scanning progress indicator, visual confidence dials, parsed URL breakdowns, and searchable tables inspecting all 50 extracted features.", point_style))
    story.append(Paragraph("<b>Why it is Better than Traditional Server-Rendered HTML / Jinja:</b> Server-rendered pages reload the entire browser window on every submission, creating a clunky user experience. React updates only the specific verdict components reactively without refreshing the page, delivering a desktop-app quality experience with instant state transitions.", point_style))

    # Tech 6: BeautifulSoup4
    story.append(Paragraph("F. BeautifulSoup4 &amp; Requests - Live Webpage Behavioral Inspector", tech_card_title))
    story.append(Paragraph("<b>In Simple Words:</b> The automated scanner that visits the webpage in the background to look for deceptive tricks inside the code.", point_style))
    story.append(Paragraph("<b>Purpose in Current Project:</b> Extracts 28 behavioral DOM features: external login form actions, password fields on unencrypted domains, hidden iframe overlays, alert popups, favicon discrepancies, and broken anchor links (e.g. <code>#</code>).", point_style))
    story.append(Paragraph("<b>Why it is Better than Headless Browsers (Selenium/Playwright):</b> Headless browsers launch full browser processes consuming 300MB+ RAM per scan and taking 8-15 seconds per URL. BeautifulSoup parses raw HTML in 200 milliseconds, giving real-time threat detection with negligible server load.", point_style))

    story.append(Spacer(1, 2))

    # SECTION 3: SIMPLE COMPARISON TABLE
    story.append(Paragraph("3. Simple Comparison: Our Stack vs Alternative Approaches", sec_h1))

    comp_data = [
        [
            Paragraph("Comparison Criteria", tbl_head_style),
            Paragraph("Our Stack<br/>(React + Flask + RF Ensemble)", tbl_head_style),
            Paragraph("Traditional Approach<br/>(Blacklist / DNS Blocklists)", tbl_head_style),
            Paragraph("Deep Learning Stack<br/>(TensorFlow / PyTorch LSTM)", tbl_head_style)
        ],
        [
            Paragraph("<b>Zero-Day Phishing Detection</b>", tbl_cell_style),
            Paragraph("<b>High (Real-Time):</b> Detects newly created fraudulent URLs instantly via feature patterns.", tbl_cell_style),
            Paragraph("<b>Zero:</b> Completely blind to new URLs until reported and blacklisted (4-8 hr delay).", tbl_cell_style),
            Paragraph("<b>Moderate-High:</b> Can detect patterns, but prone to high false-positive rates on unseen domains.", tbl_cell_style)
        ],
        [
            Paragraph("<b>Inference Speed &amp; Latency</b>", tbl_cell_style),
            Paragraph("<b>Blazing Fast:</b> Under 2ms for ML inference; total pipeline ~1.2s including web fetch.", tbl_cell_style),
            Paragraph("<b>Fast lookup:</b> Database check is fast, but static database misses active threats.", tbl_cell_style),
            Paragraph("<b>Slow:</b> Matrix multiplications require 50-200ms CPU time or dedicated GPU hardware.", tbl_cell_style)
        ],
        [
            Paragraph("<b>Model Transparency &amp; Explainability</b>", tbl_cell_style),
            Paragraph("<b>Full Transparency:</b> Tree consensus votes (e.g. 48/50 trees) + inspectable 50 features.", tbl_cell_style),
            Paragraph("<b>Binary only:</b> Returns 'listed' or 'not listed' with zero analytical reasoning.", tbl_cell_style),
            Paragraph("<b>Black Box:</b> Opaque neural network weights make decisions difficult to explain to end-users.", tbl_cell_style)
        ],
        [
            Paragraph("<b>Server Resource Footprint</b>", tbl_cell_style),
            Paragraph("<b>Minimal:</b> ~80 MB RAM total. Runs smoothly on any standard CPU server.", tbl_cell_style),
            Paragraph("<b>Low:</b> Just database lookups.", tbl_cell_style),
            Paragraph("<b>Heavy:</b> Demands high memory (1-2 GB RAM) and GPU acceleration for acceptable speed.", tbl_cell_style)
        ]
    ]

    t_comp = Table(comp_data, colWidths=[105, 150, 142, 143])
    t_comp.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), DARK_BLUE),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_CLR),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, BG_LIGHT]),
        ('TOPPADDING', (0, 0), (-1, -1), 1.8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1.8),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_comp)
    story.append(Spacer(1, 2))

    # SECTION 4: 30-SECOND VIVA PITCH
    story.append(Paragraph("4. How to Explain in 30 Seconds (Perfect Viva / Interview Answer)", sec_h1))

    pitch_box_html = """
    <b>Examiner Question:</b> <i>\"Why did you choose this tech stack for your Phishing Detection Project?\"</i><br/>
    <b>Your 30-Second Answer:</b> <i>\"We chose <b>Python</b> and <b>Scikit-learn's Random Forest</b> because tree ensembles offer the highest accuracy (~97.2%) on structured security metrics while providing instant sub-2ms inference and complete decision explainability via consensus voting. We selected <b>Flask</b> as a lightweight REST API to serve predictions without monolithic bloat, and coupled it with <b>React.js</b> to deliver a real-time reactive scanning dashboard that visualizes the 5-stage inspection flow. Finally, <b>Pandas</b> guaranteed clean feature alignment, and <b>BeautifulSoup</b> allowed fast behavioral DOM analysis without the heavy latency of browser automation.\"</i>
    """
    pitch_table = Table([[Paragraph(pitch_box_html, card_p)]], colWidths=[540])
    pitch_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), SUCCESS_BG),
        ('BOX', (0, 0), (-1, -1), 1, SUCCESS_BORDER),
        ('LEFTPADDING', (0, 0), (-1, -1), 7),
        ('RIGHTPADDING', (0, 0), (-1, -1), 7),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
    ]))
    story.append(pitch_table)
    story.append(Spacer(1, 2))

    # SECTION 5: TOP 4 QUICK VIVA QUESTIONS & DIRECT ANSWERS
    story.append(Paragraph("5. Top 4 Quick Viva Questions &amp; Direct Answers", sec_h1))

    viva_qa_data = [
        [
            Paragraph("<b>Q1: Why Random Forest instead of Deep Learning (e.g. CNN / LSTM) or Logistic Regression?</b><br/><b>Answer:</b> Deep Learning is designed for unstructured data (images/audio) and acts as an unexplainable black box requiring GPU acceleration. Logistic Regression assumes linear boundaries and fails on complex security relationships. Random Forest excels on tabular features, captures nonlinear threat patterns, runs in 2ms on CPU, and avoids overfitting via bootstrap aggregation.", card_p)
        ],
        [
            Paragraph("<b>Q2: Why React.js instead of traditional HTML templates (Jinja / PHP)?</b><br/><b>Answer:</b> Phishing scanning involves multiple stages (DNS check, lexical parsing, DOM scraping, ML inference). React enables dynamic progress bars and instant state updates without reloading the webpage. In traditional HTML, submitting a URL forces a full page reload, breaking the real-time scanning experience.", card_p)
        ],
        [
            Paragraph("<b>Q3: Why Flask instead of Django or FastAPI?</b><br/><b>Answer:</b> Django includes heavy ORMs, admin interfaces, and database migrations that an ML inference service never needs (~200MB overhead). Flask is a lightweight micro-framework (~40MB RAM) that mounts our Python ML pipeline with zero friction and sub-second startup.", card_p)
        ],
        [
            Paragraph("<b>Q4: How do the 22 Lexical and 28 DOM features work together?</b><br/><b>Answer:</b> Lexical features inspect URL structure (length, entropy, IP address hosting, subdomains) before visiting the site. DOM features inspect on-page deceptive tactics (fake login popups, hidden iframes, external credential submission forms). Combining both vectors catches zero-day attacks that lexical checks alone might miss.", card_p)
        ]
    ]
    t_viva = Table(viva_qa_data, colWidths=[540])
    t_viva.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), BG_LIGHT),
        ('BOX', (0, 0), (-1, -1), 1, BORDER_CLR),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_CLR),
        ('LEFTPADDING', (0, 0), (-1, -1), 7),
        ('RIGHTPADDING', (0, 0), (-1, -1), 7),
        ('TOPPADDING', (0, 0), (-1, -1), 2.2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.2),
    ]))
    story.append(t_viva)

    # Build PDF with custom NumberedCanvas
    doc.build(story, canvasmaker=NumberedCanvas)
    
    # Check page count
    reader = pypdf.PdfReader(output_filepath)
    num_pages = len(reader.pages)
    print(f"Generated PDF at: {output_filepath} (Total pages: {num_pages})")
    if num_pages > 2:
        raise ValueError(f"CRITICAL: PDF exceeded 2 pages! It has {num_pages} pages.")

if __name__ == "__main__":
    downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")
    if not os.path.exists(downloads_dir):
        os.makedirs(downloads_dir, exist_ok=True)
        
    download_pdf_path = os.path.join(downloads_dir, "Phishing_Detection_Tech_Stack_Guide.pdf")
    local_pdf_path = os.path.join(os.path.dirname(__file__), "Phishing_Detection_Tech_Stack_Guide.pdf")
    
    # Generate in Downloads folder
    create_phishing_tech_stack_pdf(download_pdf_path)
    
    # Also generate in local workspace for easy reference
    create_phishing_tech_stack_pdf(local_pdf_path)
