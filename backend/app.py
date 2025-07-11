from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS so frontend can call this backend

# Load the trained model
model = joblib.load("predict_runs_model.pkl")  # Make sure this file is in the same folder

# Define the API route
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        print("Received input:", data)

        # Convert JSON to DataFrame
        input_df = pd.DataFrame([data])

        # Encode text data into integers for model compatibility
        for col in input_df.columns:
            input_df[col] = input_df[col].astype('category').cat.codes

        # Predict using the loaded model
        prediction = model.predict(input_df)[0]
        return jsonify({'predicted_runs': round(float(prediction), 2)})

    except Exception as e:
        print("Error:", e)
        return jsonify({'error': str(e)}), 500

# Run the app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
