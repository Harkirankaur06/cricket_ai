from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)
model = joblib.load("predict_runs_model.pkl")

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    df = pd.DataFrame([data])
    
    for col in df.columns:
        df[col] = df[col].astype('category').cat.codes
    
    prediction = model.predict(df)[0]
    return jsonify({'predicted_runs': round(prediction, 2)})

if __name__ == '__main__':
    app.run(debug=True)
