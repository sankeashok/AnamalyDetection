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

custom_css = """
body { background: linear-gradient(135deg, #0f2027, #203a43, #2c5364) !important; }
.gradio-container {
    background: rgba(255, 255, 255, 0.05) !important;
    backdrop-filter: blur(15px) !important;
    -webkit-backdrop-filter: blur(15px) !important;
    border-radius: 20px !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37) !important;
}
.primary-btn {
    background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%) !important;
    border: none !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease !important;
}
.primary-btn:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 5px 15px rgba(0, 114, 255, 0.4) !important;
}
"""

theme = gr.themes.Base(
    primary_hue="blue",
    neutral_hue="slate",
    font=[gr.themes.GoogleFont('Inter'), 'ui-sans-serif', 'system-ui', 'sans-serif'],
)

# Build Gradio Interface
with gr.Blocks(theme=theme, css=custom_css) as demo:
    with gr.Row():
        gr.Markdown(
            """
            <div style="text-align: center; margin-bottom: 20px;">
                <h1 style="color: white; font-weight: 800; letter-spacing: 1px;">🛡️ Network Anomaly Detection System</h1>
                <p style="color: #a0aec0; font-size: 1.1em;">Real-time AI-powered threat analysis and connection classification</p>
            </div>
            """
        )
    
    with gr.Row():
        with gr.Column(scale=1):
            with gr.Group():
                gr.Markdown("### 📡 Connection Details", elem_classes="section-title")
                duration = gr.Slider(0, 10000, value=0, label="Duration", info="Length of connection in seconds")
                with gr.Row():
                    protocol = gr.Dropdown(list(le_dict['protocoltype'].classes_), value="tcp", label="Protocol Type")
                    service = gr.Dropdown(list(le_dict['service'].classes_), value="http", label="Service")
                    flag = gr.Dropdown(list(le_dict['flag'].classes_), value="SF", label="Flag")
                with gr.Row():
                    src_bytes = gr.Number(value=181, label="Source Bytes")
                    dst_bytes = gr.Number(value=5450, label="Destination Bytes")
                count = gr.Slider(0, 511, value=8, label="Connection Count", info="Number of connections to same host in past 2 seconds")
            
            btn = gr.Button("🔍 Analyze Connection", variant="primary", elem_classes="primary-btn")
            
        with gr.Column(scale=1):
            with gr.Group():
                gr.Markdown("### 🔬 Analysis Result", elem_classes="section-title")
                output_label = gr.Label(label="Classification Status")
                output_probs = gr.Label(label="Confidence Scores")
            
    btn.click(
        fn=predict_anomaly, 
        inputs=[duration, protocol, service, flag, src_bytes, dst_bytes, count], 
        outputs=[output_label, output_probs]
    )
    
    gr.Markdown(
        """
        <div style="text-align: center; margin-top: 30px; color: #a0aec0; font-size: 0.9em;">
            Developed by <strong>Sanke Ashok</strong> for Scaler Portfolio Project 01.
        </div>
        """
    )

demo.launch()
