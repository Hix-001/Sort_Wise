# ♻️ SORT WISE
### *AI-Powered Waste Intelligence System*

<div align="center">
  <img src="https://img.shields.io/badge/Status-Live_v2.0-00e676?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Dataset-15k_Images-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Hardware-Samsung_S9-orange?style=for-the-badge" />
</div>

---

## 🌐 [LIVE DEMO: SCAN NOW](https://hix-001.github.io/Sort_Wise/)
*Optimized for mobile browsers and real-time vision.*

---

## 📖 Project Vision
Sort Wise is a Computer Science & Engineering (CSE) initiative designed to solve the urban waste crisis in Delhi through accessible AI. Most people want to recycle but don't know which bin to use. This app bridges that gap with a **single click**.

### ⚡ Why it's Different:
* **Massive Brain:** Unlike basic tutorials, this was trained on a custom **15,000+ image dataset**.
* **Recycling Logic:** It doesn't just name the object; it tells you **how** to dispose of it (e.g., "Rinse the Plastic").
* **Hardware Agnostic:** Uses an old **Samsung S9** as a high-definition wireless scanner.

---

## 🛠️ Technical Architecture

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Vision Engine** | TensorFlow.js / TFLite | Real-time object detection |
| **Frontend UI** | HTML5 / CSS3 / JS | "Cyberpunk" dark-mode interface |
| **Data Core** | Python 3.13 | Backend processing and training |
| **Storage** | SQLite3 | Local history and sustainability logs |



---

## 📂 Repository Structure
* `index.html`: The main interactive web interface.
* `final_prompter.py`: The Python script for wireless S9 integration.
* `vww_96_grayscale_quantized.tflite`: The optimized "lite" brain.
* `waste_management.db`: The SQLite database tracking your impact.

---

## 🚀 Get Started in 60 Seconds

1.  **Clone & Install**
    ```bash
    git clone [https://github.com/hix-001/Sort_Wise.git](https://github.com/hix-001/Sort_Wise.git)
    cd Sort_Wise
    pip install -r requirements.txt
    ```

2.  **Connect Hardware**
    Start **IP Webcam** on your Samsung S9 and update the IP in `final_prompter.py`.

3.  **Run Inference**
    ```bash
    python final_prompter.py
    ```

---

## 📊 Impact Tracking
Every time an item is scanned, it is logged with its **recyclability status** and **confidence score**. This allows for long-term analytics on personal waste habits.

---

## 📜 License & Credits
* **License**: MIT
* **Developer**: [hix-001](https://github.com/hix-001) (19-year-old CSE Student)
* **Dataset**: Kaggle TrashNet + Custom Dataset (15k total).

---
<div align="center">
  <sub>Built with ❤️ for a Greener Tomorrow.</sub>
</div>