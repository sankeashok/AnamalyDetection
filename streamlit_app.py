import streamlit as st
import joblib
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# Optimized Page Config
st.set_page_config(
    page_title="Anomaly Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for "Single-Page" feel
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .block-container { padding-top: 1.5rem; padding-bottom: 0rem; }
    h1 { font-size: 2.2rem !important; margin-bottom: 1rem !important; }
    h4 { font-size: 1.1rem !important; color: #888; }
    .stMetric { background-color: rgba(255, 255, 255, 0.03); padding: 10px; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_resource
def load_artifacts():
    return (
        joblib.load('network_anomaly_model.pkl'),
        joblib.load('scaler.pkl'),
        joblib.load('label_encoders.pkl'),
        joblib.load('feature_names.pkl')
    )

model, scaler, le_dict, feature_names = load_artifacts()

# Sidebar
st.sidebar.title("📡 Parameters")
with st.sidebar:
    duration = st.slider('Duration', 0, 10000, 0)
    protocol = st.selectbox('Protocol', le_dict['protocoltype'].classes_)
    service = st.selectbox('Service', le_dict['service'].classes_, index=20)
    flag = st.selectbox('Flag', le_dict['flag'].classes_)
    
    with st.expander("🛠️ Traffic Stats"):
        src_bytes = st.number_input('Src Bytes', value=181)
        dst_bytes = st.number_input('Dst Bytes', value=5450)
        count = st.slider('Count', 0, 511, 8)

def predict():
    inputs = {}
    for col in feature_names:
        if col in le_dict: inputs[col] = le_dict[col].classes_[0]
        else: inputs[col] = 0.0
            
    inputs['duration'], inputs['protocoltype'], inputs['service'], inputs['flag'] = duration, protocol, service, flag
    inputs['srcbytes'], inputs['dstbytes'], inputs['count'] = src_bytes, dst_bytes, count
    
    df = pd.DataFrame([inputs])[feature_names]
    for col, le in le_dict.items():
        if col in df.columns: df[col] = le.transform(df[col])
    
    scaled = scaler.transform(df)
    return model.predict(scaled)[0], model.predict_proba(scaled)[0]

try:
    pred, prob = predict()
    confidence = np.max(prob) * 100

    # HEADER
    st.title("🛡️ Network Anomaly Detection Dashboard")
    
    # MAIN GRID
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown(f"#### STATUS: {'🚨 ANOMALY DETECTED' if pred==1 else '✅ NORMAL CONNECTION'}")
        
        # Optimized Gauge
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = confidence,
            title = {'text': "Confidence", 'font': {'size': 18}},
            gauge = {
                'axis': {'range': [None, 100], 'tickfont': {'size': 10}},
                'bar': {'color': "#ff4b4b" if pred==1 else "#00ff00"},
                'bgcolor': "rgba(0,0,0,0)",
                'steps': [{'range': [0, 100], 'color': 'rgba(255,255,255,0.05)'}]
            }
        ))
        fig_gauge.update_layout(height=350, margin=dict(l=30, r=30, t=50, b=20), paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"})
        st.plotly_chart(fig_gauge, use_container_width=True)

    with col2:
        st.markdown("#### TOP PREDICTORS")
        
        # Optimized Bar Chart
        feat_imp = pd.Series(model.feature_importances_, index=feature_names).sort_values(ascending=False).head(10)
        fig_bar = px.bar(feat_imp, x=feat_imp.values, y=feat_imp.index, orientation='h', template="plotly_dark", height=380)
        fig_bar.update_layout(margin=dict(l=0, r=0, t=10, b=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font={'size': 10})
        fig_bar.update_traces(marker_color='#1f77b4')
        st.plotly_chart(fig_bar, use_container_width=True)

    # RE-SYNCED Metrics
    m1, m2, m3 = st.columns(3)
    m1.metric("Risk Level", "High" if pred==1 else "Low")
    m2.metric("Protocol", protocol.upper())
    m3.metric("Service", service.upper())

    st.markdown("---")
    st.caption("Developed by Sanke Ashok | [GitHub](https://github.com/sankeashok/Anamoly-Detection)")

except Exception as e:
    st.error(f"Prediction Error: {e}")
