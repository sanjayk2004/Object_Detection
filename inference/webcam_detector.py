import os
import time
# pyrefly: ignore [missing-import]
import cv2
# pyrefly: ignore [missing-import]
from ultralytics import YOLO

MODEL_PATH = r"model\best.pt"
CONF_THRESHOLD = 0.35
CAM_INDEX = 0  # change to 1 if you have multiple cameras and the wrong one opens

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

def run_webcam():
    model = YOLO(resolve_model_path())

    cap = cv2.VideoCapture(CAM_INDEX, cv2.CAP_DSHOW)  # CAP_DSHOW avoids slow startup on Windows
    if not cap.isOpened():
        print("Error: could not open webcam. Try changing CAM_INDEX to 1.")
        return

    print("Webcam started. Press 'q' in the video window to quit.")

    prev_time = time.time()
    fps_smoothed = 0.0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: failed to read frame from webcam.")
            break

        results = model.predict(source=frame, conf=CONF_THRESHOLD, verbose=False)
        result = results[0]
        annotated = result.plot()

        # FPS calculation
        curr_time = time.time()
        instant_fps = 1.0 / max(curr_time - prev_time, 1e-6)
        fps_smoothed = 0.9 * fps_smoothed + 0.1 * instant_fps if fps_smoothed > 0 else instant_fps
        prev_time = curr_time

        cv2.putText(
            annotated,
            f"FPS: {fps_smoothed:.1f}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

        cv2.imshow("Custom Object Detection - Webcam (press 'q' to quit)", annotated)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Quit key pressed. Stopping webcam.")
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    run_webcam()