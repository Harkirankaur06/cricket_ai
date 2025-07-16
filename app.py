from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import joblib
import pandas as pd
import os
from huggingface_hub import hf_hub_download

app = Flask(__name__)
CORS(app)  # Allow frontend/backend interaction

# ✅ Serve the frontend (index.html)
@app.route("/", methods=["GET"])
def serve_frontend():
    return send_from_directory("frontend", "index.html")

# ✅ Serve static files (CSS, JS, etc.)
@app.route("/frontend/<path:path>")
def serve_static(path):
    return send_from_directory("frontend", path)

# ✅ Lazy loading models from Hugging Face
runs_model = None
wicket_model = None

def get_runs_model():
    global runs_model
    if runs_model is None:
        print("Downloading and loading runs model...")
        file_path = hf_hub_download(
            repo_id="harkirankaur/CRICKET-PREDICT",
            filename="predict_runs_model.pkl",
            repo_type="model"
        )
        runs_model = joblib.load(file_path)
    return runs_model

def get_wicket_model():
    global wicket_model
    if wicket_model is None:
        print("Downloading and loading wicket model...")
        file_path = hf_hub_download(
            repo_id="harkirankaur/CRICKET-PREDICT",
            filename="predict_wicket_model.pkl",
            repo_type="model"
        )
        wicket_model = joblib.load(file_path)
    return wicket_model

# ✅ Prediction APIs
@app.route("/predict", methods=["POST"])
def predict_runs():
    try:
        model = get_runs_model()
        data = request.json
        input_df = pd.DataFrame([data])
        for col in input_df.columns:
            input_df[col] = input_df[col].astype("category").cat.codes
        prediction = model.predict(input_df)[0]
        return jsonify({"predicted_runs": round(float(prediction), 2)})
    except Exception as e:
        print("Error in /predict:", e)
        return jsonify({"error": str(e)}), 500

@app.route("/predict_wicket", methods=["POST"])
def predict_wicket():
    try:
        model = get_wicket_model()
        data = request.json
        input_df = pd.DataFrame([data])
        for col in input_df.columns:
            input_df[col] = input_df[col].astype("category").cat.codes
        prediction = model.predict(input_df)[0]
        is_wicket = bool(prediction >= 0.5)
        return jsonify({"wicket": is_wicket})
    except Exception as e:
        print("Error in /predict_wicket:", e)
        return jsonify({"error": str(e)}), 500

# ✅ Run the server
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
