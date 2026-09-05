"""
Scoutline — Streamlit frontend + backend in one.

Run locally:
    streamlit run app.py

Deploy on Render:
    Start command -> streamlit run app.py --server.port $PORT --server.address 0.0.0.0
"""

import os
import tempfile
import time

# pyrefly: ignore [missing-import]
import av
# pyrefly: ignore [missing-import]
import cv2
# pyrefly: ignore [missing-import]
import numpy as np
# pyrefly: ignore [missing-import]
import streamlit as st
# pyrefly: ignore [missing-import]
from PIL import Image
# pyrefly: ignore [missing-import]
from ultralytics import YOLO
# pyrefly: ignore [missing-import]
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, RTCConfiguration

# ------------------------------------------------------------
# Config
# ------------------------------------------------------------
MODEL_PATH_1 = os.path.join("model", "best.pt")     # person, bottle, cellphone, laptop, chair, pen, pencil
MODEL_PATH_2 = os.path.join("model", "best1.pt")    # book, watch — added once trained
CONF_THRESHOLD = 0.35

st.set_page_config(page_title="Scoutline — Object Detection", page_icon="🎯", layout="centered")

# ------------------------------------------------------------
# Light theming — matches the viewfinder / bounding-box concept
# ------------------------------------------------------------
st.markdown("""
<style>
    .stApp { background-color: #0B1210; }
    h1, h2, h3 { color: #ECF3EF; font-family: 'Sora', sans-serif; }
    p, label, .stMarkdown { color: #ECF3EF; }
    .stButton>button {
        background-color: #B8FF3D;
        color: #0B1210;
        border-radius: 999px;
        font-weight: 600;
        border: none;
    }
    .eyebrow {
        font-family: monospace;
        color: #B8FF3D;
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# Load models once, cached across reruns
# ------------------------------------------------------------
@st.cache_resource
def load_models():
    m1 = YOLO(MODEL_PATH_1)
    m2 = YOLO(MODEL_PATH_2) if os.path.exists(MODEL_PATH_2) else None
    return m1, m2

model1, model2 = load_models()

# ------------------------------------------------------------
# Shared detection helper
# ------------------------------------------------------------
def run_models_on_frame(frame_bgr: np.ndarray) -> np.ndarray:
    """Runs model1 (and model2 if present) on a BGR frame, returns annotated BGR frame."""
    results1 = model1.predict(source=frame_bgr, conf=CONF_THRESHOLD, verbose=False)
    annotated = results1[0].plot()

    if model2 is not None:
        results2 = model2.predict(source=frame_bgr, conf=CONF_THRESHOLD, verbose=False)
        for box in results2[0].boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            label = model2.names[int(box.cls[0])]
            conf = float(box.conf[0])
            cv2.rectangle(annotated, (x1, y1), (x2, y2), (255, 0, 255), 2)
            cv2.putText(annotated, f"{label} {conf:.2f}", (x1, max(y1 - 10, 0)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)

    return annotated

# ------------------------------------------------------------
# Header
# ------------------------------------------------------------
st.markdown('<p class="eyebrow">7-CLASS DETECTOR · PERSON · BOTTLE · CELLPHONE · LAPTOP · CHAIR · PEN · PENCIL</p>', unsafe_allow_html=True)
st.title("🎯 Scoutline")
st.write("Point it at anything. Watch it get named.")

mode = st.sidebar.radio(
    "Choose a mode",
    ["Image Scan", "Live Watch", "Video Trace"],
)

if model2 is None:
    st.sidebar.info("Running with 7 classes only — best1.pt (book, watch) not found yet.")

# ------------------------------------------------------------
# IMAGE SCAN
# ------------------------------------------------------------
if mode == "Image Scan":
    st.header("Image Scan")
    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        image = Image.open(uploaded_image).convert("RGB")
        frame_bgr = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        with st.spinner("Scanning..."):
            annotated_bgr = run_models_on_frame(frame_bgr)
            annotated_rgb = cv2.cvtColor(annotated_bgr, cv2.COLOR_BGR2RGB)

        st.image(annotated_rgb, caption="Detection result", use_container_width=True)

        # download button
        success, buffer = cv2.imencode(".jpg", annotated_bgr)
        st.download_button(
            "Download result",
            data=buffer.tobytes(),
            file_name=f"scoutline_{uploaded_image.name}",
            mime="image/jpeg",
        )

# ------------------------------------------------------------
# VIDEO TRACE
# ------------------------------------------------------------
elif mode == "Video Trace":
    st.header("Video Trace")
    uploaded_video = st.file_uploader("Upload a video", type=["mp4", "mov", "avi"])

    if uploaded_video is not None:
        # save to a temp file since OpenCV needs a real file path
        in_path = os.path.join(tempfile.gettempdir(), f"scoutline_in_{int(time.time())}.mp4")
        with open(in_path, "wb") as f:
            f.write(uploaded_video.read())

        out_path = os.path.join(tempfile.gettempdir(), f"scoutline_out_{int(time.time())}.mp4")

        cap = cv2.VideoCapture(in_path)
        fps = cap.get(cv2.CAP_PROP_FPS) or 25
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        writer = cv2.VideoWriter(out_path, fourcc, fps, (width, height))

        progress_bar = st.progress(0, text="Tracing frames...")
        frame_idx = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            annotated = run_models_on_frame(frame)
            writer.write(annotated)
            frame_idx += 1
            if total_frames > 0:
                progress_bar.progress(min(frame_idx / total_frames, 1.0), text=f"Tracing frames... {frame_idx}/{total_frames}")

        cap.release()
        writer.release()
        progress_bar.empty()

        st.video(out_path)

        with open(out_path, "rb") as f:
            st.download_button(
                "Download result",
                data=f.read(),
                file_name=f"scoutline_{uploaded_video.name}",
                mime="video/mp4",
            )

        os.remove(in_path)
        os.remove(out_path)

# ------------------------------------------------------------
# LIVE WATCH (webcam, via streamlit-webrtc)
# ------------------------------------------------------------
elif mode == "Live Watch":
    st.header("Live Watch")
    st.write("Opens your camera and detects objects in real time, right in the browser.")

    class DetectionProcessor(VideoProcessorBase):
        def recv(self, frame):
            img = frame.to_ndarray(format="bgr24")
            annotated = run_models_on_frame(img)
            return av.VideoFrame.from_ndarray(annotated, format="bgr24")

    RTC_CONFIGURATION = RTCConfiguration({"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})

    webrtc_streamer(
        key="scoutline-live",
        video_processor_factory=DetectionProcessor,
        rtc_configuration=RTC_CONFIGURATION,
        media_stream_constraints={"video": True, "audio": False},
    )

    st.caption("Nothing from your camera is stored — detection happens frame by frame, live.")

st.markdown("---")
st.caption("Scoutline — a custom-trained YOLO detector · person, bottle, cellphone, laptop, chair, pen, pencil")