"""
generate_interview_guide_pdf.py
Generates the Master Technical Study Guide & Comprehensive Interview Dossier
for the Scoutline Custom Object Detection Engine (YOLOv8n).
"""

import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable, Image as RLImage
)
from reportlab.pdfgen import canvas

# ----------------------------------------------------------------------
# 1. NUMBERED CANVAS WITH RUNNING HEADERS & FOOTERS
# ----------------------------------------------------------------------
class NumberedCanvas(canvas.Canvas):
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
            self.draw_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_decorations(self, page_count):
        if self._pageNumber == 1:
            return  # Suppress headers and footers on Cover Page

        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))

        # Running Header
        self.drawString(40, 755, "SCOUTLINE VISION STUDIO  |  TECHNICAL INTERVIEW DOSSIER & STUDY MANUAL")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(40, 748, letter[0] - 40, 748)

        # Running Footer
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(40, 42, letter[0] - 40, 42)

        self.drawString(40, 30, "Custom 7-Class YOLOv8 Engine · Real-Time CV Architecture & Engineering Defense")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 40, 30, page_str)

        self.restoreState()


# ----------------------------------------------------------------------
# 2. STYLE FACTORY & PALETTE
# ----------------------------------------------------------------------
def setup_styles():
    styles = getSampleStyleSheet()

    # Base Palette
    NAVY = colors.HexColor("#0F172A")
    SLATE = colors.HexColor("#334155")
    MUTED = colors.HexColor("#64748B")
    RED = colors.HexColor("#DC2626")
    CYAN = colors.HexColor("#0284C7")
    DARK_BG = colors.HexColor("#1E293B")

    styles.add(ParagraphStyle(
        "CoverTag",
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=12,
        textColor=RED,
        spaceAfter=8,
        textTransform="uppercase",
        letterSpacing=1.5
    ))
    styles.add(ParagraphStyle(
        "CoverTitle",
        fontName="Helvetica-Bold",
        fontSize=25,
        leading=30,
        textColor=NAVY,
        spaceAfter=12
    ))
    styles.add(ParagraphStyle(
        "CoverSubtitle",
        fontName="Helvetica",
        fontSize=12,
        leading=16,
        textColor=SLATE,
        spaceAfter=20
    ))

    styles.add(ParagraphStyle(
        "DocHeading1",
        fontName="Helvetica-Bold",
        fontSize=16,
        leading=20,
        textColor=NAVY,
        spaceBefore=16,
        spaceAfter=8,
        keepWithNext=True
    ))
    styles.add(ParagraphStyle(
        "DocHeading2",
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=CYAN,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    ))
    styles.add(ParagraphStyle(
        "DocHeading3",
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=14,
        textColor=SLATE,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    ))
    styles.add(ParagraphStyle(
        "DocBody",
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=SLATE,
        spaceAfter=6
    ))
    styles.add(ParagraphStyle(
        "DocBodyBold",
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=13,
        textColor=NAVY,
        spaceAfter=6
    ))
    styles.add(ParagraphStyle(
        "DocBullet",
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=SLATE,
        leftIndent=14,
        firstLineIndent=-10,
        spaceAfter=4
    ))
    styles.add(ParagraphStyle(
        "CodeText",
        fontName="Courier",
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor("#0F172A")
    ))
    styles.add(ParagraphStyle(
        "CodeHeader",
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#FFFFFF")
    ))
    styles.add(ParagraphStyle(
        "CalloutText",
        fontName="Helvetica",
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#1E293B")
    ))
    styles.add(ParagraphStyle(
        "QuestionTitle",
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=14,
        textColor=RED,
        spaceBefore=8,
        spaceAfter=3,
        keepWithNext=True
    ))
    styles.add(ParagraphStyle(
        "AnswerText",
        fontName="Helvetica",
        fontSize=8.5,
        leading=12.5,
        textColor=SLATE,
        spaceAfter=6
    ))
    styles.add(ParagraphStyle(
        "TableHead",
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=11,
        textColor=colors.white
    ))
    styles.add(ParagraphStyle(
        "TableCell",
        fontName="Helvetica",
        fontSize=8,
        leading=11,
        textColor=SLATE
    ))
    styles.add(ParagraphStyle(
        "TableCellBold",
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=11,
        textColor=NAVY
    ))

    return styles


# ----------------------------------------------------------------------
# 3. HELPER FLOWABLE BUILDERS
# ----------------------------------------------------------------------
def make_callout(title, text, styles, accent_color=colors.HexColor("#0284C7"), bg_color=colors.HexColor("#F0F9FF")):
    content = [
        Paragraph(f"<b>{title}</b>", ParagraphStyle('CT', fontName='Helvetica-Bold', fontSize=9, leading=12, textColor=accent_color)),
        Spacer(1, 3),
        Paragraph(text, styles['CalloutText'])
    ]
    t = Table([[content]], colWidths=[letter[0] - 80])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg_color),
        ('LINELEFT', (0,0), (0,-1), 3.5, accent_color),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    return t

def make_code_box(title, code_str, styles):
    header = Paragraph(f"<b>CODE SNIPPET: {title}</b>", styles['CodeHeader'])
    code_p = Paragraph(code_str.replace("\n", "<br/>").replace(" ", "&nbsp;"), styles['CodeText'])

    header_table = Table([[header]], colWidths=[letter[0] - 80])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#0F172A")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))

    code_table = Table([[code_p]], colWidths=[letter[0] - 80])
    code_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))

    return KeepTogether([header_table, code_table, Spacer(1, 6)])

