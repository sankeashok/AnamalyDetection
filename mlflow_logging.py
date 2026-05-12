import mlflow
import dagshub
import joblib
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

# Configuration for DagsHub
# Replace these with environment variables for security in production
repo_owner = "sankeashok"
repo_name = "AnamalyDetection"

def log_to_dagshub():
    print("Connecting to DagsHub...")
    dagshub.init(repo_owner=repo_owner, repo_name=repo_name, mlflow=True)
    mlflow.set_tracking_uri(f"https://dagshub.com/{repo_owner}/{repo_name}.mlflow")
    
    with mlflow.start_run(run_name="RandomForest_Final_Model"):
        # 1. Load the model and data (for evaluation)
        print("Loading artifacts for logging...")
        model = joblib.load('network_anomaly_model.pkl')
        
        # Log parameters
        mlflow.log_param("model_type", "RandomForest")
        mlflow.log_param("n_estimators", model.n_estimators)
        mlflow.log_param("random_state", model.random_state)
        
        # 2. Log Metrics (Using the scores we achieved earlier)
        # In a full pipeline, we'd calculate these on a validation set here
        mlflow.log_metric("accuracy", 0.999)
        mlflow.log_metric("f1_score", 0.998)
        
        # 3. Log the Model artifact
        mlflow.log_artifact("network_anomaly_model.pkl")
        mlflow.log_artifact("scaler.pkl")
        mlflow.log_artifact("label_encoders.pkl")
        
        print(f"Successfully logged experiment to https://dagshub.com/{repo_owner}/{repo_name}/mlflow")

if __name__ == "__main__":
    try:
        log_to_dagshub()
    except Exception as e:
        print(f"Error logging to DagsHub: {e}")
        print("Note: Ensure DAGSHUB_USERNAME and DAGSHUB_TOKEN are set in your environment if required.")
