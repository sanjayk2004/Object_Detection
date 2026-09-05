import argparse
import os
# pyrefly: ignore [missing-import]
import cv2
# pyrefly: ignore [missing-import]
from ultralytics import YOLO
import tkinter as tk
from tkinter import filedialog

MODEL_PATH = r"model\best.pt"
CONF_THRESHOLD = 0.35

def resolve_model_path(path=MODEL_PATH):
    candidates = [
        path,
        os.path.join(os.path.dirname(__file__), "..", path),
        os.path.join(os.path.dirname(__file__), "..", "streamlit-app", path),
    ]
    for c in candidates:
        if os.path.exists(c):
            return os.path.abspath(c)
    return path

def pick_video_file():
    root = tk.Tk()
    root.withdraw()  # hide the empty tkinter window
    root.attributes('-topmost', True)  # bring dialog to front

    file_path = filedialog.askopenfilename(
        title="Select a video file",
        filetypes=[("Video files", "*.mp4 *.avi *.mov *.mkv"), ("All files", "*.*")]
    )
    root.destroy()
    return file_path

def detect_video(video_path, output_dir="outputs/videos"):
    if not os.path.exists(video_path):
        print(f"Error: video not found at {video_path}")
        return

    os.makedirs(output_dir, exist_ok=True)

    model = YOLO(resolve_model_path())

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: could not open video {video_path}")
        return

    fps = cap.get(cv2.CAP_PROP_FPS) or 25
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    base_name = os.path.splitext(os.path.basename(video_path))[0]
    output_path = os.path.join(output_dir, f"{base_name}_detected.mp4")

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    frame_idx = 0
    class_counts = {}

    print(f"Processing video: {video_path}")
    print(f"Resolution: {width}x{height} | FPS: {fps:.1f} | Total frames: {total_frames}")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model.predict(source=frame, conf=CONF_THRESHOLD, verbose=False)
        result = results[0]
        annotated = result.plot()

        for box in result.boxes:
            cls_id = int(box.cls[0])
            cls_name = model.names[cls_id]
            class_counts[cls_name] = class_counts.get(cls_name, 0) + 1

        writer.write(annotated)
        frame_idx += 1

        if frame_idx % 30 == 0 or frame_idx == total_frames:
            print(f"  Processed frame {frame_idx}/{total_frames}")

    cap.release()
    writer.release()

    print(f"\nDone. Processed {frame_idx} frames.")
    print("Detection counts across all frames (per-frame, not unique objects):")
    if class_counts:
        for cls_name, count in sorted(class_counts.items(), key=lambda x: -x[1]):
            print(f"  {cls_name}: {count}")
    else:
        print("  No objects detected in any frame.")

    print(f"\nSaved annotated video to: {output_path}")
    return output_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run custom object detection on a video.")
    parser.add_argument("video_path", nargs="?", default=None, help="Path to the input video (optional, opens file picker if omitted)")
    args = parser.parse_args()

    video_path = args.video_path

    if not video_path:
        print("No video path provided — opening file picker...")
        video_path = pick_video_file()
        if not video_path:
            print("No file selected. Exiting.")
            exit()

    detect_video(video_path)