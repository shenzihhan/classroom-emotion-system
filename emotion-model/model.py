# -*- coding: utf-8 -*-
"""emotion_local.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1bwYEUT6PHh8z8vmH7vQxtbRJhZOvBR4q
"""

import cv2
import time
import numpy as np
from deepface import DeepFace
import requests
from datetime import datetime
import uuid

# === Config ===
API_ENDPOINT = "https://student-api-emk4.onrender.com/upload"
ANON_ID = "anon_" + str(uuid.uuid4())[:8]
RECORD_DURATION = 30  # seconds

# === Initialization ===
cap = cv2.VideoCapture(0)
cv2.namedWindow("Emotion Detection - Student", cv2.WINDOW_NORMAL)
frames = []
attention_scores = []
emotions_list = []
start_time = time.time()
print("Recording started. Please stay visible on camera.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to access camera.")
        break

    annotated_frame = frame.copy()
    try:
        analyses = DeepFace.analyze(annotated_frame, actions=['emotion'], enforce_detection=False)
        if not isinstance(analyses, list):
            analyses = [analyses]

        for result in analyses:
            emotion = result.get('dominant_emotion', 'unknown')
            region = result.get('region', {})
            x, y, w, h = region.get('x', 0), region.get('y', 0), region.get('w', 0), region.get('h', 0)

            if w > 0 and h > 0:
                cv2.rectangle(annotated_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(annotated_frame, emotion, (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            emotions_list.append(emotion)
            attention_scores.append(1 if emotion in ['happy', 'neutral', 'surprise'] else 0)

    except Exception as e:
        print(f"Analysis error: {e}")
        emotions_list.append("error")
        attention_scores.append(0)

    # Countdown display
    elapsed = time.time() - start_time
    remaining = int(RECORD_DURATION - elapsed)
    cv2.putText(annotated_frame, f"Time remaining: {remaining}s", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    resized = cv2.resize(annotated_frame, (960, 720))

    # Show result
    cv2.imshow("Emotion Detection - Student", resized)
    # Stop if 30 seconds passed or 'q' is pressed
    if elapsed >= RECORD_DURATION or cv2.waitKey(1) & 0xFF == ord('q'):
        break

# === Cleanup ===
cap.release()
cv2.destroyAllWindows()

# === Upload results ===
avg_attention = round(np.mean(attention_scores), 2) if attention_scores else 0
payload = {
    "student_id": ANON_ID,
    "emotions": emotions_list,
    "attention": avg_attention,
    "timestamp": datetime.utcnow().isoformat()
}

try:
    res = requests.post(API_ENDPOINT, json=payload)
    if res.status_code == 200:
        print("Emotions and attention uploaded successfully!")
    else:
        print(f"Failed to upload. Status: {res.status_code}")
except Exception as e:
    print(f"Upload error: {e}")
