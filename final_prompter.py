import cv2
import numpy as np
import tensorflow as tf
import threading
import os
from collections import deque

# --- LABELS ---
class_names = ["background", "paper", "plastic", "trash"]

# --- SORTING LOGIC ---
RECYCLABLE = {"paper", "plastic"}

def get_verdict(label):
    if label == "background":
        return "PLACE ITEM IN FRAME", (160, 160, 160)
    elif label in RECYCLABLE:
        return "RECYCLABLE", (0, 200, 80)
    else:
        return "NON-RECYCLABLE", (0, 60, 220)

# --- CONFIG ---
CONFIDENCE_THRESHOLD = 0.70   # Phase 2: minimum confidence to show a verdict
SMOOTHING_WINDOW     = 5      # Phase 2: how many consecutive frames must agree

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
def get_path(filename):
    return os.path.join(BASE_DIR, filename)

# --- THREADED VIDEO STREAM ---
class VideoStream:
    def __init__(self, src):
        self.cap = cv2.VideoCapture(src)
        self.ret, self.frame = self.cap.read()
        self.stopped = False
        threading.Thread(target=self.update, daemon=True).start()

    def update(self):
        while not self.stopped:
            self.ret, self.frame = self.cap.read()

    def get_frame(self):
        return self.frame

    def stop(self):
        self.stopped = True
        self.cap.release()

# --- LOAD MODEL ---
model_path = get_path("vww_96_grayscale_quantized.tflite")
interpreter = tf.lite.Interpreter(model_path=model_path)
interpreter.allocate_tensors()
input_details  = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# --- PHASE 1 FIX: read the model's actual expected dtype ---
INPUT_DTYPE = input_details[0]['dtype']
print(f"[INFO] Model input dtype: {INPUT_DTYPE.__name__}")
print(f"[INFO] Model input shape: {input_details[0]['shape']}")

# --- CAMERA ---
url = "http://162.16.0.99:8080/video"
vs  = VideoStream(url)

# --- PHASE 2: rolling window for temporal smoothing ---
prediction_window = deque(maxlen=SMOOTHING_WINDOW)

print("[INFO] AI Waste Sorter — Phase 1+2 active. Press 'q' to quit.")

while True:
    frame = vs.get_frame()
    if frame is None:
        continue

    display = frame.copy()
    h, w = display.shape[:2]

    # --- PREPROCESS ---
    gray    = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, (96, 96))

    # PHASE 1 FIX: feed the correct dtype — no forced float32, no /255 for INT8
    if INPUT_DTYPE == np.uint8:
        # Quantized INT8 model — feed raw 0-255 uint8 values
        input_data = np.expand_dims(resized, axis=(0, -1)).astype(np.uint8)
    else:
        # Float model (fallback) — normalise to 0-1
        input_data = np.expand_dims(resized, axis=(0, -1)).astype(np.float32) / 255.0

    # --- INFERENCE ---
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    raw_output = interpreter.get_tensor(output_details[0]['index'])[0]

    # Dequantize if output is INT8 (convert to 0-1 probabilities)
    output_dtype = output_details[0]['dtype']
    if output_dtype == np.uint8:
        scale, zero_point = output_details[0]['quantization']
        prediction = (raw_output.astype(np.float32) - zero_point) * scale
    else:
        prediction = raw_output.astype(np.float32)

    raw_index      = int(np.argmax(prediction))
    raw_confidence = float(prediction[raw_index])
    raw_label      = class_names[raw_index]

    # --- PHASE 2A: confidence gate ---
    # If the model isn't sure enough, treat it as uncertain (not background)
    if raw_confidence < CONFIDENCE_THRESHOLD and raw_label != "background":
        gated_label      = "uncertain"
        gated_confidence = raw_confidence
    else:
        gated_label      = raw_label
        gated_confidence = raw_confidence

    # --- PHASE 2B: temporal smoothing ---
    prediction_window.append(gated_label)

    # Only commit to a label if the last N frames all agree
    if len(prediction_window) == SMOOTHING_WINDOW and len(set(prediction_window)) == 1:
        stable_label = prediction_window[-1]
    else:
        stable_label = None   # still stabilising

    # --- DISPLAY ---
    # Confidence bar (bottom of frame)
    bar_width = int(w * raw_confidence)
    bar_color = (0, 200, 80) if raw_confidence >= CONFIDENCE_THRESHOLD else (0, 140, 220)
    cv2.rectangle(display, (0, h - 18), (bar_width, h), bar_color, -1)
    cv2.putText(display, f"Conf: {raw_confidence*100:.0f}%  [{raw_label}]",
                (8, h - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)

    if stable_label is None:
        # Stabilising — show a neutral prompt
        cv2.putText(display, "Analysing...", (20, 52),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (200, 200, 200), 2)

    elif stable_label == "uncertain":
        cv2.putText(display, "HOLD ITEM STILL", (20, 52),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 180, 240), 2)

    else:
        verdict, color = get_verdict(stable_label)
        # Big verdict text
        cv2.putText(display, verdict, (20, 52),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.1, color, 3)
        # Item class below
        cv2.putText(display, f"Item: {stable_label.upper()}  ({gated_confidence*100:.0f}%)",
                    (20, 88), cv2.FONT_HERSHEY_SIMPLEX, 0.65, color, 2)

    # Smoothing window indicator (small dots top-right)
    for i, past in enumerate(prediction_window):
        dot_color = (0, 200, 80) if past not in ("background", "uncertain") else (80, 80, 80)
        cv2.circle(display, (w - 20 - i * 18, 20), 6, dot_color, -1)

    cv2.imshow("AI Waste Sorter — Phase 1+2", display)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

vs.stop()
cv2.destroyAllWindows()
print("[INFO] Session ended.")