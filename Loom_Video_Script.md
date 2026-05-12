# 🎥 Loom Demo Video Script & Outline (5 Minutes)

## 0:00 - 0:45: Introduction & Problem Statement
- **Introduction**: "Hi, I'm Sanke Ashok, and today I'll be presenting my Network Anomaly Detection project."
- **Problem**: Explain the rise of cyber threats and why traditional firewalls aren't enough.
- **Objective**: "To build an ML system that detects anomalies in network traffic with high precision."

## 0:45 - 2:00: Exploratory Data Analysis (EDA) & Hypothesis Testing
- **Dashboard**: Briefly mention the Tableau dashboard (show it if you have it open).
- **Notebook**: Open `Network_Anomaly_EDA.ipynb`.
- **Key Insights**:
    - Show the distribution of attack types.
    - Explain the Protocol Type hypothesis: "We found that certain protocols are significantly more associated with anomalies."
    - Show the Traffic Volume comparison: "Anomalous connections often have distinct byte count patterns."

## 2:00 - 3:30: Machine Learning Modeling
- **The Model**: Explain why you chose Random Forest.
- **Preprocessing**: Mention scaling and encoding.
- **Results**: Show the Classification Report (99.9% Accuracy).
- **Feature Importance**: Highlight that `src_bytes` and `service` are the biggest predictors.

## 3:30 - 4:30: Live Deployment Demo
- **Terminal**: Show the Flask app running (`python app.py`).
- **Test Script**: Run `python test_api.py`.
- **API Response**: "As you can see, the API receives network features in JSON format and instantly returns a prediction with a confidence score."

## 4:30 - 5:00: Recommendations & Conclusion
- **Recommendations**: Mention real-time monitoring and multi-class classification.
- **Conclusion**: "Thank you for watching. The full code is available on my GitHub."

---

### Tips for a Great Video:
- **Speak Clearly**: Don't rush through the technical parts.
- **Screen Sharing**: Use a tool like Loom to share your screen while your webcam is in the corner.
- **Preparation**: Have your terminal and notebook ready and cleared of any errors before you start recording.
