# train.py
"""
Train YOLOv8 on your custom dataset and produce best.pt
Run:  python train.py
"""
from ultralytics import YOLO
import shutil, os

DATA_YAML = r"C:\Users\ZaBir\Desktop\Real Time Anomoly Detection\Dataset\data.yaml"
BASE_MODEL = "yolov8n.pt"     # auto-downloaded on first run (~6 MB)
EPOCHS = 50
IMGSZ = 640

def main():
    if not os.path.exists(DATA_YAML):
        raise FileNotFoundError(
            f"[ERROR] {DATA_YAML} not found.\n"
            "Place your dataset inside datasets/my_dataset/ with the structure:\n"
            "  images/train, images/val, labels/train, labels/val, data.yaml"
        )

    print("[INFO] Loading base model...")
    model = YOLO(BASE_MODEL)

    print("[INFO] Starting training...")
    model.train(
        data=DATA_YAML,
        epochs=EPOCHS,
        imgsz=IMGSZ,
        batch=16,
        project="runs/detect",
        name="train",
        exist_ok=True,
        patience=20,
        verbose=True,
    )

    # copy best.pt to project root so app.py picks it up
    src = "runs/detect/train/weights/best.pt"
    if os.path.exists(src):
        shutil.copy(src, "best.pt")
        print(f"[SUCCESS] best.pt saved to project root → {os.path.abspath('best.pt')}")
    else:
        print("[WARN] best.pt not found — check runs/detect/train/weights/")

if __name__ == "__main__":
    main()