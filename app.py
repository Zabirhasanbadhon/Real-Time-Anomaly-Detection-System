# app.py
from flask import Flask, render_template, Response, jsonify
import cv2
import supervision as sv
from ultralytics import YOLO
import threading
import time
import numpy as np
import os

app = Flask(__name__)

# -------------------------------------------------
# 1. Load model  (fallback to yolov8n if best.pt missing)
# -------------------------------------------------
MODEL_PATH = "best.pt" if os.path.exists("best.pt") else "yolov8n.pt"
print(f"[INFO] Loading model: {MODEL_PATH}")
model = YOLO(MODEL_PATH)

# -------------------------------------------------
# 2. Video sources
# -------------------------------------------------
VIDEO_1 = r"D:\My Projects\Real Time Anomaly Detection System\Dataset\demo.mp4"
VIDEO_2 = r"D:\My Projects\Real Time Anomaly Detection System\Dataset\demo2.mp4"

# -------------------------------------------------
# 3. Annotators
# -------------------------------------------------
colors = sv.ColorPalette.from_hex(
    ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FECA57"]
)
bbox_annotator = sv.BoxAnnotator(thickness=3, color=colors)


class CenterLabelAnnotator:
    """Draws class label centered inside bbox."""
    def __init__(self, text_scale=0.7, text_thickness=2, color=colors):
        self.text_scale = text_scale
        self.text_thickness = text_thickness
        self.color = color

    def annotate(self, scene: np.ndarray, detections: sv.Detections) -> np.ndarray:
        img = scene.copy()
        for (x1, y1, x2, y2), class_id, conf in zip(
            detections.xyxy.astype(int),
            detections.class_id,
            detections.confidence,
        ):
            label = f"{model.names[int(class_id)]} {conf:.2f}"
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
            (tw, th), baseline = cv2.getTextSize(
                label, cv2.FONT_HERSHEY_SIMPLEX,
                self.text_scale, self.text_thickness,
            )
            pad = 4
            cv2.rectangle(
                img,
                (cx - tw // 2 - pad, cy - th // 2 - pad),
                (cx + tw // 2 + pad, cy + th // 2 + pad),
                self.color.by_idx(int(class_id)).as_bgr(),
                -1,
            )
            cv2.putText(
                img, label,
                (cx - tw // 2, cy + th // 2 - baseline // 2),
                cv2.FONT_HERSHEY_SIMPLEX, self.text_scale,
                (255, 255, 255), self.text_thickness, cv2.LINE_AA,
            )
        return img


label_annotator = CenterLabelAnnotator()

# -------------------------------------------------
# 4. Frame storage
# -------------------------------------------------
frame_lock = threading.Lock()
frame_cam1 = None
frame_cam2 = None

# -------------------------------------------------
# 5. Alerts store (for /alerts endpoint)
# -------------------------------------------------
alert_lock = threading.Lock()
alerts = []                      # list of dicts
last_alert_time = {"cam1": 0, "cam2": 0}
ALERT_COOLDOWN = 3.0             # seconds between alerts per camera


def push_alert(cam: str, msg: str):
    now = time.time()
    if now - last_alert_time[cam] < ALERT_COOLDOWN:
        return
    last_alert_time[cam] = now
    with alert_lock:
        alerts.append({
            "cam": cam,
            "msg": msg,
            "type": "danger",
            "time": time.strftime("%H:%M:%S"),
        })
        # keep last 50
        if len(alerts) > 50:
            del alerts[:-50]


# -------------------------------------------------
# 6. Video processing worker
# -------------------------------------------------
def process_video(source: str, storage: str):
    global frame_cam1, frame_cam2
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        print(f"[ERROR] Cannot open {source}")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        results = model(frame, verbose=False)[0]
        detections = sv.Detections.from_ultralytics(results)

        # ---- fire alert if any detection ----
        if len(detections) > 0:
            names = [model.names[int(c)] for c in detections.class_id]
            uniq = list(dict.fromkeys(names))
            push_alert(storage, f"{storage.upper()}: {', '.join(uniq)} detected")

        annotated = bbox_annotator.annotate(scene=frame.copy(), detections=detections)
        annotated = label_annotator.annotate(scene=annotated, detections=detections)

        cv2.putText(
            annotated, time.strftime("%H:%M:%S"), (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2,
        )
        cv2.putText(
            annotated, f"{storage.upper()} | det:{len(detections)}", (10, 65),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 212, 255), 2,
        )

        with frame_lock:
            if storage == "cam1":
                frame_cam1 = annotated.copy()
            else:
                frame_cam2 = annotated.copy()


# -------------------------------------------------
# 7. MJPEG stream generator
# -------------------------------------------------
def generate_stream(storage: str):
    while True:
        with frame_lock:
            frame = frame_cam1 if storage == "cam1" else frame_cam2
        if frame is None:
            time.sleep(0.01)
            continue
        ret, buffer = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
        if not ret:
            continue
        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n"
               + buffer.tobytes() + b"\r\n")


# -------------------------------------------------
# 8. Routes
# -------------------------------------------------
@app.route("/")
def index():
    return render_template("dashboard.html")


@app.route("/cam1")
def cam1():
    return Response(generate_stream("cam1"),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/cam2")
def cam2():
    return Response(generate_stream("cam2"),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/alerts")
def get_alerts():
    with alert_lock:
        return jsonify(list(alerts))


@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "model": MODEL_PATH,
        "classes": list(model.names.values()),
        "alerts": len(alerts),
    })


# -------------------------------------------------
# 9. Entry point
# -------------------------------------------------
if __name__ == "__main__":
    threading.Thread(target=process_video, args=(VIDEO_1, "cam1"), daemon=True).start()
    threading.Thread(target=process_video, args=(VIDEO_2, "cam2"), daemon=True).start()

    print("Pyresearch Dashboard LIVE → http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, threaded=True)