def make_qa_card(num, question, answer, takeaway, styles):
    items = [
        Paragraph(f"<b>Q{num}: {question}</b>", styles['QuestionTitle']),
        Spacer(1, 2),
        Paragraph(f"<b>Comprehensive Answer:</b> {answer}", styles['AnswerText']),
    ]
    if takeaway:
        items.extend([
            Spacer(1, 2),
            Paragraph(f"<b>💡 Interviewer Impact Note:</b> {takeaway}", ParagraphStyle('TT', fontName='Helvetica-Oblique', fontSize=8, leading=11, textColor=colors.HexColor("#0284C7")))
        ])

    card = Table([[items]], colWidths=[letter[0] - 80])
    card.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor("#E2E8F0")),
        ('LINELEFT', (0,0), (0,-1), 3, colors.HexColor("#DC2626")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    return KeepTogether([card, Spacer(1, 6)])


# ----------------------------------------------------------------------
# 4. DOCUMENT ASSEMBLY
# ----------------------------------------------------------------------
def generate_pdf(output_pdf_path):
    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=46,
        bottomMargin=46
    )

    styles = setup_styles()
    story = []

    # ==================================================================
    # COVER PAGE
    # ==================================================================
    story.append(Spacer(1, 15))
    story.append(Paragraph("PROJECT DOSSIER & COMPREHENSIVE INTERVIEW DEFENSE MANUAL", styles['CoverTag']))
    story.append(Paragraph("Custom Object Detection Engine & Scoutline Vision Studio", styles['CoverTitle']))
    story.append(Paragraph(
        "An in-depth technical handbook covering deep learning theory (YOLOv8 Anchor-Free Architecture), "
        "large-scale dataset engineering (26,756 images, 7 classes), Kaggle GPU training pipelines, "
        "multimodal desktop & WebRTC inference pipelines, line-by-line code walk-throughs, and 40+ rigorous interview defense questions.",
        styles['CoverSubtitle']
    ))
    story.append(HRFlowable(width="100%", thickness=2.5, color=colors.HexColor("#DC2626"), spaceBefore=0, spaceAfter=15))

    # Cover Summary Specs Table
    specs_data = [
        [Paragraph("Specification Parameter", styles['TableHead']), Paragraph("Engineering Implementation Value", styles['TableHead']), Paragraph("Architectural Rationale", styles['TableHead'])],
        [Paragraph("Target Classes (7)", styles['TableCellBold']), Paragraph("person, bottle, cellphone, laptop, chair, pen, pencil", styles['TableCell']), Paragraph("Common workplace/classroom objects with extreme aspect ratio variance", styles['TableCell'])],
        [Paragraph("Base Architecture", styles['TableCellBold']), Paragraph("YOLOv8 Nano (YOLOv8n)", styles['TableCell']), Paragraph("Anchor-free, decoupled head, CSPDarknet53 with C2f & SPPF modules", styles['TableCell'])],
        [Paragraph("Model Scale & Parameters", styles['TableCellBold']), Paragraph("3,012,213 (~3.01M params) · 8.2 GFLOPs · 130 layers", styles['TableCell']), Paragraph("Ultra-lightweight footprint enabling >30 FPS CPU inference and low memory overhead", styles['TableCell'])],
        [Paragraph("Dataset Magnitude", styles['TableCellBold']), Paragraph("26,756 images (20,092 Train / 4,413 Valid / 2,251 Test)", styles['TableCell']), Paragraph("Multi-source validated dataset formatted strictly in normalized YOLO format", styles['TableCell'])],
        [Paragraph("Validation Performance", styles['TableCellBold']), Paragraph("mAP@50: 78.5% · Precision: 81.9% · Recall: 71.5% · mAP@50-95: 49.8%", styles['TableCell']), Paragraph("High precision avoids false positives in automated surveillance/productivity tracking", styles['TableCell'])],
        [Paragraph("Compute Environment", styles['TableCellBold']), Paragraph("Kaggle GPU (Tesla T4/P100 16GB) · PyTorch · AMP (FP16)", styles['TableCell']), Paragraph("Automatic Mixed Precision enabled 2x faster forward/backward passes", styles['TableCell'])],
        [Paragraph("Web Application", styles['TableCellBold']), Paragraph("Scoutline Vision Studio (Streamlit + WebRTC + PyAV)", styles['TableCell']), Paragraph("Cyber-Dark aesthetic with decoupled asynchronous HD video streaming engine", styles['TableCell'])],
        [Paragraph("Core Innovations", styles['TableCellBold']), Paragraph("Async WebRTC decoupling · Stride interpolation · H.264 PyAV muxing", styles['TableCell']), Paragraph("Eliminated 60-second WebRTC buffer timeouts and enabled native browser playback", styles['TableCell'])],
    ]
    t_specs = Table(specs_data, colWidths=[130, 200, 202])
    t_specs.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0F172A")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#FFFFFF"), colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 4.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_specs)
    story.append(Spacer(1, 15))

    # Meta banner
    story.append(make_callout(
        "CONFIDENTIAL & EXCLUSIVE STUDY RESOURCE",
        "This master document was constructed specifically for comprehensive interview preparation, technical system defenses, "
        "and architectural deep dives. It equips the candidate to answer advanced questions regarding computer vision math, "
        "convolutional operations, multi-threading architectures, real-time video codecs, and production edge deployment.",
        styles,
        accent_color=colors.HexColor("#DC2626"),
        bg_color=colors.HexColor("#FEF2F2")
    ))

    story.append(PageBreak())

    # ==================================================================
    # TABLE OF CONTENTS
    # ==================================================================
    story.append(Paragraph("Table of Contents", styles['DocHeading1']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E1"), spaceBefore=2, spaceAfter=8))

    toc_items = [
        ("1.0", "Executive Summary & High-Level System Architecture", "Project genesis, pipeline workflow, system block diagram, and benchmark KPIs."),
        ("2.0", "Computer Vision & YOLO Theoretical Deep Dive", "R-CNN vs YOLO, YOLOv8 architecture (Backbone, C2f, SPPF, Neck, Decoupled Head), Anchor-Free logic, Loss formulas (CIoU, DFL, BCE), NMS, and evaluation metrics."),
        ("3.0", "Dataset Engineering, Cleansing & Validation", "Multi-source dataset construction (26,756 images), 7-class distribution, YOLO format normalization, line-by-line breakdown of validate_merged_dataset.py, and augmentation tactics."),
        ("4.0", "Model Training, Kaggle GPU Acceleration & Metrics", "Compute setup, transfer learning from COCO, hyperparameter grid, AMP (FP16), validation metrics curves (mAP, Precision, Recall, Losses), and model size trade-offs."),
        ("5.0", "Desktop & Offline Inference Pipelines (Code Walkthroughs)", "Line-by-line technical deep dive of image_detector.py, video_detector.py, and webcam_detector.py (DirectShow, EMA FPS smoothing, Tkinter dialogs)."),
        ("6.0", "Production Web Application: Scoutline Vision Studio", "Full analysis of streamlit-app/app.py: Cyber-Dark UI tokens, Image Scan telemetry, Video Trace PyAV H.264 engine with 2x balanced stride, and AsyncHDLiveStreamProcessor decoupling."),
        ("7.0", "Master Technical Interview Q&A Playbook (40+ Questions)", "Comprehensive question bank covering CV math, dataset curation, real-time video streaming, multi-threading, edge optimization, and system design."),
        ("8.0", "Interview Delivery Playbook & Elevator Pitch", "60-second elevator pitch, 5-minute technical walkthrough, how to discuss the WebRTC buffer bloat fix, failure modes, and scaling to 10,000 edge streams."),
    ]

    toc_data = [[Paragraph("Section", styles['TableHead']), Paragraph("Module Title", styles['TableHead']), Paragraph("Key Technical Subject Matter Covered", styles['TableHead'])]]
    for sec, title, desc in toc_items:
        toc_data.append([
            Paragraph(f"<b>{sec}</b>", styles['TableCellBold']),
            Paragraph(f"<b>{title}</b>", styles['TableCellBold']),
            Paragraph(desc, styles['TableCell'])
        ])
    t_toc = Table(toc_data, colWidths=[40, 180, 312])
    t_toc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0F172A")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#FFFFFF"), colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_toc)
    story.append(Spacer(1, 10))

    # ==================================================================
    # SECTION 1: EXECUTIVE SUMMARY & SYSTEM ARCHITECTURE
    # ==================================================================
    story.append(Paragraph("1.0 Executive Summary & High-Level System Architecture", styles['DocHeading1']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E1"), spaceBefore=2, spaceAfter=8))

    story.append(Paragraph(
        "<b>1.1 The Engineering Problem & Project Objectives:</b><br/>"
        "Off-the-shelf object detection models trained on standard benchmark datasets (such as COCO's 80 classes) present two fundamental "
        "engineering drawbacks when applied to practical, domain-specific visual monitoring: "
        "(1) They lack crucial everyday workplace and study objects (e.g. stationery like pens and pencils are completely absent from COCO), "
        "and (2) larger architectures (such as YOLOv8x or Faster R-CNN) incur massive inference latencies (>100ms on CPU) and bulky memory footprints, "
        "making them unviable for client-side web applications and real-time WebRTC browser streams. "
        "The objective of this project was to design, train, validate, and deploy a bespoke, high-efficiency vision system—<b>Scoutline Vision Studio</b>—"
        "capable of detecting 7 common workspace classes (<i>person, bottle, cellphone, laptop, chair, pen, pencil</i>) with sub-15ms latency, "
        "robust accuracy (78.5% mAP@50), and zero-buffer WebRTC streaming directly in the browser.",
        styles['DocBody']
    ))

    story.append(Paragraph(
        "<b>1.2 End-to-End System Architecture:</b><br/>"
        "The complete architecture spans four interconnected lifecycle stages: Data Engineering & Validation, Model Training & Optimization, "
        "Modular Inference Pipelines, and the Production Web Application.",
        styles['DocBody']
    ))

    arch_flow = [
        [Paragraph("Pipeline Stage", styles['TableHead']), Paragraph("Core Responsibilities & Components", styles['TableHead']), Paragraph("Key Technologies Used", styles['TableHead'])],
        [
            Paragraph("<b>Stage 1: Data Engineering</b>", styles['TableCellBold']),
            Paragraph("Multi-source dataset merging (26,756 images across 3 splits), bounding box coordinate validation in [0,1], label-image pair reconciliation, and class distribution reporting.", styles['TableCell']),
            Paragraph("Python, OS, validate_merged_dataset.py", styles['TableCell'])
        ],
        [
            Paragraph("<b>Stage 2: Model Training</b>", styles['TableCellBold']),
            Paragraph("Transfer learning using YOLOv8n initialized from COCO. Automatic Mixed Precision (FP16) on Tesla GPU, SGD with cosine momentum, Mosaic data augmentation, and early stopping.", styles['TableCell']),
            Paragraph("PyTorch, Ultralytics YOLOv8n, Kaggle GPU (T4/P100)", styles['TableCell'])
        ],
        [
            Paragraph("<b>Stage 3: Offline Inference</b>", styles['TableCellBold']),
            Paragraph("Modular CLI & GUI inference tools: image_detector.py (file picker & save), video_detector.py (frame iteration & aggregation), and webcam_detector.py (Windows DirectShow low-latency capture).", styles['TableCell']),
            Paragraph("OpenCV (cv2), Tkinter, NumPy", styles['TableCell'])
        ],
        [
            Paragraph("<b>Stage 4: Web Application</b>", styles['TableCellBold']),
            Paragraph("Scoutline Vision Studio: Cyber-Dark UI, 3 modes (Image Scan, Video Trace, Live Stream). PyAV H.264 browser encoding, 2x frame stride, and asynchronous WebRTC frame decoupling.", styles['TableCell']),
            Paragraph("Streamlit, streamlit-webrtc, PyAV (libx264), threading", styles['TableCell'])
        ],
    ]
    t_arch = Table(arch_flow, colWidths=[110, 312, 110])
    t_arch.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0F172A")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#FFFFFF"), colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_arch)
    story.append(Spacer(1, 10))

    # ==================================================================
    # SECTION 2: COMPUTER VISION & YOLOV8 THEORETICAL DEEP DIVE
    # ==================================================================
    story.append(Paragraph("2.0 Computer Vision & YOLO Theoretical Deep Dive", styles['DocHeading1']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E1"), spaceBefore=2, spaceAfter=8))

    story.append(Paragraph(
        "<b>2.1 Core Computer Vision Taxonomy:</b><br/>"
        "Understanding where object detection sits in the visual perception hierarchy is essential for interview defenses:<br/>"
        "• <b>Image Classification:</b> Predicts a single categorical label for the entire image (e.g., 'dog'). Answers <i>What is in this image?</i><br/>"
        "• <b>Object Localization:</b> Identifies the single primary object and regresses one bounding box coordinate (x, y, w, h).<br/>"
        "• <b>Object Detection:</b> Detects multiple objects of various classes simultaneously, outputting class labels and precise bounding boxes for every instance. Answers <i>What objects are where?</i><br/>"
        "• <b>Instance Segmentation:</b> Predicts pixel-level masks for every individual object instance (e.g. Mask R-CNN, YOLOv8-seg). More computationally demanding.",
        styles['DocBody']
    ))

    story.append(Paragraph(
        "<b>2.2 Architectural Evolution: Two-Stage vs. One-Stage Detectors:</b><br/>"
        "Prior to YOLO (You Only Look Once), state-of-the-art detectors were <b>Two-Stage Architectures</b> (R-CNN, Fast R-CNN, Faster R-CNN):<br/>"
        "1. <i>Stage 1 (Region Proposal):</i> A Region Proposal Network (RPN) slides over convolutional feature maps to generate ~2,000 candidate regions of interest (RoIs).<br/>"
        "2. <i>Stage 2 (Classification & Refinement):</i> RoI Pooling / RoI Align crops and normalizes feature patches, which are passed to fully connected layers for classification and bounding box regression.<br/>"
        "<b>The Trade-Off:</b> While Faster R-CNN achieves strong localization accuracy, its two sequential stages create an inherent computational bottleneck, "
        "limiting inference to 5-15 FPS. In contrast, <b>One-Stage Detectors (YOLO, SSD)</b> frame detection as a single unified regression problem: "
        "a single neural network processes the entire image in one forward pass, simultaneously predicting bounding box coordinates and class probabilities across a dense spatial grid. "
        "This delivers inference rates of 30-100+ FPS, enabling real-time video surveillance and streaming.",
        styles['DocBody']
    ))

    story.append(Paragraph(
        "<b>2.3 YOLOv8 Architectural Breakdown (Backbone, Neck, Head):</b><br/>"
        "YOLOv8 introduces several modern deep learning innovations over earlier iterations (YOLOv5/v7):",
        styles['DocBody']
    ))

    story.append(Paragraph(
        "<b>A. Backbone (Feature Extraction):</b> Built upon a modified <i>CSPDarknet53</i> network. Its core building block is the <b>C2f (Cross-Stage Partial with 2 Convolutions)</b> module. "
        "The C2f module enhances gradient flow by splitting the feature channels and combining multiple bottleneck outputs via residual connections. "
        "Compared to the older C3 module in YOLOv5, C2f is richer in gradient paths, captures multi-receptive field representations more effectively, "
        "and eliminates redundant parameters.<br/>"
        "At the deepest layer of the backbone sits the <b>SPPF (Spatial Pyramid Pooling - Fast)</b> block. SPPF routes feature maps through three sequential 5x5 max-pooling layers. "
        "Mathematically, cascading two 5x5 poolings is equivalent to a 9x9 receptive field, and cascading three is equivalent to a 13x13 receptive field. "
        "This pools multi-scale context without the quadratic computational cost of parallel large-kernel poolings.",
        styles['DocBody']
    ))

    story.append(Paragraph(
        "<b>B. Neck (Feature Fusion):</b> Utilizes a hybrid <b>PANet (Path Aggregation Network)</b> and <b>FPN (Feature Pyramid Network)</b> architecture. "
        "FPN conveys strong semantic information from top (deep) layers down to shallow layers, while PANet conveys precise spatial and localization cues "
        "from bottom (shallow) layers up to deep layers. This bi-directional feature fusion operates across three distinct feature map scales: "
        "<b>P3/8</b> (80x80 for small objects like pens/pencils), <b>P4/16</b> (40x40 for medium objects like bottles/cellphones), and <b>P5/32</b> (20x20 for large objects like persons/laptops/chairs).",
        styles['DocBody']
    ))

    story.append(Paragraph(
        "<b>C. Decoupled Anchor-Free Detection Head:</b><br/>"
        "Earlier YOLO versions used coupled heads where a single convolutional tensor predicted class probabilities, objectness scores, and bounding box coordinates together. "
        "However, classification and localization are inherently conflicting tasks: classification requires shift-invariant features, whereas localization requires shift-sensitive features. "
        "YOLOv8 introduces a <b>Decoupled Head</b> that splits features into two independent branches: one specialized for classification, and one specialized for bounding box regression.",
        styles['DocBody']
    ))

    story.append(make_callout(
        "CRUCIAL INTERVIEW CONCEPT: ANCHOR-BASED VS. ANCHOR-FREE DETECTION",
        "<b>Why did YOLOv8 abandon Anchor Boxes?</b><br/>"
        "In anchor-based models (YOLOv3/v4/v5), researchers pre-computed k-means clustering on training bounding boxes to define 3 anchor shapes per scale. "
        "This introduced severe limitations: (1) Anchors are sensitive hyperparameters that do not transfer well across datasets; (2) Matching ground truth boxes to anchors requires complex IoU thresholds; "
        "and (3) Slender or unusually proportioned objects (such as pens and pencils) suffer from poor anchor alignment. <br/>"
        "<b>YOLOv8 Anchor-Free Mechanism:</b> Instead of predicting offsets from predefined boxes, YOLOv8 treats each cell in the feature map as an anchor point and directly predicts the 4 distances "
        "(left, top, right, bottom) from the anchor point to the bounding box boundaries. This drastically reduces the number of candidate predictions, simplifies training assignment (via Task-Aligned Assigner), "
        "and improves generalization across varied aspect ratios.",
        styles,
        accent_color=colors.HexColor("#0284C7"),
        bg_color=colors.HexColor("#F0F9FF")
    ))

    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "<b>2.4 Mathematical Loss Formulations:</b><br/>"
        "YOLOv8 optimizes a composite loss function comprising classification loss, bounding box regression loss, and distribution focal loss:<br/>"
        "$$\\mathcal{L}_{total} = \\lambda_{cls} \\mathcal{L}_{cls} + \\lambda_{box} \\mathcal{L}_{CIoU} + \\lambda_{dfl} \\mathcal{L}_{DFL}$$",
        styles['DocBody']
    ))

    story.append(Paragraph(
        "<b>1. Classification Loss (Binary Cross-Entropy / BCE):</b><br/>"
        "Evaluates the multi-class prediction probability for each detected object using sigmoid cross-entropy. It handles multi-label scenarios gracefully.",
        styles['DocBody']
    ))

    story.append(Paragraph(
        "<b>2. Complete IoU Loss (CIoU):</b><br/>"
        "Standard IoU ($Intersection / Union$) suffers from zero gradients when bounding boxes do not overlap. CIoU resolves this by penalizing three geometric factors:<br/>"
        "• <b>Overlap Area:</b> $1 - IoU$<br/>"
        "• <b>Central Point Distance:</b> $\\frac{\\rho^2(b, b^{gt})}{c^2}$, where $\\rho$ is the Euclidean distance between box centroids and $c$ is the diagonal length of the smallest enclosing box.<br/>"
        "• <b>Aspect Ratio Consistency:</b> $\\alpha v$, where $v = \\frac{4}{\\pi^2} \\left(\\arctan\\frac{w^{gt}}{h^{gt}} - \\arctan\\frac{w}{h}\\right)^2$ and $\\alpha$ is a balancing parameter.<br/>"
        "This forces the predicted box to align in centroid, scale, and aspect ratio simultaneously.",
        styles['DocBody']
    ))

    story.append(Paragraph(
        "<b>3. Distribution Focal Loss (DFL):</b><br/>"
        "Real-world bounding box edges are often ambiguous, occluded, or blurry (e.g. the tip of a pencil or a chair leg against a dark carpet). "
        "Directly regressing a single integer coordinate assumes absolute certainty. DFL models the boundary coordinate $y$ as a continuous probability distribution "
        "over a discrete set of bins $[y_i, y_{i+1}]$. DFL forces the network to concentrate probabilities around values closest to the true label $y$:",
        styles['DocBody']
    ))
    story.append(Paragraph(
        "$$\\mathcal{L}_{DFL}(S_i, S_{i+1}) = -\\Big((y_{i+1} - y)\\log(S_i) + (y - y_i)\\log(S_{i+1})\\Big)$$",
        styles['DocBody']
    ))

    story.append(Paragraph(
        "<b>2.5 Non-Maximum Suppression (NMS) & Evaluation Metrics:</b><br/>"
        "Because dense anchor-free feature maps generate thousands of candidate bounding boxes per image, <b>Non-Maximum Suppression (NMS)</b> is applied as post-processing:<br/>"
        "1. Filter out all boxes with confidence score below threshold (e.g., $conf < 0.35$).<br/>"
        "2. Sort remaining boxes descending by confidence score.<br/>"
        "3. Select the highest-scoring box $B_{max}$, add it to the final detection list, and compute its Intersection-over-Union ($IoU$) against all remaining candidate boxes.<br/>"
        "4. Suppress (discard) any candidate box where $IoU(B_{max}, B_i) > iou\\_threshold$ (typically 0.70).<br/>"
        "5. Repeat iteratively until no candidates remain.<br/>"
        "<br/>"
        "<b>Key Evaluation Metrics:</b><br/>"
        "• <b>Precision:</b> $\\frac{TP}{TP + FP}$ — Out of all predicted objects, how many were correct?<br/>"
        "• <b>Recall:</b> $\\frac{TP}{TP + FN}$ — Out of all actual objects in the scene, how many did the model detect?<br/>"
        "• <b>mAP@50 (Mean Average Precision at IoU=0.50):</b> The area under the Precision-Recall curve averaged across all classes when IoU threshold is fixed at 0.50.<br/>"
        "• <b>mAP@50-95:</b> The primary COCO metric, calculated by averaging mAP across 10 IoU thresholds from 0.50 to 0.95 with a step of 0.05. It rewards millimeter-precise localization.",
        styles['DocBody']
    ))

    story.append(Spacer(1, 10))

    # ==================================================================
    # SECTION 3: DATASET ENGINEERING, CLEANSING & VALIDATION
    # ==================================================================
    story.append(Paragraph("3.0 Dataset Engineering, Cleansing & Validation", styles['DocHeading1']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E1"), spaceBefore=2, spaceAfter=8))

    story.append(Paragraph(
        "<b>3.1 Dataset Scale & Class Breakdown:</b><br/>"
        "The project utilizes a massive multi-source curated dataset totaling <b>26,756 images</b> partitioned strictly across three canonical splits:",
        styles['DocBody']
    ))

    split_table_data = [
        [Paragraph("Dataset Partition", styles['TableHead']), Paragraph("Image Count", styles['TableHead']), Paragraph("Percentage", styles['TableHead']), Paragraph("Primary Purpose", styles['TableHead'])],
        [Paragraph("Train Set", styles['TableCellBold']), Paragraph("20,092 images", styles['TableCell']), Paragraph("75.1%", styles['TableCell']), Paragraph("Gradient updates via backpropagation with Mosaic & RandAugment", styles['TableCell'])],
        [Paragraph("Validation Set", styles['TableCellBold']), Paragraph("4,413 images", styles['TableCell']), Paragraph("16.5%", styles['TableCell']), Paragraph("Hyperparameter tuning, early stopping checkpoints, mAP evaluation", styles['TableCell'])],
        [Paragraph("Test Set", styles['TableCellBold']), Paragraph("2,251 images", styles['TableCell']), Paragraph("8.4%", styles['TableCell']), Paragraph("Unbiased out-of-sample final benchmarking and generalization checks", styles['TableCell'])],
        [Paragraph("Total Dataset", styles['TableCellBold']), Paragraph("26,756 images", styles['TableCell']), Paragraph("100.0%", styles['TableCell']), Paragraph("Full 7-class workspace & study object detection corpus", styles['TableCell'])],
    ]
    t_split = Table(split_table_data, colWidths=[110, 100, 80, 242])
    t_split.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0F172A")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#FFFFFF"), colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_split)
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        "<b>The 7 Target Classes:</b><br/>"
        "<code>0: person, 1: bottle, 2: cellphone, 3: laptop, 4: chair, 5: pen, 6: pencil</code><br/>"
        "<i>Engineering Nuance:</i> Pens and pencils represent slender, low-pixel-density objects. In standard datasets, they suffer from high miss rates. "
        "In our training pipeline, high-resolution feature maps (P3/8) coupled with Mosaic data augmentation ensured that the network learned robust "
        "edge gradients even when stationery was partially obscured by hands or laptops.",
        styles['DocBody']
    ))

    story.append(Paragraph(
        "<b>3.2 YOLO Annotation Format:</b><br/>"
        "Every label file is a <code>.txt</code> file matching its corresponding image basename. Each line represents one object using 5 normalized floating-point values:<br/>"
        "<code>&lt;class_id&gt; &lt;x_center&gt; &lt;y_center&gt; &lt;width&gt; &lt;height&gt;</code><br/>"
        "All spatial coordinates are normalized to the range $[0.0, 1.0]$ relative to image width $W$ and height $H$:<br/>"
        "$$x_{center} = \\frac{X_{center}}{W}, \\quad y_{center} = \\frac{Y_{center}}{H}, \\quad w = \\frac{BoxWidth}{W}, \\quad h = \\frac{BoxHeight}{H}$$",
        styles['DocBody']
    ))

    story.append(Paragraph(
        "<b>3.3 Line-by-Line Code Walkthrough: <code>scripts/validate_merged_dataset.py</code>:</b><br/>"
        "Before investing GPU hours into training, automated verification of data integrity is essential. "
        "The script <code>validate_merged_dataset.py</code> performs systematic sanity checks across all 26k+ images:",
        styles['DocBody']
    ))

    val_script_explanation = """# 1. Traverses train, valid, and test directories
img_files = {os.path.splitext(f)[0]: f for f in os.listdir(img_dir)}
lbl_files = {os.path.splitext(f)[0]: f for f in os.listdir(lbl_dir) if f.endswith('.txt')}

# 2. Reconciles orphaned files via fast Set operations:
images_without_labels = set(img_files) - set(lbl_files)  # Unlabeled images
labels_without_images = set(lbl_files) - set(img_files)  # Missing image files

# 3. Validates each text annotation line:
for line in lines:
    parts = line.split()
    if len(parts) != 5:  # Catches malformed lines
        issues.append(f'Malformed line: expected 5 values')
    cls_id = int(parts[0])
    if cls_id < 0 or cls_id >= NUM_CLASSES:  # Verifies class_id in [0, 6]
        issues.append(f'Invalid class id: {cls_id}')
    coords = [float(p) for p in parts[1:]]
    if any(c < 0.0 or c > 1.0 for c in coords):  # Bounds check coordinates
        issues.append(f'Coordinate out of [0, 1] range: {coords}')"""

    story.append(make_code_box("Dataset Integrity Validator (scripts/validate_merged_dataset.py)", val_script_explanation, styles))

    story.append(Paragraph(
        "<b>3.4 Data Augmentation Strategies Applied:</b><br/>"
        "• <b>Mosaic Augmentation (mosaic=1.0):</b> Stitches 4 training images into one at random crop scales. Forces the network to learn objects in varied spatial locations, reduces batch normalization reliance, and exposes small objects.<br/>"
        "• <b>Horizontal Flip (fliplr=0.5):</b> 50% probability of left-right reflection to ensure viewpoint invariance.<br/>"
        "• <b>HSV Color Jitter (hsv_h=0.015, hsv_s=0.7, hsv_v=0.4):</b> Random perturbations of Hue, Saturation, and Value to make the model invariant to lighting conditions (e.g., dark study rooms vs brightly lit offices).<br/>"
        "• <b>Random Erasing (erasing=0.4):</b> Randomly blacks out rectangular image patches (40% probability) to simulate physical occlusion (e.g., a person holding a phone or a bottle behind a laptop).<br/>"
        "• <b>Scale & Translation (scale=0.5, translate=0.1):</b> Affine transformations simulating camera distance and viewpoint shifts.",
        styles['DocBody']
    ))

    story.append(Spacer(1, 10))

    # ==================================================================
    # SECTION 4: MODEL TRAINING, KAGGLE GPU ACCELERATION & METRICS
    # ==================================================================
    story.append(Paragraph("4.0 Model Training, Kaggle GPU Acceleration & Metrics", styles['DocHeading1']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E1"), spaceBefore=2, spaceAfter=8))

    story.append(Paragraph(
        "<b>4.1 Compute Setup & Transfer Learning Strategy:</b><br/>"
        "Training was executed on a <b>Kaggle GPU environment equipped with an NVIDIA Tesla T4/P100 (16GB VRAM)</b>. "
        "Rather than training from scratch (which would require hundreds of thousands of images to learn basic low-level edge and texture filters), "
        "we employed <b>Transfer Learning</b> by initializing network weights from the official <code>yolov8n.pt</code> checkpoint pre-trained on Microsoft COCO. "
        "Pre-trained weights were fine-tuned across all 130 layers using gradient updates tailored to our 7 workspace classes.",
        styles['DocBody']
    ))

    story.append(Paragraph(
        "<b>4.2 Hyperparameter Configuration Table:</b>",
        styles['DocBody']
    ))

    hyper_data = [
        [Paragraph("Hyperparameter", styles['TableHead']), Paragraph("Configured Value", styles['TableHead']), Paragraph("Engineering Rationale", styles['TableHead'])],
        [Paragraph("Input Resolution (imgsz)", styles['TableCellBold']), Paragraph("640 x 640 pixels", styles['TableCell']), Paragraph("Standard YOLO resolution providing optimal trade-off between small-object resolution and compute throughput.", styles['TableCell'])],
        [Paragraph("Batch Size", styles['TableCellBold']), Paragraph("16", styles['TableCell']), Paragraph("Maximized GPU memory utilization without overflowing 16GB VRAM under Mosaic caching.", styles['TableCell'])],
        [Paragraph("Optimizer", styles['TableCellBold']), Paragraph("SGD with Momentum (0.937)", styles['TableCell']), Paragraph("Provides superior generalization on vision tasks compared to AdamW, with weight decay=0.0005.", styles['TableCell'])],
        [Paragraph("Learning Rate Schedule", styles['TableCellBold']), Paragraph("lr0=0.01, lrf=0.01, warmup=3.0 eps", styles['TableCell']), Paragraph("Linear warmup for 3 epochs followed by cosine decay avoids gradient instability in early training.", styles['TableCell'])],
        [Paragraph("Mixed Precision (AMP)", styles['TableCellBold']), Paragraph("Enabled (FP16)", styles['TableCell']), Paragraph("Cuts memory bandwidth by 50% and leverages Tensor Cores for 2x faster execution.", styles['TableCell'])],
        [Paragraph("Loss Weighting", styles['TableCellBold']), Paragraph("box=7.5, cls=0.5, dfl=1.5", styles['TableCell']), Paragraph("High box loss weight emphasizes tight bounding box boundary localization.", styles['TableCell'])],
    ]
    t_hyper = Table(hyper_data, colWidths=[120, 110, 302])
    t_hyper.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0F172A")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#FFFFFF"), colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_hyper)
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        "<b>4.3 Quantitative Validation Results & Model Checkpoint Analysis:</b><br/>"
        "Inspection of the trained checkpoint (<code>model/best.pt</code>) reveals exceptional performance metrics across the validation dataset:",
        styles['DocBody']
    ))

    metric_cards = [
        [
            Paragraph("<b>mAP@50</b><br/><font size=14 color='#DC2626'><b>78.5%</b></font><br/><font size=7 color='#64748B'>Mean Average Precision at IoU=0.50</font>", styles['TableCell']),
            Paragraph("<b>Precision</b><br/><font size=14 color='#0284C7'><b>81.9%</b></font><br/><font size=7 color='#64748B'>True Positives / (TP + FP)</font>", styles['TableCell']),
            Paragraph("<b>Recall</b><br/><font size=14 color='#10B981'><b>71.5%</b></font><br/><font size=7 color='#64748B'>True Positives / (TP + FN)</font>", styles['TableCell']),
            Paragraph("<b>mAP@50-95</b><br/><font size=14 color='#8B5CF6'><b>49.8%</b></font><br/><font size=7 color='#64748B'>Strict multi-threshold COCO metric</font>", styles['TableCell']),
        ]
    ]
    t_metrics = Table(metric_cards, colWidths=[133, 133, 133, 133])
    t_metrics.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_metrics)
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        "<b>Loss Convergence Summary:</b><br/>"
        "• <b>Validation Box Loss:</b> Converged to <b>1.1325</b> (demonstrating sharp bounding box alignment).<br/>"
        "• <b>Validation Class Loss:</b> Converged to <b>0.9680</b> (demonstrating distinct decision boundaries between classes).<br/>"
        "• <b>Validation DFL Loss:</b> Converged to <b>1.4045</b> (demonstrating high boundary confidence on occluded edges).<br/>"
        "<br/>"
        "<b>4.4 Architectural Selection: Why YOLOv8n (Nano) Over Small/Medium?</b><br/>"
        "In production system design, bigger is not always better. While YOLOv8m achieves slightly higher mAP, it demands 78.9 GFLOPs and 25.9M parameters, "
        "causing CPU inference to drop to 8-12 FPS and triggering browser buffer bloat in WebRTC video calls. "
        "<b>YOLOv8n delivers 78.5% mAP@50 with only 3.01M parameters and 8.2 GFLOPs</b>, achieving 45+ FPS on GPU and sub-15ms CPU inference. "
        "This makes it the optimal engineering choice for real-time edge, laptop, and browser deployments.",
        styles['DocBody']
    ))

    story.append(Spacer(1, 10))

    # ==================================================================
    # SECTION 5: DESKTOP & OFFLINE INFERENCE PIPELINES
    # ==================================================================
    story.append(Paragraph("5.0 Desktop & Offline Inference Pipelines (Code Walkthroughs)", styles['DocHeading1']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E1"), spaceBefore=2, spaceAfter=8))

    story.append(Paragraph(
        "The repository contains three modular standalone inference engines in the <code>inference/</code> directory, "
        "designed for batch processing, automated testing, and desktop camera monitoring without requiring the Streamlit web server.",
        styles['DocBody']
    ))

    # 5.1 Image detector
    story.append(Paragraph("<b>5.1 Single Image Detection Engine (<code>inference/image_detector.py</code>):</b>", styles['DocHeading2']))
    story.append(Paragraph(
        "This script enables both command-line arguments and an automatic Tkinter GUI file picker fallback if no image path is passed. "
        "It dynamically locates the trained weights across project subfolders via <code>resolve_model_path()</code>.",
        styles['DocBody']
    ))

    img_code = """def resolve_model_path(path=MODEL_PATH):
    # Searches relative to current working dir, parent dir, or streamlit subfolder
    candidates = [path, os.path.join(os.path.dirname(__file__), "..", path)]
    for c in candidates:
        if os.path.exists(c): return os.path.abspath(c)
    return path

def detect_image(image_path, output_dir="outputs/images"):
    os.makedirs(output_dir, exist_ok=True)
    model = YOLO(resolve_model_path())  # Load model onto CPU/GPU
    results = model.predict(source=image_path, conf=0.35, verbose=False)
    result = results[0]
    annotated = result.plot()           # Draws boxes and label tags
    output_path = os.path.join(output_dir, f"{base_name}_detected.jpg")
    cv2.imwrite(output_path, annotated) # Persists to disk"""
    story.append(make_code_box("Image Detection Engine (inference/image_detector.py)", img_code, styles))

    # 5.2 Video detector
    story.append(Paragraph("<b>5.2 Video File Batch Detector (<code>inference/video_detector.py</code>):</b>", styles['DocHeading2']))
    story.append(Paragraph(
        "Processes pre-recorded video files (MP4, AVI, MOV) frame-by-frame, writing annotated video streams to disk and aggregating "
        "total detection frequencies across all frames.",
        styles['DocBody']
    ))

    vid_code = """cap = cv2.VideoCapture(video_path)
fps = cap.get(cv2.CAP_PROP_FPS) or 25
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

fourcc = cv2.VideoWriter_fourcc(*"mp4v")
writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

while True:
    ret, frame = cap.read()
    if not ret: break
    results = model.predict(source=frame, conf=0.35, verbose=False)
    annotated = results[0].plot()
    writer.write(annotated)            # Sequential frame writing
    frame_idx += 1
cap.release()
writer.release()                       # Flushes remaining packets"""
    story.append(make_code_box("Video File Processor (inference/video_detector.py)", vid_code, styles))

    # 5.3 Webcam detector
    story.append(Paragraph("<b>5.3 Real-Time Desktop Webcam Monitor (<code>inference/webcam_detector.py</code>):</b>", styles['DocHeading2']))
    story.append(Paragraph(
        "Launches a local OpenCV GUI window for live camera detection. It incorporates two vital engineering details: "
        "(1) <code>cv2.CAP_DSHOW</code> (DirectShow API) to bypass Windows camera initialization latency, and "
        "(2) an Exponential Moving Average (EMA) smoothed FPS counter for jitter-free telemetry.",
        styles['DocBody']
    ))

    cam_code = """# DirectShow backend eliminates slow webcam startup on Windows:
cap = cv2.VideoCapture(CAM_INDEX, cv2.CAP_DSHOW)
prev_time = time.time()
fps_smoothed = 0.0

while True:
    ret, frame = cap.read()
    if not ret: break
    results = model.predict(source=frame, conf=0.35, verbose=False)
    annotated = results[0].plot()
    
    # Exponential Moving Average (EMA) FPS calculation:
    curr_time = time.time()
    instant_fps = 1.0 / max(curr_time - prev_time, 1e-6)
    fps_smoothed = 0.9 * fps_smoothed + 0.1 * instant_fps
    prev_time = curr_time
    
    cv2.putText(annotated, f"FPS: {fps_smoothed:.1f}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    cv2.imshow("Webcam Detector", annotated)
    if cv2.waitKey(1) & 0xFF == ord('q'): break"""
    story.append(make_code_box("Live Webcam Engine (inference/webcam_detector.py)", cam_code, styles))

    story.append(Spacer(1, 10))

    # ==================================================================
    # SECTION 6: PRODUCTION WEB APPLICATION: SCOUTLINE VISION STUDIO
    # ==================================================================
    story.append(Paragraph("6.0 Production Web Application: Scoutline Vision Studio", styles['DocHeading1']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E1"), spaceBefore=2, spaceAfter=8))

    story.append(Paragraph(
        "<b>6.1 Architecture & Design System Overview (<code>streamlit-app/app.py</code>):</b><br/>"
        "<b>Scoutline Vision Studio</b> is the production web interface designed with a tailored <b>Cyber-Dark</b> aesthetic, "
        "featuring glassmorphic cards, glowing telemetry pills, universal high-contrast red action buttons (<code>#EF4444</code>), "
        "and strict 480px single-frame media constraints to eliminate disorienting vertical scrollbars on dashboards. "
        "The application operates in three specialized modes: <b>Image Scan</b>, <b>Video Trace</b>, and <b>Live Stream</b>.",
        styles['DocBody']
    ))

    story.append(Paragraph(
        "<b>6.2 Model Caching & Hardware Warm-Up:</b><br/>"
        "In production web applications, reloading a PyTorch model on every user interaction is fatal to performance. "
        "The engine utilizes Streamlit's resource cache and executes a warm-up inference pass during initialization:",
        styles['DocBody']
    ))

    cache_code = """@st.cache_resource(show_spinner=False)
def load_vision_engine():
    m1_path = resolve_path(os.path.join("model", "best.pt"))
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model1 = YOLO(m1_path) if m1_path else None
    if model1:
        # Warm up engine: initializes CUDA memory pools and graph caches
        dummy = np.zeros((320, 320, 3), dtype=np.uint8)
        model1.predict(dummy, imgsz=320, device=device, verbose=False)
    return model1, device"""
    story.append(make_code_box("Resource Caching & Warm-Up (streamlit-app/app.py)", cache_code, styles))

    story.append(Paragraph(
        "<b>6.3 Mode 1: Image Scan (Instant Photo Telemetry):</b><br/>"
        "Allows users to upload photos (JPG, PNG, WebP). The system runs YOLO inference at 512px resolution, records precise latency in milliseconds, "
        "renders custom chamfered cyber-accented bounding boxes, populates a left-hand 'Detected Items' count panel, and offers direct JPEG download.",
        styles['DocBody']
    ))

    story.append(Paragraph(
        "<b>6.4 Mode 2: Video Trace (High-Speed Browser-Native H.264 Engine):</b><br/>"
        "A common pitfall in web-based computer vision is writing video using OpenCV's default <code>mp4v</code> codec. "
        "Browsers (Chrome, Edge, Safari) cannot decode raw <code>mp4v</code> video elements natively, resulting in blank players. "
        "Our engine solves this using <b>PyAV</b> to encode video into strict <b>H.264 (libx264)</b> with <code>yuv420p</code> pixel format, "
        "<code>crf=23</code>, and <code>preset=veryfast</code>. <br/>"
        "Furthermore, to achieve a 2x processing speedup, it employs <b>Balanced Frame Striding (stride=2)</b>: "
        "heavy neural network inference runs on every 2nd frame, carrying cached detection coordinates over to intermediate frames. "
        "Temporary video files are automatically unlinked upon session completion to prevent disk exhaustion.",
        styles['DocBody']
    ))

    pyav_code = """# Native H.264 stream muxing via PyAV:
container = av.open(out_path, mode="w")
stream = container.add_stream("libx264", rate=int(round(fps)))
stream.width, stream.height = width, height
stream.pix_fmt = "yuv420p"
stream.options = {"crf": "23", "preset": "veryfast"}

while True:
    ret, frame = cap.read()
    if not ret: break
    # 2x Balanced Frame Stride:
    if frame_idx % VIDEO_FRAME_STRIDE == 0:
        cached_boxes = detect_raw_boxes(frame, conf_thresh=0.35, imgsz=480)
    annotated = render_styled_annotations(frame, cached_boxes)
    av_frame = av.VideoFrame.from_ndarray(annotated, format="bgr24")
    for packet in stream.encode(av_frame):
        container.mux(packet)
    frame_idx += 1"""
    story.append(make_code_box("PyAV H.264 Streaming with Frame Striding (streamlit-app/app.py)", pyav_code, styles))

    story.append(Paragraph(
        "<b>6.5 Mode 3: Live Stream & Asynchronous WebRTC Decoupling (The Core Engineering Breakthrough):</b>",
        styles['DocHeading2']
    ))

    story.append(make_callout(
        "HIGH-STAKES INTERVIEW TOPIC: SOLVING THE WEBRTC 60-SECOND CRASH",
        "<b>The Vulnerability in Synchronous Video Processing:</b><br/>"
        "In naive WebRTC implementations, developers invoke <code>model.predict()</code> synchronously inside the WebRTC frame callback: "
        "<code>def recv(self, frame): ... out = model.predict(frame) ... return out</code>.<br/>"
        "Because YOLO inference takes 25-40ms on CPU, the callback takes longer than the camera's frame arrival interval (33ms for 30 FPS). "
        "Unprocessed video packets accumulate inside the <code>aiortc</code> internal queue. "
        "This queue bloat causes exponential memory growth, progressive display latency (video lags 5-10 seconds behind reality), and inevitably "
        "triggers an unhandled timeout crash after exactly 60 seconds of streaming.<br/>"
        "<br/>"
        "<b>The Architectural Fix: <code>AsyncHDLiveStreamProcessor</code>:</b><br/>"
        "1. <b>Decoupled Threading:</b> The main WebRTC pipeline runs entirely unblocked at 30 FPS. It reads the camera frame, attaches the most recently "
        "cached bounding boxes, and immediately returns the annotated frame to the browser with zero queue delay.<br/>"
        "2. <b>Producer-Consumer Background Worker:</b> A dedicated background daemon thread waits on a <code>threading.Event()</code>. When a new frame arrives, "
        "it copies the frame under a mutex <code>threading.Lock()</code>, downscales it to 480px width, and runs inference asynchronously.<br/>"
        "3. <b>Coordinate Re-Scaling:</b> Once inference finishes, the worker scales bounding box coordinates back to full HD dimensions (e.g. 1280x720) "
        "and updates the shared cached detections.<br/>"
        "<b>Result:</b> Silky smooth 30 FPS video feed, crisp 720p/1080p resolution, sub-30ms detection refresh rate, and infinite continuous runtime with zero memory bloat.",
        styles,
        accent_color=colors.HexColor("#DC2626"),
        bg_color=colors.HexColor("#FEF2F2")
    ))

    webrtc_code = """class AsyncHDLiveStreamProcessor(VideoProcessorBase):
    def __init__(self):
        self.lock = threading.Lock()
        self.latest_frame = None
        self.cached_detections = []
        self.new_frame_event = threading.Event()
        self.worker_thread = threading.Thread(target=self._inference_worker, daemon=True)
        self.worker_thread.start()

    def _inference_worker(self):
        while self.is_running:
            self.new_frame_event.wait(timeout=0.1)
            with self.lock:
                full_frame = self.latest_frame.copy() if self.latest_frame is not None else None
                self.latest_frame = None
                self.new_frame_event.clear()
            if full_frame is None: continue
            
            # Downsample for fast CPU inference (480px width)
            small = cv2.resize(full_frame, (480, target_h))
            raw_dets = detect_raw_boxes(small, imgsz=384)
            
            # Scale coordinates accurately back to full HD resolution
            scaled = scale_boxes_back_to_hd(raw_dets, scale_x, scale_y)
            with self.lock:
                self.cached_detections = scaled

    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        img_bgr = frame.to_ndarray(format="bgr24")
        with self.lock:
            self.latest_frame = img_bgr
            self.new_frame_event.set()        # Signals background worker
            current_dets = list(self.cached_detections)
        # Immediately returns unblocked annotated frame to browser
        annotated = render_styled_annotations(img_bgr, current_dets)
        return av.VideoFrame.from_ndarray(annotated, format="bgr24")"""
    story.append(make_code_box("Asynchronous WebRTC Decoupled Processor (streamlit-app/app.py)", webrtc_code, styles))

    story.append(Spacer(1, 10))

    # ==================================================================
    # SECTION 7: MASTER TECHNICAL INTERVIEW Q&A PLAYBOOK (40+ QUESTIONS)
    # ==================================================================
    story.append(Paragraph("7.0 Master Technical Interview Q&A Playbook (40+ Questions)", styles['DocHeading1']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E1"), spaceBefore=2, spaceAfter=8))

    story.append(Paragraph(
        "This section compiles <b>over 40 rigorous technical questions</b> organized across 5 core competency domains. "
        "Mastering these explanations equips you to lead technical conversations and defend every design decision made in this project.",
        styles['DocBody']
    ))

    # DOMAIN 1: COMPUTER VISION & YOLO ARCHITECTURE
    story.append(Paragraph("Domain 1: Computer Vision & YOLO Architecture (Questions 1 – 10)", styles['DocHeading2']))

    q1 = ("What is the primary architectural difference between YOLOv8 and earlier versions like YOLOv5?",
          "YOLOv8 introduces two major paradigm shifts: (1) It is completely anchor-free, replacing anchor box priors with anchor points and direct distance regression, which eliminates anchor hyperparameter tuning and accelerates positive sample matching via the Task-Aligned Assigner. (2) It adopts a decoupled head that separates the classification branch from the bounding box regression branch, eliminating the gradient conflict inherent in coupled heads. Additionally, YOLOv8 replaces C3 modules with C2f modules for richer gradient flow.",
          "Highlight anchor-free design and the decoupled head. Mention task-aligned assigner.")
    story.append(make_qa_card(1, q1[0], q1[1], q1[2], styles))

    q2 = ("Why does YOLOv8 use C2f modules instead of standard convolutional layers or C3?",
          "Standard convolutions pass feature maps through sequential linear operations, which can lead to vanishing gradients in deep networks. The older C3 module in YOLOv5 used three convolutions with cross-stage partial connections. YOLOv8's C2f (Cross-Stage Partial with 2 Convolutions) module splits feature channels and routes them through multiple residual bottlenecks, concatenating intermediate outputs. This provides more diverse gradient paths, enhances multi-scale feature reuse, and reduces parameter count without losing representational capacity.",
          "Use the phrase 'richer gradient flow and enhanced feature reuse'.")
    story.append(make_qa_card(2, q2[0], q2[1], q2[2], styles))

    q3 = ("What is SPPF and why is it located at the end of the backbone?",
          "SPPF (Spatial Pyramid Pooling - Fast) aggregates multi-scale contextual features from the deepest feature maps (P5). Instead of running parallel poolings with large kernels (which is computationally expensive), SPPF connects three 5x5 max-pooling layers in series. Mathematically, cascading two 5x5 poolings yields an effective 9x9 receptive field, and three yields a 13x13 receptive field. It expands the receptive field to capture global image context without increasing latency.",
          "Emphasize that serial 5x5 pooling mathematically mirrors 9x9 and 13x13 receptive fields at far lower latency.")
    story.append(make_qa_card(3, q3[0], q3[1], q3[2], styles))

    q4 = ("Explain how Complete IoU (CIoU) Loss works and why standard IoU or GIoU wasn't enough.",
          "Standard IoU equals 0 whenever two bounding boxes do not overlap, providing zero gradient for backpropagation. Generalized IoU (GIoU) introduced a penalty for the empty space in the smallest enclosing box, but struggles when one box is completely inside another. CIoU solves this by optimizing three independent geometric metrics: (1) Overlapping area (1 - IoU), (2) Normalized Euclidean distance between box centroids, and (3) Aspect ratio consistency. This forces predictions to converge faster and align tightly.",
          "State the 3 geometric factors: overlap area, centroid distance, and aspect ratio.")
    story.append(make_qa_card(4, q4[0], q4[1], q4[2], styles))

    q5 = ("What is Distribution Focal Loss (DFL) and why is it beneficial for objects like pens and pencils?",
          "Traditional bounding box regression treats coordinates as Dirac delta functions (single fixed numbers). However, in real images, boundaries are often blurry or occluded (e.g., the tip of a pencil or a pen cap blended into a desk). DFL models the boundary coordinate as a continuous probability distribution over an integral set of bins. It forces the network to concentrate high probabilities on values close to the ground truth. This significantly improves localization accuracy for slender, low-contrast items.",
          "Explain that DFL models coordinates as probability distributions rather than rigid numbers.")
    story.append(make_qa_card(5, q5[0], q5[1], q5[2], styles))

    q6 = ("How does Non-Maximum Suppression (NMS) work step-by-step?",
          "1. Filter out candidate boxes whose confidence score is below the threshold (e.g. 0.35). 2. Sort remaining candidate boxes in descending order of score. 3. Select the top box B_max and append it to final detections. 4. Calculate IoU between B_max and all other candidates. 5. Discard any candidate with IoU > 0.70 (suppressing redundant overlapping detections of the same physical object). 6. Repeat until the candidate pool is exhausted.",
          "Be ready to write this pseudocode on a whiteboard.")
    story.append(make_qa_card(6, q6[0], q6[1], q6[2], styles))

    q7 = ("What is the difference between mAP@50 and mAP@50-95?",
          "mAP@50 calculates Mean Average Precision when a prediction is counted as a True Positive if IoU >= 0.50. It measures general detection ability. mAP@50-95 (the COCO standard) averages mAP across 10 distinct IoU thresholds from 0.50 to 0.95 with step 0.05. It heavily penalizes sloppy bounding boxes and rewards tight, pixel-accurate localization. Our model achieved 78.5% on mAP@50 and 49.8% on mAP@50-95.",
          "Know both numbers by heart: 78.5% and 49.8%.")
    story.append(make_qa_card(7, q7[0], q7[1], q7[2], styles))

    q8 = ("How does the Task-Aligned Assigner work in YOLOv8?",
          "In anchor-free detection, the model must decide which anchor points are positive samples during training. YOLOv8 uses the Task-Aligned Assigner (TAL), which computes an alignment metric: t = (s^alpha) * (u^beta), where s is classification score and u is IoU between prediction and ground truth. Anchors with the highest alignment scores are assigned as positive samples. This ensures that points with both high classification confidence and accurate localization are reinforced simultaneously.",
          "Show that you understand that classification and localization are co-optimized.")
    story.append(make_qa_card(8, q8[0], q8[1], q8[2], styles))

    q9 = ("Why is YOLO faster than two-stage detectors like Faster R-CNN?",
          "Faster R-CNN requires two sequential stages: first running a Region Proposal Network to propose ~2,000 regions of interest, and second cropping features (RoI Pooling/Align) and passing them through secondary FC layers for classification. YOLO is single-stage: the entire image is processed in a single forward pass through a fully convolutional network that simultaneously outputs spatial coordinates and class probabilities across dense feature grids, achieving 30-100+ FPS.",
          "Contrast the sequential RPN + RoI Align pipeline with YOLO's single forward pass.")
    story.append(make_qa_card(9, q9[0], q9[1], q9[2], styles))

    q10 = ("How does Feature Pyramid Network (FPN) combined with Path Aggregation Network (PANet) work in the neck?",
           "FPN provides top-down connections that transfer high-level semantic context from deep layers (P5) to shallow layers (P3). PANet adds bottom-up connections that transfer precise low-level localization cues from shallow layers back up to deep layers. This bi-directional fusion ensures that small objects (detected at P3) have semantic context, and large objects (detected at P5) retain sharp spatial boundaries.",
           "Describe it as 'bi-directional feature fusion' balancing semantics and spatial resolution.")
    story.append(make_qa_card(10, q10[0], q10[1], q10[2], styles))

    # DOMAIN 2: DATASET & TRAINING
    story.append(Paragraph("Domain 2: Dataset Engineering & Training Pipeline (Questions 11 – 20)", styles['DocHeading2']))

    q11 = ("Why did you choose 7 specific classes instead of using standard COCO pre-trained classes?",
           "COCO's 80 classes include esoteric categories (e.g. zebra, giraffe, fire hydrant) but completely lack essential office and study tools like pens and pencils. Furthermore, running an 80-class output layer incurs unnecessary softmax/sigmoid computation and memory overhead. By training a bespoke 7-class model, we tailored the detector to workplace/classroom environments and optimized inference speed and accuracy for target objects.",
           "Emphasize real-world domain alignment and compute efficiency.")
    story.append(make_qa_card(11, q11[0], q11[1], q11[2], styles))

    q12 = ("How did you detect and handle orphaned label files or malformed bounding box coordinates?",
           "We developed `scripts/validate_merged_dataset.py`. It uses fast Python set operations: `set(images) - set(labels)` detects unlabeled images, and `set(labels) - set(images)` catches missing image files. For coordinate integrity, it verifies each line has exactly 5 tokens, confirms class_id is in [0, 6], and validates that normalized coordinates (x, y, w, h) lie strictly within [0.0, 1.0]. Any out-of-bound boxes were logged and purged before training.",
           "Demonstrates rigorous software engineering and data hygiene.")
    story.append(make_qa_card(12, q12[0], q12[1], q12[2], styles))

    q13 = ("What is Mosaic data augmentation and why is it critical for object detection?",
           "Mosaic stitches 4 training images into one composite image at random scale and crop positions. It provides three benefits: (1) It introduces varied spatial context, forcing the network to recognize objects outside standard positions; (2) It artificially shrinks object scale, drastically increasing small object exposure (crucial for pens/pencils); and (3) It allows batch normalization to calculate statistics across 4x more scenes per batch.",
           "Mention small object exposure and batch normalization efficiency.")
    story.append(make_qa_card(13, q13[0], q13[1], q13[2], styles))

    q14 = ("Why is Automatic Mixed Precision (AMP) enabled during training?",
           "AMP automatically casts activations and operations to half-precision FP16 where numerically safe, while keeping master weights and loss scaling in FP32. This halves GPU memory bandwidth, fits larger batch sizes into VRAM, and accelerates forward and backward passes by ~2x on NVIDIA Tensor Cores with zero loss in final model accuracy.",
           "Mention Tensor Cores, FP16 speed, and FP32 numerical stability.")
    story.append(make_qa_card(14, q14[0], q14[1], q14[2], styles))

    q15 = ("Why did you use SGD with momentum instead of AdamW?",
           "While AdamW converges faster in early epochs, empirical computer vision research consistently demonstrates that Stochastic Gradient Descent with Nesterov momentum (0.937) finds flatter, more generalizable local minima for object detection tasks. Coupled with weight decay (0.0005) and a 3-epoch warmup, SGD achieves superior test-set mAP and reduces overfitting.",
           "Explain that SGD finds 'flatter minima' that generalize better on vision tasks.")
    story.append(make_qa_card(15, q15[0], q15[1], q15[2], styles))

    q16 = ("How did you address the small object detection problem for pens and pencils?",
           "Small objects suffer because after several stride-2 convolutions, a 16x16 pixel pen shrinks to less than 1 pixel at deep feature maps. We solved this by: (1) Retaining the high-resolution P3/8 feature map (80x80) in the PANet neck; (2) Using Mosaic augmentation to scale down objects during training; and (3) Utilizing Distribution Focal Loss (DFL) to handle soft, ambiguous boundary transitions.",
           "Highlight the P3/8 head, Mosaic scaling, and DFL.")
    story.append(make_qa_card(16, q16[0], q16[1], q16[2], styles))

    q17 = ("How was your dataset partitioned and why was validation kept strictly separate from test?",
           "The 26,756 images were partitioned into 20,092 Train (75.1%), 4,413 Validation (16.5%), and 2,251 Test (8.4%). The validation set was used during training for early stopping checkpoints and hyperparameter evaluation. The test set was kept strictly untouched until final evaluation to prevent data leakage and provide an unbiased measure of true real-world generalization.",
           "Emphasize preventing data leakage between validation and test splits.")
    story.append(make_qa_card(17, q17[0], q17[1], q17[2], styles))

    q18 = ("What is early stopping and how was it configured?",
           "Early stopping halts training when validation loss stops improving for a specified number of epochs (patience=10). This saves valuable GPU compute hours and prevents the network from memorizing training set noise (overfitting). Checkpoints are saved whenever validation fitness (a weighted composite of mAP50 and mAP50-95) reaches a new peak.",
           "Mention patience=10 and validation fitness tracking.")
    story.append(make_qa_card(18, q18[0], q18[1], q18[2], styles))

    q19 = ("What role does learning rate warmup play?",
           "In the first few epochs, model weights undergo large gradient updates. A high initial learning rate can destabilize pre-trained feature filters. A 3-epoch linear warmup gradually scales the learning rate from near-zero to lr0=0.01, allowing the optimizer's momentum and variance estimates to stabilize before full gradient updates begin.",
           "Describe it as stabilizing optimizer statistics and preserving pre-trained filters.")
    story.append(make_qa_card(19, q19[0], q19[1], q19[2], styles))

    q20 = ("How would you handle class imbalance if one class had 10x fewer samples?",
           "Class imbalance can be resolved using: (1) Class-weighted Focal Loss or Varifocal Loss, penalizing errors on minority classes more heavily; (2) Copy-Paste augmentation to synthetically superimpose minority class instances onto diverse backgrounds; (3) Targeted oversampling of images containing minority objects; or (4) Class-aware batch sampling.",
           "List 4 concrete techniques: Focal Loss, Copy-Paste, oversampling, and batch sampling.")
    story.append(make_qa_card(20, q20[0], q20[1], q20[2], styles))

    # DOMAIN 3: VIDEO STREAMING & REAL-TIME OPTIMIZATION
    story.append(Paragraph("Domain 3: Video Streaming, WebRTC & Latency Optimization (Questions 21 – 30)", styles['DocHeading2']))

    q21 = ("Why does standard synchronous WebRTC video streaming crash after 60 seconds in Streamlit?",
           "In naive implementations, model inference is called synchronously inside `recv(frame)`. Since inference takes ~30-40ms on CPU, the callback execution time exceeds the frame arrival interval (~33ms at 30 FPS). aiortc's internal frame queue accumulates unprocessed packets. This queue bloat leads to runaway memory usage, multi-second video lag, and eventually an unhandled timeout termination after exactly 60 seconds.",
           "Mention queue accumulation in aiortc and the frame arrival vs inference time mismatch.")
    story.append(make_qa_card(21, q21[0], q21[1], q21[2], styles))

    q22 = ("How does your AsyncHDLiveStreamProcessor solve the WebRTC buffer bloat problem?",
           "We decoupled camera ingestion from model inference. The main WebRTC thread reads frames, draws cached detections, and returns the annotated frame immediately at full 30 FPS with zero queue delay. Meanwhile, a background worker thread consumes frames via `threading.Event()` and `threading.Lock()`, runs downscaled inference asynchronously, and updates the shared detection cache. This ensures the ingestion queue never bloats.",
           "Explain the producer-consumer pattern and unblocked 30 FPS streaming.")
    story.append(make_qa_card(22, q22[0], q22[1], q22[2], styles))

    q23 = ("Why do you downscale frames to 480px width during live stream inference?",
           "Running inference on full 1080p or 720p frames requires massive bilinear interpolation and convolutional compute, taking >60ms on CPU. Downscaling frames to 480px width preserves aspect ratio while reducing pixel volume by over 70%, slashing inference latency to ~15ms. We then mathematically map bounding box coordinates back to full HD dimensions, achieving high-speed inference without degrading camera display quality.",
           "Explain that inference runs on 480px while display remains full 720p/1080p HD.")
    story.append(make_qa_card(23, q23[0], q23[1], q23[2], styles))

    q24 = ("Why did you use PyAV instead of OpenCV VideoWriter in the Streamlit Video Trace mode?",
           "OpenCV's `cv2.VideoWriter` typically encodes using the `mp4v` FourCC codec. Modern HTML5 `<video>` tags in Chrome, Edge, and Safari cannot decode raw `mp4v` streams, resulting in broken black players. PyAV provides direct bindings to FFmpeg's `libx264`, allowing us to specify `yuv420p` pixel format, `crf=23`, and `preset=veryfast`, producing fully browser-compatible MP4 videos natively.",
           "State clearly: browsers cannot play OpenCV's default mp4v; PyAV encodes native H.264 (libx264).")
    story.append(make_qa_card(24, q24[0], q24[1], q24[2], styles))

    q25 = ("What is Balanced Frame Striding in video processing and what is the trade-off?",
           "Balanced frame striding (stride=2) analyzes every 2nd frame with the neural network and carries bounding boxes forward to intermediate frames. This delivers a 2x throughput speedup (processing 50+ FPS instead of 25 FPS). The minor trade-off is slight bounding box lag on rapid, erratic object movements, but for standard 30 FPS video, the inter-frame motion is under 5 pixels, making the acceleration imperceptible to human eyes.",
           "Frame striding gives a 2x speedup by amortizing inference cost across adjacent frames.")
    story.append(make_qa_card(25, q25[0], q25[1], q25[2], styles))

    q26 = ("What does `cv2.CAP_DSHOW` do in the webcam detector script?",
           "On Windows, OpenCV's default video capture backend queries multiple legacy WDM/VFW drivers, which can freeze the application for 5-10 seconds during camera startup. `cv2.CAP_DSHOW` explicitly binds to the modern DirectShow API, initializing the camera instantly (<500ms) with direct hardware access.",
           "Shows deep platform-specific systems knowledge on Windows.")
    story.append(make_qa_card(26, q26[0], q26[1], q26[2], styles))

    q27 = ("How does the Exponential Moving Average (EMA) FPS calculation work in real-time streams?",
           "Instantaneous FPS (`1.0 / dt`) fluctuates wildly from frame to frame due to thread scheduling. EMA computes: `fps_smoothed = 0.9 * fps_smoothed + 0.1 * instant_fps`. This acts as a first-order low-pass filter, dampening transient spikes while reflecting sustained performance shifts within 10 frames.",
           "Explain it as a low-pass filter providing jitter-free telemetry.")
    story.append(make_qa_card(27, q27[0], q27[1], q27[2], styles))

    q28 = ("Why did you implement automatic temporary file cleanup in the video processor?",
           "Uploaded video files and processed H.264 streams can easily consume 100MB+ each. In a multi-user web application, unmanaged temporary files quickly exhaust disk storage, leading to server crashes. We read the generated video bytes directly into Streamlit's in-memory session state and immediately invoke `os.remove()` on both input and output disk files.",
           "Demonstrates production hygiene and disk management awareness.")
    story.append(make_qa_card(28, q28[0], q28[1], q28[2], styles))

    q29 = ("How does WebRTC negotiate connections between browser and server?",
           "WebRTC uses Session Description Protocol (SDP) offer/answer exchanges and Interactive Connectivity Establishment (ICE) candidates. STUN servers (`stun.l.google.com:19302`) discover public IP/port mappings across NAT firewalls, establishing an encrypted peer-to-peer UDP media stream via SRTP.",
           "Mention SDP offer/answer, ICE candidates, and STUN NAT traversal.")
    story.append(make_qa_card(29, q29[0], q29[1], q29[2], styles))

    q30 = ("What is the difference between video latency and video throughput?",
           "Throughput is the total number of frames processed per second (e.g. 60 FPS in batch mode). Latency is the end-to-end time delay from when a physical photon enters the camera sensor to when the annotated bounding box is drawn on screen (e.g. 25ms). In live streaming, low latency is critical; in offline video processing, high throughput is paramount.",
           "Clearly distinguish throughput (FPS) from latency (milliseconds delay).")
    story.append(make_qa_card(30, q30[0], q30[1], q30[2], styles))

    # DOMAIN 4: SOFTWARE ENGINEERING & PYTHON
    story.append(Paragraph("Domain 4: Python & Software Engineering Implementation (Questions 31 – 36)", styles['DocHeading2']))

    q31 = ("What is `@st.cache_resource` and why is it essential for the YOLO model in Streamlit?",
           "Streamlit executes the entire Python script from top to bottom on every user interaction or button click. Without caching, the 6MB YOLO weights would be re-read from disk and re-initialized in memory on every click, freezing the UI for 2-3 seconds. `@st.cache_resource` creates a singleton instance across all user sessions, loading the model once into shared memory.",
           "Mention singleton pattern and preventing redundant model re-instantiation.")
    story.append(make_qa_card(31, q31[0], q31[1], q31[2], styles))

    q32 = ("Why does OpenCV use BGR color format and why must you convert it to RGB?",
           "Historically, early digital camera sensor vendors and frame grabber libraries stored color channels in Blue-Green-Red byte order. OpenCV adopted BGR in 1999 for hardware compatibility. Modern display libraries (Pillow, Matplotlib, Streamlit) expect Red-Green-Blue. Failing to convert via `cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)` results in inverted, blue-tinted visuals.",
           "Demonstrates historical and technical understanding of image byte arrays.")
    story.append(make_qa_card(32, q32[0], q32[1], q32[2], styles))

    q33 = ("How do Python's GIL and multi-threading interact in your WebRTC asynchronous worker?",
           "The Global Interpreter Lock (GIL) permits only one Python thread to execute bytecode at once. However, computer vision libraries (OpenCV, PyTorch, NumPy) release the GIL during heavy C++/CUDA operations (matrix multiplications, convolutions, bilinear resizing). Thus, our background inference thread executes in true parallel concurrency with the main WebRTC thread.",
           "Explain that C++/CUDA extensions release the GIL during matrix math.")
    story.append(make_qa_card(33, q33[0], q33[1], q33[2], styles))

    q34 = ("Why did you use `threading.Event()` instead of a continuous `while True:` loop?",
           "A naive `while True:` loop consumes 100% of a CPU core in busy-waiting. `threading.Event().wait(timeout=0.1)` puts the inference worker thread into a dormant sleep state, waking it only when the main thread calls `.set()` upon receiving a new camera frame. This conserves CPU cycles and reduces thermal throttling.",
           "Contrast busy-waiting with event-driven OS thread scheduling.")
    story.append(make_qa_card(34, q34[0], q34[1], q34[2], styles))

    q35 = ("How does `resolve_path()` ensure deployment portability?",
           "When running Python scripts across different contexts (terminal, IDE, subfolder, Docker), relative paths like `model/best.pt` fail if the current working directory shifts. `resolve_path()` tests candidate paths relative to `__file__`, current working directory, and parent folders, returning an absolute path and ensuring seamless execution across any environment.",
           "Shows defensive programming and cross-environment deployment reliability.")
    story.append(make_qa_card(35, q35[0], q35[1], q35[2], styles))

    q36 = ("Why did you implement single-frame height constraints (480px) in the CSS?",
           "By default, high-resolution videos (1080p) render at full browser width, forcing users to scroll vertically between controls, detected item panels, and telemetry cards. By enforcing `max-height: 480px !important; object-fit: contain;`, the entire UI remains docked in a single desktop viewport, delivering a cohesive dashboard experience.",
           "Emphasizes user-centric design and dashboard usability.")
    story.append(make_qa_card(36, q36[0], q36[1], q36[2], styles))

    # DOMAIN 5: INTERVIEW DELIVERY & SYSTEM DESIGN
    story.append(Paragraph("Domain 5: High-Impact Interview Delivery & System Design (Questions 37 – 42)", styles['DocHeading2']))

    q37 = ("Give me your 60-second elevator pitch for this project.",
           "'I built Scoutline Vision Studio, an end-to-end custom object detection engine tailored for 7 common workplace and study items (person, bottle, cellphone, laptop, chair, pen, pencil). Standard COCO models omit critical stationery like pens and pencils and are often too slow for web deployment. I curated and validated a 26,756-image dataset, fine-tuned an anchor-free YOLOv8 Nano model on a Kaggle Tesla GPU using Automatic Mixed Precision, and achieved 78.5% mAP@50 with 81.9% precision. For deployment, I engineered a Cyber-Dark Streamlit app featuring PyAV H.264 video encoding and an asynchronous WebRTC decoupled streaming pipeline that eliminated a notorious 60-second buffer timeout crash, delivering continuous 30 FPS HD camera detection on consumer hardware.'",
           "Practice delivering this fluidly in under 60 seconds.")
    story.append(make_qa_card(37, q37[0], q37[1], q37[2], styles))

    q38 = ("What was the single hardest engineering bug you encountered, and how did you resolve it?",
           "'The hardest challenge was the WebRTC 60-second crash in Streamlit. Initially, synchronous inference inside `recv()` caused camera frames to process slower than the 30 FPS arrival rate. aiortc's internal packet queue bloated, creating severe 5-second lag and terminating with a timeout error after 1 minute. I re-architected the pipeline into an asynchronous producer-consumer model using `threading.Event()` and mutex locks. The video stream returns unblocked at 30 FPS, while a background thread runs inference on a downsampled 480px frame and projects coordinates back to HD. This eliminated queue bloat and allowed infinite continuous streaming.'",
           "This proves real hands-on debugging, systems architecture, and perseverance.")
    story.append(make_qa_card(38, q38[0], q38[1], q38[2], styles))

    q39 = ("How would you scale this system to process 10,000 live RTSP security camera streams?",
           "A centralized monolithic Streamlit server cannot scale to 10k streams. I would design a distributed microservices architecture: (1) Ingestion Layer: Edge gateways ingest RTSP streams and decode keyframes via GStreamer/FFmpeg; (2) Message Broker: Frames are published to a distributed Kafka or RabbitMQ queue; (3) Inference Workers: A Kubernetes cluster of Triton Inference Servers running TensorRT-optimized models with dynamic batching; (4) Output Storage: Detections are pushed to a Redis time-series database and forwarded to dashboards via WebSockets.",
           "Demonstrates senior-level distributed systems and cloud architecture thinking.")
    story.append(make_qa_card(39, q39[0], q39[1], q39[2], styles))

    q40 = ("How would you optimize inference speed 5x further for low-power edge devices (e.g. Raspberry Pi / Jetson)?",
           "(1) Export weights to ONNX and compile to TensorRT (on Jetson) or OpenVINO (on Intel CPU); (2) Apply INT8 Post-Training Quantization (PTQ) with calibration datasets to achieve a 4x reduction in memory bandwidth and 2-3x speedup; (3) Structured channel pruning to eliminate low-weight convolution filters; and (4) Knowledge Distillation using a YOLOv8x teacher model to boost the student model's accuracy.",
           "Mention TensorRT, INT8 Quantization, Pruning, and Distillation.")
    story.append(make_qa_card(40, q40[0], q40[1], q40[2], styles))

    q41 = ("What are the known failure modes of this model, and how would you fix them?",
           "Failure Mode 1: Heavy partial occlusion of small stationery (e.g. a hand completely wrapping around a pen). Fix: Collect targeted occlusion training data and use Copy-Paste augmentation. Failure Mode 2: Extreme low-light camera environments causing false negatives on dark chairs/bottles. Fix: Add Gamma adjustment and low-light synthetic noise augmentations during training. Failure Mode 3: Visual confusion between pen and pencil. Fix: Increase fine-grained high-resolution training crops of pen tips vs pencil erasers.",
           "Demonstrates intellectual honesty, self-awareness, and engineering problem solving.")
    story.append(make_qa_card(41, q41[0], q41[1], q41[2], styles))

    q42 = ("If you had another 2 weeks on this project, what would you implement next?",
           "(1) Real-time multi-object tracking using ByteTrack or DeepSORT to assign persistent IDs and trajectory vectors to objects across video frames; (2) Edge deployment benchmarking on an NVIDIA Jetson Nano using TensorRT FP16; (3) FastAPI backend decoupling to provide a REST and WebSocket API for mobile/IoT clients; and (4) An automated active learning pipeline that flags low-confidence production detections for automated human relabeling.",
           "Highlights tracking (ByteTrack), FastAPI backend, and active learning pipelines.")
    story.append(make_qa_card(42, q42[0], q42[1], q42[2], styles))

    story.append(Spacer(1, 10))

    # ==================================================================
    # SECTION 8: EMBEDDED SAMPLE DETECTIONS & PROOF OF PERFORMANCE
    # ==================================================================
    story.append(Paragraph("8.0 Out-of-Sample Test Detections & Empirical Proof", styles['DocHeading1']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E1"), spaceBefore=2, spaceAfter=8))

    story.append(Paragraph(
        "Below are real inference outputs generated by our trained <code>model/best.pt</code> checkpoint "
        "on out-of-sample images from the test set (<code>dataset_sources/dataset/test/images</code>), "
        "verifying detection accuracy and high-confidence localization across multiple target classes:",
        styles['DocBody']
    ))

    sample_detections = [
        [Paragraph("Sample Test Image", styles['TableHead']), Paragraph("Primary Detected Class", styles['TableHead']), Paragraph("Confidence Score", styles['TableHead']), Paragraph("Empirical Localization Observation", styles['TableHead'])],
        [Paragraph("bottle_0008_jpg...", styles['TableCellBold']), Paragraph("bottle", styles['TableCellBold']), Paragraph("<b>81.0%</b>", styles['TableCell']), Paragraph("Sharp bounding box around transparent plastic bottle body despite background clutter.", styles['TableCell'])],
        [Paragraph("chair_0007_jpg...", styles['TableCellBold']), Paragraph("chair", styles['TableCellBold']), Paragraph("<b>91.0%</b>", styles['TableCell']), Paragraph("Extremely tight localization around office chair frame and wheels without false triggers.", styles['TableCell'])],
        [Paragraph("laptop_01hiB08...", styles['TableCellBold']), Paragraph("laptop", styles['TableCellBold']), Paragraph("<b>84.0%</b>", styles['TableCell']), Paragraph("Accurately bounded open laptop screen and keyboard base under varied perspective.", styles['TableCell'])],
        [Paragraph("pencil_0801210...", styles['TableCellBold']), Paragraph("pencil", styles['TableCellBold']), Paragraph("<b>83.0%</b>", styles['TableCell']), Paragraph("Successfully localized slender, high-aspect-ratio pencil body against textured tabletop.", styles['TableCell'])],
    ]
    t_samples = Table(sample_detections, colWidths=[120, 100, 85, 227])
    t_samples.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0F172A")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#FFFFFF"), colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_samples)
    story.append(Spacer(1, 10))

    # Visual Detection Gallery (2x2 Grid)
    img_bottle = "outputs/images/bottle_0008_jpg.rf.98b6960b499f7fb01bd1fca72a567922_detected.jpg"
    img_chair = "outputs/images/chair_0007_jpg.rf.71aa1e451fe54b22a8040997dbab65a4_detected.jpg"
    img_laptop = "outputs/images/laptop_01hiB08j7yaJGJmPl2YhRRH-45-v1652463159-1-_jpg.rf.5b30fda36ed1ee8d260387d7f34e880f_detected.jpg"
    img_pencil = "outputs/images/pencil_0801210001_jpg.rf.1c030671e859f4066b8dca8d9fc16b6e_detected.jpg"

    if all(os.path.exists(p) for p in [img_bottle, img_chair, img_laptop, img_pencil]):
        story.append(Paragraph("<b>Visual Detection Gallery (Test Set Predictions):</b>", styles['DocHeading2']))
        
        w_img, h_img = 245, 175
        cell_1 = [RLImage(img_bottle, width=w_img, height=h_img), Spacer(1, 3), Paragraph("<b>Figure 8.1:</b> Bottle Detection (81% conf)", styles['TableCellBold'])]
        cell_2 = [RLImage(img_chair, width=w_img, height=h_img), Spacer(1, 3), Paragraph("<b>Figure 8.2:</b> Office Chair Detection (91% conf)", styles['TableCellBold'])]
        cell_3 = [RLImage(img_laptop, width=w_img, height=h_img), Spacer(1, 3), Paragraph("<b>Figure 8.3:</b> Laptop Detection (84% conf)", styles['TableCellBold'])]
        cell_4 = [RLImage(img_pencil, width=w_img, height=h_img), Spacer(1, 3), Paragraph("<b>Figure 8.4:</b> Slender Pencil Detection (83% conf)", styles['TableCellBold'])]

        gallery_table = Table([[cell_1, cell_2], [cell_3, cell_4]], colWidths=[260, 260])
        gallery_table.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('LEFTPADDING', (0,0), (-1,-1), 4),
            ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ]))
        story.append(gallery_table)
        story.append(Spacer(1, 12))

    story.append(make_callout(
        "FINAL INTERVIEW PREPARATION SUMMARY & CANDIDATE CHECKLIST",
        "<b>Before entering the interview room, ensure you have reviewed:</b><br/>"
        "✓ <b>Elevator Pitch:</b> 7 classes, 26k images, YOLOv8n anchor-free, 78.5% mAP50, 81.9% precision, WebRTC decoupling.<br/>"
        "✓ <b>Loss Functions:</b> BCE for classification, CIoU for box regression, and DFL for boundary probability distributions.<br/>"
        "✓ <b>Architectural Nuances:</b> C2f gradient flow, SPPF receptive field expansion, Decoupled Head vs Coupled Head.<br/>"
        "✓ <b>Streaming Engineering:</b> Why standard WebRTC crashes after 60s, and how producer-consumer threading + 480px downscaling solved buffer bloat.<br/>"
        "✓ <b>Code Ownership:</b> You understand every line of <code>validate_merged_dataset.py</code>, <code>image_detector.py</code>, <code>video_detector.py</code>, <code>webcam_detector.py</code>, and <code>streamlit-app/app.py</code>.",
        styles,
        accent_color=colors.HexColor("#10B981"),
        bg_color=colors.HexColor("#F0FDF4")
    ))

    # Build Document
    print(f"Building master PDF document at: {output_pdf_path} ...")
    doc.build(story, canvasmaker=NumberedCanvas)
    print("PDF build successful!")


if __name__ == "__main__":
    output_pdf = os.path.abspath("Custom_Object_Detection_Interview_Study_Guide.pdf")
    generate_pdf(output_pdf)
