import argparse
import os
# pyrefly: ignore [missing-import]
import cv2
# pyrefly: ignore [missing-import]
from ultralytics import YOLO
import tkinter as tk
from tkinter import filedialog

MODEL_PATH = r"model\best.pt"       # person, bottle, cellphone, laptop, chair, pen, pencil
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

def pick_image_file():
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)

    file_path = filedialog.askopenfilename(
        title="Select an image file",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp"), ("All files", "*.*")]
    )
    root.destroy()
    return file_path

def detect_image(image_path, output_dir="outputs/images"):
    if not os.path.exists(image_path):
        print(f"Error: image not found at {image_path}")
        return

    os.makedirs(output_dir, exist_ok=True)

    model = YOLO(resolve_model_path())

    results = model.predict(source=image_path, conf=CONF_THRESHOLD, save=False, verbose=False)
    result = results[0]
    annotated = result.plot()

    base_name = os.path.splitext(os.path.basename(image_path))[0]
    output_path = os.path.join(output_dir, f"{base_name}_detected.jpg")
    cv2.imwrite(output_path, annotated)

    print(f"\nDetections for {image_path}:")
    if len(result.boxes) == 0:
        print("  No objects detected.")
    else:
        for box in result.boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            print(f"  {model.names[cls_id]}: {conf:.2f}")

    print(f"\nSaved annotated image to: {output_path}")
    return output_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run custom object detection on an image.")
    parser.add_argument("image_path", nargs="?", default=None, help="Path to the input image (optional, opens file picker if omitted)")
    args = parser.parse_args()

    image_path = args.image_path

    if not image_path:
        print("No image path provided — opening file picker...")
        image_path = pick_image_file()
        if not image_path:
            print("No file selected. Exiting.")
            exit()

    detect_image(image_path)