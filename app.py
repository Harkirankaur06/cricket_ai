from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import requests
from io import BytesIO

app = Flask(__name__)
CORS(app)

# Google Drive loader for large .pkl files
def load_model_from_drive(file_id, save_as):
    def get_confirm_token(response):
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                return value
        return None

    def download_file(file_id):
        URL = "https://docs.google.com/uc?export=download"
        session = requests.Session()
        response = session.get(URL, params={'id': file_id}, stream=True)
        token = get_confirm_token(response)

        if token:
            response = session.get(URL, params={'id': file_id, 'confirm': token}, stream=True)

        with open(save_as, "wb") as f:
            for chunk in response.iter_content(32768):
                if chunk:
                    f.write(chunk)

        return save_as

    file_path = download_file(file_id)
    return joblib.load(file_path)

# ✅ Load both models
runs_model = load_model_from_drive("1HRe4PxVfXVw0-J6MNCQ38laWxQY-flPq", "runs_model.pkl")
wicket_model = load_model_from_drive("1p7OwxgqctUneztgXsoqG34wl8eVPEkq1", "wicket_model.pkl")

# ✅ Route: Predict Runs
@app.route('/predict', methods=['POST'])
def predict_runs():
    try:
        data = request.json
        input_df = pd.DataFrame([data])
        for col in input_df.columns:
            input_df[col] = input_df[col].astype('category').cat.codes
        prediction = runs_model.predict(input_df)[0]
        return jsonify({'predicted_runs': round(float(prediction), 2)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ✅ Route: Predict Wicket
@app.route('/predict_wicket', methods=['POST'])
def predict_wicket():
    try:
        data = request.json
        input_df = pd.DataFrame([data])
        for col in input_df.columns:
            input_df[col] = input_df[col].astype('category').cat.codes
        prediction = wicket_model.predict(input_df)[0]
        is_wicket = bool(prediction >= 0.5)  # binary classification style
        return jsonify({'wicket': is_wicket})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
