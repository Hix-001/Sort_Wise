<div align="center">

```
███████╗ ██████╗ ██████╗ ████████╗    ██╗    ██╗██╗███████╗███████╗
██╔════╝██╔═══██╗██╔══██╗╚══██╔══╝    ██║    ██║██║██╔════╝██╔════╝
███████╗██║   ██║██████╔╝   ██║       ██║ █╗ ██║██║███████╗█████╗  
╚════██║██║   ██║██╔══██╗   ██║       ██║███╗██║██║╚════██║██╔══╝  
███████║╚██████╔╝██║  ██║   ██║       ╚███╔███╔╝██║███████║███████╗
╚══════╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝        ╚══╝╚══╝ ╚═╝╚══════╝╚══════╝
```

**AI-Powered Waste Intelligence — Point. Scan. Sort.**

[![Website](https://img.shields.io/badge/🌐_Launch_App-hix--001.github.io/Sort__Wise-00e676?style=for-the-badge&logoColor=white)](https://hix-001.github.io/Sort_Wise/)
[![Status](https://img.shields.io/badge/Status-Live_v2.0-00e676?style=for-the-badge)](https://hix-001.github.io/Sort_Wise/)
[![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](LICENSE)
[![Dataset](https://img.shields.io/badge/Dataset-15k_Images-purple?style=for-the-badge)]()
[![Made With](https://img.shields.io/badge/Made_with-TensorFlow.js-FF6F00?style=for-the-badge&logo=tensorflow)](https://www.tensorflow.org/js)

> *Built by a 19-year-old CSE student to tackle Delhi's urban waste crisis — one scan at a time.*

</div>

---

## ⚡ Use It Now

> No installation. No account. No cost. Just open the link and point your camera.

**[https://hix-001.github.io/Sort_Wise/](https://hix-001.github.io/Sort_Wise/)**

Works on any device with a browser — phone, tablet, laptop. The AI runs entirely on your device; nothing leaves your screen.

---

## 🧠 What It Does

Most people *want* to recycle. They just don't know which bin to use.

Sort Wise fixes that in one second. Point your phone at any piece of trash — a bottle, a pizza box, a broken charger — and the system instantly tells you:

- **What** the item is
- **Whether** it's recyclable, non-recyclable, or compostable
- **How** to dispose of it correctly (e.g. *"Rinse before recycling"* or *"Remove battery first"*)
- **Every item** in the frame simultaneously — point it at a full bin and scan everything at once

---

## 🏗️ Architecture

The system runs a two-stage AI pipeline entirely in the browser:

```
YOUR CAMERA / PHOTO
        │
        ▼
┌─────────────────────┐
│   COCO-SSD (Stage 1)│  ← Locates WHERE objects are in the frame
│   TensorFlow.js     │    Draws a bounding box around each item
└──────────┬──────────┘
           │  N cropped regions
           ▼
┌─────────────────────┐
│  MobileNetV2 Custom │  ← Identifies WHAT each item is
│  Trained on 15k img │    Classifies into waste categories
└──────────┬──────────┘
           │
           ▼
  ♻ RECYCLABLE  |  🗑 NON-RECYCLABLE  |  🌱 COMPOSTABLE
  + disposal tip per item
```

| Component | Technology | Purpose |
|:--|:--|:--|
| Object detection | COCO-SSD (TF.js) | Locate items in frame |
| Waste classification | MobileNetV2 (custom) | Identify waste category |
| Frontend | HTML5 / CSS3 / Vanilla JS | Cyberpunk UI, zero dependencies |
| Training pipeline | Python + Google Colab | Free GPU fine-tuning |
| Hosting | GitHub Pages | Free, zero-cost deployment |
| Local inference | Python + TFLite + OpenCV | Samsung S9 wireless scanner mode |

---

## 📂 Repository Structure

```
Sort_Wise/
│
├── index.html                        # Full web app — the entire frontend in one file
│
├── final_prompter.py                 # Python inference script (IP Webcam / S9 mode)
├── ai_waste_sorter.py                # Data collection script for custom dataset
│
├── vww_96_grayscale_quantized.tflite # Quantized TFLite model (offline/edge use)
├── labels_txt.txt                    # Class labels for the TFLite model
│
├── SortWise_Train.ipynb              # Google Colab notebook — train your own model
│
├── waste_management.db               # SQLite log — scan history & sustainability stats
└── requirements.txt                  # Python dependencies
```

---

## 🚀 Run Locally (Python + IP Webcam)

For the full hardware setup with your phone as a live scanner:

**1. Clone the repo**
```bash
git clone https://github.com/hix-001/Sort_Wise.git
cd Sort_Wise
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Connect your phone**

Install [IP Webcam](https://play.google.com/store/apps/details?id=com.pas.webcam) on your Android phone, start the server, and update the IP address in `final_prompter.py`:
```python
url = "http://YOUR_PHONE_IP:8080/video"
```

**4. Run**
```bash
python final_prompter.py
```

Controls in the OpenCV window:
| Key | Action |
|:--|:--|
| `q` | Quit |

The system will display real-time classification with confidence scores and a temporal smoothing window to eliminate flickering.

---

## 🔬 Training Your Own Model

The `SortWise_Train.ipynb` notebook lets you retrain the classifier on any dataset using a free Google Colab T4 GPU in ~25 minutes.

**Quick start:**
1. Open the notebook in Google Colab
2. Set runtime to **T4 GPU** (Runtime → Change runtime type)
3. Upload your dataset to Google Drive
4. Set `DATASET_PATH` in Cell 1
5. Run all cells — the final cell downloads your trained model

The notebook handles two-phase transfer learning automatically:
- **Phase 1** — trains the classification head (base frozen, fast)
- **Phase 2** — fine-tunes the top 30 layers (low LR, high accuracy)

Expected output accuracy on the standard garbage dataset: **90–96% validation accuracy**.

---

## 📊 Impact Tracking

Every scan is logged locally to `waste_management.db` with:

- Timestamp
- Detected item and category
- Confidence score
- Recyclability verdict

This enables long-term analytics on personal or institutional waste patterns — useful for schools, offices, or municipal pilot programs.

---

## 🌍 Why This Project Exists

Delhi generates over **11,000 tonnes of solid waste every day.** A large portion of recyclable material ends up in landfills not because people don't care — but because the system makes it too hard to know what goes where.

Sort Wise is a CSE student's answer to that problem: a tool that is free, instant, requires no training to use, and works on any phone already in your pocket. It is designed for the public and for government pilots alike.

---

## 📜 Credits & License

- **Developer** — [hix-001](https://github.com/hix-001) — 19-year-old Computer Science & Engineering student, Delhi
- **Dataset** — Kaggle TrashNet + Custom collected dataset (15,000+ images)
- **Hardware** — Samsung Galaxy S9 (IP Webcam) as wireless scanner
- **License** — MIT — use it, fork it, build on it

---

<div align="center">

*"The best time to fix the waste problem was 20 years ago. The second best time is now."*

**[Launch Sort Wise →](https://hix-001.github.io/Sort_Wise/)**

Built with purpose for a greener tomorrow.

</div>
