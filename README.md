# ⚡ Scoutline Vision Studio — Custom 7-Class Object Detection

[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-blue?logo=python&logoColor=white)](https://www.python.org/)
[![YOLOv8](https://img.shields.io/badge/YOLOv8-Nano%20(Anchor--Free)-00F2FE?logo=ultralytics&logoColor=black)](https://github.com/ultralytics/ultralytics)
[![PyTorch](https://img.shields.io/badge/PyTorch-Deep%20Learning-EE4C2C?logo=pytorch&logoColor=white)](https://pytorch.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Vision%20Studio-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![WebRTC](https://img.shields.io/badge/WebRTC-Asynchronous%20Decoupling-333333?logo=webrtc&logoColor=white)](https://webrtc.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An end-to-end deep learning visual perception suite and production-grade Web application powered by a custom-trained **YOLOv8 Nano** model for everyday workplace and study environments.

---

## 🎯 Key Benchmark & Architectural Highlights

| Metric / Dimension | Specification Value | Engineering Significance |
| :--- | :--- | :--- |
| **Target Classes (7)** | `person`, `bottle`, `cellphone`, `laptop`, `chair`, `pen`, `pencil` | Detects critical stationery & devices absent from standard COCO |
| **Model Architecture** | **YOLOv8n (Anchor-Free)** | Decoupled head, C2f gradient flow, SPPF multi-scale context |
| **Footprint & Complexity** | **3,012,213 (~3.01M params)** · **8.2 GFLOPs** · **130 layers** | Ultra-lightweight; enables >30 FPS CPU inference |
| **Dataset Magnitude** | **26,756 images** (20,092 Train / 4,413 Valid / 2,251 Test) | Multi-source validated corpus in normalized YOLO format |
| **Validation mAP@50** | **78.5% (0.785)** | High detection reliability across varied indoor scenes |
| **Precision / Recall** | **81.9% Precision** · **71.5% Recall** | Minimizes false triggers in automated monitoring |
| **Training Acceleration** | Kaggle GPU (Tesla T4/P100 16GB) · **AMP FP16** | 2x faster forward/backward pass via Tensor Cores |
| **Web Engine** | Scoutline Vision Studio (Streamlit + WebRTC + PyAV) | Cyber-Dark UI, decoupled async HD stream, 2x frame stride |

---

## 🚀 System Architecture

```
                                      +---------------------------------------------+
                                      |         26,756 Multi-Source Images          |
                                      +---------------------------------------------+
                                                             |
                                                             v
+-------------------------------------------------------------------------------------------------------------------+
| 1. DATA VALIDATION (validate_merged_dataset.py)                                                                   |
|    - Set reconciliation: Orphaned images without labels & labels without images                                   |
|    - Syntax & bounds checking: Exactly 5 values, class_id in [0, 6], coordinates in [0.0, 1.0]                     |
+-------------------------------------------------------------------------------------------------------------------+
                                                             |
                                                             v
+-------------------------------------------------------------------------------------------------------------------+
| 2. MODEL TRAINING (Kaggle GPU Tesla T4/P100)                                                                      |
|    - Transfer learning initialized from COCO pretrained weights (yolov8n.pt)                                      |
|    - Hyperparameters: imgsz=640, batch=16, SGD momentum=0.937, lr0=0.01, AMP (FP16)                            |
|    - Loss: CIoU (box=7.5) + BCE (cls=0.5) + Distribution Focal Loss (dfl=1.5)                                    |
|    - Augmentations: Mosaic 1.0, Flip LR 0.5, Random Erasing 0.4, HSV color jitter                                 |
+-------------------------------------------------------------------------------------------------------------------+
                                                             |
                                                             v
+-------------------------------------------------------------------------------------------------------------------+
| 3. INFERENCE ENGINES (Modular Suite)                                                                              |
|    - Desktop Image Detector (image_detector.py): File picker fallback & image annotation                         |
|    - Batch Video Processor (video_detector.py): Frame-by-frame processing & detection aggregation                 |
|    - Low-Latency Webcam (webcam_detector.py): DirectShow (CAP_DSHOW) on Windows & smoothed EMA FPS            |
+-------------------------------------------------------------------------------------------------------------------+
                                                             |
                                                             v
+-------------------------------------------------------------------------------------------------------------------+
| 4. PRODUCTION WEB STUDIO (streamlit-app/app.py)                                                                   |
|    - Mode 1: Image Scan — Instant photo analysis, telemetry grid, dual-view tabs, direct download                 |
|    - Mode 2: Video Trace — High-speed browser playback with PyAV H.264 muxing & 2x balanced frame striding       |
|    - Mode 3: Live Stream — WebRTC decoupled async worker (30 FPS HD, zero buffer bloat, eliminates 60s crash)     |
+-------------------------------------------------------------------------------------------------------------------+
```

---

## 📂 Project Structure

```text
custom-object-detection/
├── .agents/
│   ├── rules/
│   │   └── agent-skills.md              # Global operational skills directive
│   └── skills/                          # 25 Agent Skills (Addy Osmani)
├── inference/
│   ├── image_detector.py                # Standalone CLI/GUI single-image detector
│   ├── video_detector.py                # Offline video file processor
│   └── webcam_detector.py               # DirectShow live webcam monitor with smoothed FPS
├── model/
│   └── best.pt                          # Trained YOLOv8n weights (78.5% mAP50)
├── outputs/
│   └── images/                          # Sample detection predictions
├── scripts/
│   ├── generate_interview_guide_pdf.py  # ReportLab 19-page study guide PDF compiler
│   └── validate_merged_dataset.py       # Dataset integrity validation script
├── streamlit-app/
│   ├── app.py                           # Scoutline Vision Studio web application
│   ├── model/best.pt                    # Embedded web app model weights
│   └── requirements.txt                 # Web application dependencies
├── .gitignore                           # Excludes venv, large datasets, and bulky videos
├── AGENTS.md                            # Workspace operational skills directive
├── Custom_Object_Detection_Interview_Study_Guide.pdf  # 19-page master interview preparation guide
└── README.md                            # Project documentation
```

---

## 🛠️ Quickstart & Usage

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/sanjayk2004/custom-object-detection.git
cd custom-object-detection

# Create and activate virtual environment
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r streamlit-app/requirements.txt
pip install reportlab pypdf
```

### 2. Launching Scoutline Vision Studio (Web App)

```bash
cd streamlit-app
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

### 3. Running Standalone Desktop Detectors

```bash
# Detect on an image (opens native file picker if no argument is passed):
python inference/image_detector.py path/to/image.jpg

# Process a video file:
python inference/video_detector.py path/to/video.mp4

# Launch real-time webcam detection (press 'q' to quit):
python inference/webcam_detector.py
```

---

## 📖 Master Technical Study Guide (19-Page PDF)

Included in this repository is [`Custom_Object_Detection_Interview_Study_Guide.pdf`](Custom_Object_Detection_Interview_Study_Guide.pdf), a comprehensive **19-page dossier** prepared for technical interviews, featuring:
- In-depth computer vision theory (YOLOv8 vs Faster R-CNN, anchor-free design, CIoU derivation, DFL loss math).
- Granular line-by-line code walkthroughs of every script.
- The **42-question Master Interview Q&A Playbook** across CV theory, dataset engineering, WebRTC streaming, and systems architecture.
- Real test-set visual detection gallery with confidence metrics.

---

## 👤 Author

**Sanjay K**  
- GitHub: [@sanjayk2004](https://github.com/sanjayk2004)  
  
