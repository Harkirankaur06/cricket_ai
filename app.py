from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import os
import requests

app = Flask(__name__)
CORS(app)

# 🔽 Function to download model from Hugging Face if not already present
def download_model(url, save_path):
    if not os.path.exists(save_path):
        print(f"Downloading model from: {url}")
        response = requests.get(url)
        response.raise_for_status()  # fail loudly if broken link
        with open(save_path, "wb") as f:
            f.write(response.content)
    return joblib.load(save_path)

# ✅ REPLACE these URLs with your actual Hugging Face model URLs
RUNS_MODEL_URL = "https://huggingface.co/harkirankaur/CRICKET-PREDICT/resolve/main/predict_runs_model.pkl"
WICKET_MODEL_URL = "https://huggingface.co/harkirankaur/CRICKET-PREDICT/resolve/main/predict_wicket_model.pkl"

runs_model = None
wicket_model = None

def get_runs_model():
    global runs_model
    if runs_model is None:
        print("Loading runs model...")
        runs_model = download_model(RUNS_MODEL_URL, "runs_model.pkl")
    return runs_model

def get_wicket_model():
    global wicket_model
    if wicket_model is None:
        print("Loading wicket model...")
        wicket_model = download_model(WICKET_MODEL_URL, "wicket_model.pkl")
    return wicket_model

@app.route('/predict', methods=['POST'])
def predict_runs():
    try:
        model = get_runs_model()
        data = request.json
        input_df = pd.DataFrame([data])
        for col in input_df.columns:
            input_df[col] = input_df[col].astype('category').cat.codes
        prediction = model.predict(input_df)[0]
        return jsonify({'predicted_runs': round(float(prediction), 2)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/predict_wicket', methods=['POST'])
def predict_wicket():
    try:
        model = get_wicket_model()
        data = request.json
        input_df = pd.DataFrame([data])
        for col in input_df.columns:
            input_df[col] = input_df[col].astype('category').cat.codes
        prediction = model.predict(input_df)[0]
        is_wicket = bool(prediction >= 0.5)
        return jsonify({'wicket': is_wicket})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
