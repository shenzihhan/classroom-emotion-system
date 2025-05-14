from flask import Flask, request, jsonify
import os
import json
from datetime import datetime

app = Flask(__name__)

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

@app.route("/upload", methods=["POST"])
def upload_emotions():
    data = request.json
    student_id = data.get("student", "unknown")
    emotions = data.get("emotions", {})
    attention = data.get("attention", 0)
    timestamp = datetime.utcnow().isoformat()

    record = {
        "student_id": student_id,
        "timestamp": timestamp,
        "emotions": emotions,
        "attention": attention
    }

    # Save to file (optional)
    filename = f"{student_id}_{timestamp}.json"
    with open(os.path.join(DATA_DIR, filename), "w") as f:
        json.dump(record, f)

    print(f"Received from {student_id} at {timestamp}: {emotions}, attention: {attention}")

    return jsonify({"status": "success", "message": "Emotion data received."})

@app.route("/all", methods=["GET"])
def get_all_emotions():
    all_results = []
    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".json"):
            with open(os.path.join(DATA_DIR, filename)) as f:
                try:
                    data = json.load(f)
                    all_results.append(data)
                except:
                    continue
    return jsonify({"data": all_results})

@app.route("/")
def home():
    return "Student Emotion API is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
