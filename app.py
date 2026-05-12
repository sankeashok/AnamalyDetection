import gradio as gr
import joblib
import pandas as pd
import numpy as np

# Load artifacts
model = joblib.load('network_anomaly_model.pkl')
scaler = joblib.load('scaler.pkl')
le_dict = joblib.load('label_encoders.pkl')
feature_names = joblib.load('feature_names.pkl')

def predict_anomaly(duration, protocol, service, flag, src_bytes, dst_bytes, count):
    # 1. Prepare input dictionary with defaults
    inputs = {col: 0.0 for col in feature_names}
    for col in le_dict:
        inputs[col] = le_dict[col].classes_[0]
        
    # 2. Update with user inputs
    inputs['duration'] = duration
    inputs['protocoltype'] = protocol
    inputs['service'] = service
    inputs['flag'] = flag
    inputs['srcbytes'] = src_bytes
    inputs['dstbytes'] = dst_bytes
    inputs['count'] = count
    
    # 3. Process data
    df = pd.DataFrame([inputs])[feature_names]
    for col, le in le_dict.items():
        if col in df.columns:
            df[col] = le.transform(df[col])
            
    scaled = scaler.transform(df)
    
    # 4. Predict
    prediction = model.predict(scaled)[0]
    probs = model.predict_proba(scaled)[0]
    
    label = "🚨 ANOMALY DETECTED" if prediction == 1 else "✅ NORMAL CONNECTION"
    confidence = {
        "Normal": float(probs[0]),
        "Anomaly": float(probs[1])
    }
    
    return label, confidence

# Build Gradio Interface
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🛡️ Network Anomaly Detection System")
    gr.Markdown("Identify suspicious network connections in real-time using Machine Learning.")
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("### 📡 Connection Details")
            duration = gr.Slider(0, 10000, value=0, label="Duration")
            protocol = gr.Dropdown(list(le_dict['protocoltype'].classes_), value="tcp", label="Protocol Type")
            service = gr.Dropdown(list(le_dict['service'].classes_), value="http", label="Service")
            flag = gr.Dropdown(list(le_dict['flag'].classes_), value="SF", label="Flag")
            src_bytes = gr.Number(value=181, label="Source Bytes")
            dst_bytes = gr.Number(value=5450, label="Destination Bytes")
            count = gr.Slider(0, 511, value=8, label="Connection Count")
            
            btn = gr.Button("Analyze Connection", variant="primary")
            
        with gr.Column():
            gr.Markdown("### 🔍 Analysis Result")
            output_label = gr.Label(label="Classification")
            output_probs = gr.Label(label="Confidence Scores")
            
    btn.click(
        fn=predict_anomaly, 
        inputs=[duration, protocol, service, flag, src_bytes, dst_bytes, count], 
        outputs=[output_label, output_probs]
    )
    
    gr.Markdown("---")
    gr.Markdown("Developed by **Sanke Ashok** for Scaler Portfolio Project 01.")

demo.launch()
