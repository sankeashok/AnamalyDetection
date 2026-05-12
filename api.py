from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import numpy as np

app = Flask(__name__)
CORS(app)

# Load model and preprocessing artifacts
model = joblib.load('network_anomaly_model.pkl')
scaler = joblib.load('scaler.pkl')
le_dict = joblib.load('label_encoders.pkl')
feature_names = joblib.load('feature_names.pkl')

@app.route('/')
def home():
    return "Network Anomaly Detection API is running!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        # Convert JSON to DataFrame
        input_df = pd.DataFrame([data])
        
        # Ensure all required features are present (fill missing with 0)
        for col in feature_names:
            if col not in input_df.columns:
                if col in le_dict:
                    input_df[col] = le_dict[col].classes_[0]
                else:
                    input_df[col] = 0.0
        
        # Reorder columns to match training
        input_df = input_df[feature_names]
        
        # Encode categorical variables
        for col, le in le_dict.items():
            if col in input_df.columns:
                input_df[col] = le.transform(input_df[col])
        
        # Scale numerical features
        input_scaled = scaler.transform(input_df)
        
        # Make prediction
        prediction = model.predict(input_scaled)[0]
        prediction_prob = model.predict_proba(input_scaled)[0]
        
        result = {
            'prediction': int(prediction),
            'prediction_label': 'anomaly' if prediction == 1 else 'normal',
            'confidence': float(np.max(prediction_prob))
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
