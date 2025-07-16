from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pandas as pd
import joblib
from huggingface_hub import hf_hub_download
import gc
import os

app = Flask(__name__)
CORS(app)

# ✅ Load models ONCE with Hugging Face hub and cache
print("🔁 Downloading and loading runs model...")
runs_model = joblib.load(hf_hub_download(
    repo_id="harkirankaur/CRICKET-PREDICT",
    filename="predict_runs_model.pkl",
    repo_type="model"
))
gc.collect()

print("🔁 Downloading and loading wicket model...")
wicket_model = joblib.load(hf_hub_download(
    repo_id="harkirankaur/CRICKET-PREDICT",
    filename="predict_wicket_model.pkl",
    repo_type="model"
))
gc.collect()

# ✅ Serve frontend (index.html)
@app.route("/", methods=["GET"])
def serve_frontend():
    return send_from_directory("frontend", "index.html")

# ✅ Serve static files (CSS, JS, etc.)
@app.route("/frontend/<path:path>")
def serve_static(path):
    return send_from_directory("frontend", path)

# ✅ Predict Runs API
@app.route("/predict", methods=["POST"])
def predict_runs():
    try:
        data = request.json
        input_df = pd.DataFrame([data])
        for col in input_df.columns:
            input_df[col] = input_df[col].astype("category").cat.codes
        prediction = runs_model.predict(input_df)[0]
        return jsonify({"predicted_runs": round(float(prediction), 2)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Predict Wicket API
@app.route("/predict_wicket", methods=["POST"])
def predict_wicket():
    try:
        data = request.json
        input_df = pd.DataFrame([data])
        for col in input_df.columns:
            input_df[col] = input_df[col].astype("category").cat.codes
        prediction = wicket_model.predict(input_df)[0]
        return jsonify({"wicket": bool(prediction >= 0.5)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Run the server
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
