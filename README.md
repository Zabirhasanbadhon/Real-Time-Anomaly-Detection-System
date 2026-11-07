# 🛡️ ZaBir — Real-Time Anomaly Detection System

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Flask-Web%20Framework-black?logo=flask" />
  <img src="https://img.shields.io/badge/YOLOv8-Object%20Detection-purple" />
  <img src="https://img.shields.io/badge/OpenCV-Computer%20Vision-green?logo=opencv" />
  <img src="https://img.shields.io/badge/Supervision-Detection%20Tools-orange" />
  <img src="https://img.shields.io/badge/Status-Active-success" />
</p>

<p align="center">
  <b>AI-Powered Multi-Camera Security & Intelligent Monitoring System</b>
  <br/>
  Detect anomalies. Monitor multiple cameras. Stay protected.
</p>

---

## 📸 Dashboard Preview

<p align="center">
  <img src="assets/Dashboard.png"
       alt="Real Time Anomaly Detection System Dashboard"
       width="100%"/>
</p>

---

## 🌟 Overview

**Real-Time Anomaly Detection System** is a lightweight, high-performance, AI-powered security and monitoring system designed to detect custom objects and anomalies across multiple video streams simultaneously.

Built with **Flask, Ultralytics YOLOv8, OpenCV, and Supervision**, the system processes multiple camera feeds using multithreading and streams real-time annotated video directly to a modern web dashboard.

The application features intelligent detection alerts, confidence-based object recognition, and low-latency MJPEG streaming, providing an efficient solution for real-time visual monitoring.

## ✨ Key Features

- 📹 **Multi-Camera Monitoring** — Process two video streams simultaneously.
- 🤖 **AI-Powered Detection** — Custom object detection using YOLOv8.
- 🎯 **Custom Anomaly Recognition** — Detect objects from your specially trained dataset.
- 📦 **Real-Time Annotations** — Display bounding boxes, class names, and confidence scores.
- 🌐 **Modern Web Dashboard** — Interactive interface with a glassmorphism-inspired design.
- 🚨 **Smart Detection Alerts** — Receive real-time alerts when target objects are detected.
- ⏱️ **Alert Cooldown** — Built-in 3-second cooldown to prevent repeated notifications.
- ⚡ **MJPEG Live Streaming** — Stream annotated video directly to your browser.
- 🧵 **Multithreaded Processing** — Process multiple video feeds concurrently.
- 🧠 **Custom Model Training** — Train your own YOLOv8 model using a custom dataset.
- 🔄 **Automatic Model Loading** — Load trained `best.pt` weights for custom detection.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| 🐍 Python | Core programming language |
| 🌐 Flask | Backend web framework |
| 🤖 YOLOv8 | AI object detection |
| 👁️ OpenCV | Video capture and image processing |
| 📦 Supervision | Detection annotation utilities |
| 🔢 NumPy | Numerical operations |
| 🎨 HTML5 / CSS3 | Dashboard design |
| ⚡ JavaScript | Frontend interactions |
| 🧵 Threading | Concurrent camera processing |

---

### 📌 File Descriptions

| File / Folder | Description |
|---|---|
| `app.py` | Flask backend and real-time detection engine |
| `train.py` | YOLOv8 custom model training script |
| `yolov8n.pt` | Trained YOLOv8 model weights |
| `demo.mp4` | First camera video source |
| `demo2.mp4` | Second camera video source |
| `requirements.txt` | Required Python dependencies |
| `templates/` | HTML dashboard templates |
| `data.yaml` | Dataset configuration |

---

## 🚀 Getting Started

Follow these steps to install and run VisionGuard AI on your local machine.

### 1️⃣ Prerequisites

Make sure you have installed:

- Python 3.10–3.12 (recommended)
- pip package manager
- Visual Studio Code (optional)
- A webcam or video files
- Internet connection for downloading model weights and dependencies

> ⚠️ Python 3.14 may not be supported by all dependencies and their compatible PyTorch builds. Python 3.11 or 3.12 is recommended.

