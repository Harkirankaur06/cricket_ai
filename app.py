from flask import Flask, request, jsonify, send_from_directory
import joblib
import pandas as pd
import os
import requests

app = Flask(__name__)

# ✅ Serve your frontend as-is
@app.route("/", methods=["GET"])
def serve_frontend():
    return send_from_directory("frontend", "index.html")

# ✅ Serve static files (CSS, JS if needed)
@app.route("/frontend/<path:path>")
def serve_static(path):
    return send_from_directory("frontend", path)

# ✅ Use lazy loading for models
runs_model = None
wicket_model = None

def download_model(url, save_path):
    if not os.path.exists(save_path):
        r = requests.get(url)
        with open(save_path, "wb") as f:
            f.write(r.content)
    return joblib.load(save_path)

def get_runs_model():
    global runs_model
    if runs_model is None:
        print("Loading runs model...")
        runs_model = download_model(
            "https://huggingface.co/harkirankaur/CRICKET-PREDICT/resolve/main/predict_runs_model.pkl",
            "runs_model.pkl"
        )
    return runs_model

def get_wicket_model():
    global wicket_model
    if wicket_model is None:
        print("Loading wicket model...")
        wicket_model = download_model(
            "https://huggingface.co/harkirankaur/CRICKET-PREDICT/resolve/main/predict_wicket_model.pkl",
            "wicket_model.pkl"
        )
    return wicket_model

# ✅ API endpoints
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
        return jsonify({"error": str(e)}), 500

# ✅ Start the server
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
