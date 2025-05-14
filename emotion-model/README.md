# Emotion Model (Mini-Xception)

This folder contains the emotion classification model used in the classroom-emotion-system project.

## Model Overview

- **Architecture:** Mini-Xception (via DeepFace pretrained model)  
- **Source:** Pretrained on FER-2013, used through DeepFace's emotion API  
- **Output Classes:** `['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']`  
- **Usage:** Integrated directly into classroom engagement system for real-time facial emotion detection  

---

## Fairness & Bias Evaluation

We evaluated the pretrained model for potential bias across race groups using a test dataset of 135 labeled images:

- **Caucasian**: 15 happy, 15 angry, 15 sad  
- **Black**: 15 happy, 15 angry, 15 sad  
- **Asian**: 15 happy, 15 angry, 15 sad  

The goal was to identify whether the model's accuracy or misclassification rate varies significantly by racial group. Results and observations are summarized in `bias_evaluation.ipynb`.

---

## Files

- `model.py` – Optional model loading or wrapper (not custom trained)  
- `bias_evaluation.ipynb` – Fairness test using a balanced emotion dataset  
- `weights/model.h5` – Placeholder for compatibility (not custom trained)

---

## Usage Example (via DeepFace)

```python
from deepface import DeepFace

# Run emotion detection on a frame
result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
dominant_emotion = result[0]['dominant_emotion']