### 2️⃣ Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/VisionGuard-AI.git
```

### 3️⃣ Navigate to the Project

```bash
cd Real-Time-Anomaly-Detection-System
```

### 4️⃣ Create a Virtual Environment (Recommended)

```bash
python -m venv venv
```

**Windows:**

```bash
venv\Scripts\activate
```

### 5️⃣ Install Dependencies

```bash
python -m pip install --upgrade pip
```

```bash
pip install -r requirements.txt
```

Alternatively, install the main dependencies manually:

```bash
pip install flask ultralytics opencv-python supervision numpy
```

---

## 🎬 Video Source Configuration

VisionGuard AI supports multiple video streams.

Place two video files in the project root directory:

```text
demo.mp4
demo2.mp4
```

You can use your own security footage or royalty-free sample videos.

> 💡 Make sure the filenames match the video paths configured in `app.py`.

---

## 🧠 Custom YOLOv8 Model Training

ZaBir — Real-Time Anomaly Detection System supports custom-trained YOLOv8 models for detecting specific objects and anomalies.

If you already have a trained `yolov8n.pt` file, place it in the project root directory and skip the training process.

**Important:**
- `nc` represents the number of object classes.
- `names` contains your custom class names.
- The number of class names must match `nc`.
- Image and label filenames must correspond.

### 3️⃣ Start Model Training

Run the training script:

```bash
python train.py
```

The training script should:

1. Load the YOLOv8 base model.
2. Read your custom dataset.
3. Train the detection model.
4. Generate the best-performing weights.
5. Copy the resulting `yolov8n.pt` into the project root directory.

### 4️⃣ Use Your Trained Model

After successful training:

```text
VisionGuard-AI/
│
├── yolov8n.pt
├── app.py
└── train.py
```

Your application can now use your custom-trained model.

---

## 💻 Running The System

Once the dependencies, video sources, and model are ready, launch the Flask application.

```bash
python app.py
```

Open your browser and visit:

🌐 **http://localhost:5000**

You should now see ZaBir — Real-Time Anomaly Detection System web dashboard with your camera feeds and real-time detection results.

---

## 🚨 Smart Alert System

ZaBir — Real-Time Anomaly Detection System includes a real-time alert mechanism to notify users when configured target objects are detected.

### Alert Features

- 🎯 Detect target objects using YOLOv8.
- 🚨 Generate alerts when detections occur.
- ⚡ Display alerts on the web dashboard.
- ⏱️ Apply a 3-second cooldown between repeated alerts.

This helps reduce unnecessary repeated notifications during continuous detection.

---

## ⚡ Real-Time MJPEG Streaming

The application uses **MJPEG (Motion JPEG)** to deliver annotated video streams directly to the browser.

### Benefits

- Low-latency video streaming.
- No WebRTC configuration required.
- Simple browser integration.
- Continuous annotated frame delivery.
- Suitable for local multi-camera monitoring.

---

## ⚙️ Troubleshooting

### ❌ 1. Black Screen in Browser

**Possible causes:**
- Video files are missing.
- Incorrect video paths.
- OpenCV cannot access the video source.

**Solution:**

Check that both files exist:

```text
demo.mp4
demo2.mp4
```

Also verify the terminal output for camera or video capture errors.

### ❌ 2. TemplateNotFound Error

**Problem:**

```text
jinja2.exceptions.TemplateNotFound: dashboard.html
```

**Solution:**

Make sure your HTML file is inside the `templates` directory:

```text
templates/dashboard.html
```

### ❌ 3. Supervision AttributeError

Make sure your annotation code uses the API supported by your installed Supervision version.

For example:

```python
sv.BoxAnnotator()
sv.LabelAnnotator()
```

### ❌ 4. ModuleNotFoundError

Install the required packages:

```bash
pip install flask ultralytics opencv-python supervision numpy
```

### ❌ 5. YOLO Model Not Found

Ensure `best.pt` exists in the project root and that the model path in `app.py` is correct.

### ❌ 6. OpenCV Video Processing Issues

Try reinstalling OpenCV:

```bash
python -m pip uninstall opencv-python opencv-python-headless -y
```

```bash
python -m pip install opencv-python
```

---

## 🔐 Security & Privacy

- Use authorized camera feeds only.
- Secure the Flask application before exposing it to a public network.
- Avoid exposing video streams without authentication.
- Protect custom-trained model files and recorded footage.

---

## 🛠️ Built With

<p align="center">
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/></a>
  <a href="https://flask.palletsprojects.com/"><img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white"/></a>
  <a href="https://github.com/ultralytics/ultralytics"><img src="https://img.shields.io/badge/YOLOv8-111F68?style=for-the-badge"/></a>
  <a href="https://opencv.org/"><img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white"/></a>
  <a href="https://github.com/roboflow/supervision"><img src="https://img.shields.io/badge/Supervision-FF6F00?style=for-the-badge"/></a>
</p>

---

## 👨‍💻 Developer

**ZaBir Hasan**

🌐 Website: [www.zabirhasan.com](https://www.zabirhasan.com)

---

<p align="center">
  <b>🛡️ ZaBir — Real-Time Anomaly Detection System</b>
  <br/>
  <i>See More. Detect Smarter. Stay Safer.</i>
  <br/><br/>
  Made with ❤️ using Python and Artificial Intelligence.
</p>
