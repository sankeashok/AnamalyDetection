"""
MLOps Training Pipeline — Network Anomaly Detection
=====================================================
This script performs end-to-end model training and logs all experiments,
parameters, metrics, and artifacts to DagsHub via MLflow.

Usage:
    1. Set your DagsHub token (one-time):
       $env:DAGSHUB_TOKEN = "your_dagshub_token_here"

    2. Run:
       .\.venv\Scripts\activate
       python train_and_log.py
"""

import os
import warnings
import mlflow
import mlflow.sklearn
import joblib
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for saving plots
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (
    accuracy_score, f1_score, precision_score,
    recall_score, classification_report, confusion_matrix
)

warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────────────────────────
# DAGSHUB CONFIG — update repo_name if it differs on DagsHub
# ─────────────────────────────────────────────────────────────────────────────
REPO_OWNER = "sankeashok"
REPO_NAME  = "network-anomaly-detection"

# ─────────────────────────────────────────────────────────────────────────────
# STEP 1 — Connect to DagsHub
# ─────────────────────────────────────────────────────────────────────────────
def connect_dagshub():
    print("Connecting to DagsHub MLflow tracking server...")
    token = os.environ.get("DAGSHUB_TOKEN")
    if not token:
        raise ValueError("DAGSHUB_TOKEN env var not set!")

    # Set MLflow basic auth directly — no interactive OAuth prompt
    os.environ["MLFLOW_TRACKING_USERNAME"] = REPO_OWNER
    os.environ["MLFLOW_TRACKING_PASSWORD"] = token

    tracking_uri = f"https://dagshub.com/{REPO_OWNER}/{REPO_NAME}.mlflow"
    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment("Network-Anomaly-Detection")
    print(f"   Tracking URI: {tracking_uri}")
    print(f"   Authenticated as: {REPO_OWNER}")

# ─────────────────────────────────────────────────────────────────────────────
# STEP 2 — Load & Preprocess Data
# ─────────────────────────────────────────────────────────────────────────────
def load_and_preprocess():
    print("\n📂 Loading dataset...")
    df = pd.read_csv("Network_anomaly_data.csv")
    df.drop_duplicates(inplace=True)
    print(f"   Shape after dedup: {df.shape}")

    # Binary label
    df["label"] = df["attack"].apply(lambda x: 0 if x == "normal" else 1)

    X = df.drop(["attack", "label", "lastflag"], axis=1, errors="ignore")
    y = df["label"]

    # Encode categorical
    le_dict = {}
    for col in X.select_dtypes(include=["object"]).columns:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col])
        le_dict[col] = le

    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Scale
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled  = scaler.transform(X_test)

    print(f"   Train: {X_train_scaled.shape} | Test: {X_test_scaled.shape}")
    return X_train_scaled, X_test_scaled, y_train, y_test, X.columns, scaler, le_dict

# ─────────────────────────────────────────────────────────────────────────────
# STEP 3 — Train, Evaluate & Log ONE model run
# ─────────────────────────────────────────────────────────────────────────────
def run_experiment(model, run_name, params,
                   X_train, X_test, y_train, y_test,
                   feature_names, scaler, le_dict):

    with mlflow.start_run(run_name=run_name):

        # --- PARAMS ---
        for k, v in params.items():
            mlflow.log_param(k, v)

        # --- TRAIN ---
        print(f"\n🏋️  Training: {run_name}")
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        # --- METRICS ---
        acc  = accuracy_score(y_test, y_pred)
        f1   = f1_score(y_test, y_pred, average="weighted")
        prec = precision_score(y_test, y_pred, average="weighted", zero_division=0)
        rec  = recall_score(y_test, y_pred, average="weighted", zero_division=0)

        mlflow.log_metric("accuracy",  acc)
        mlflow.log_metric("f1_score",  f1)
        mlflow.log_metric("precision", prec)
        mlflow.log_metric("recall",    rec)

        print(f"   Accuracy : {acc:.4f}")
        print(f"   F1 Score : {f1:.4f}")
        print(f"   Precision: {prec:.4f}")
        print(f"   Recall   : {rec:.4f}")

        # --- CONFUSION MATRIX PLOT ---
        cm_path = f"confusion_matrix_{run_name.replace(' ', '_')}.png"
        cm = confusion_matrix(y_test, y_pred)
        fig, ax = plt.subplots(figsize=(6, 5))
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                    xticklabels=["Normal", "Anomaly"],
                    yticklabels=["Normal", "Anomaly"], ax=ax)
        ax.set_xlabel("Predicted")
        ax.set_ylabel("Actual")
        ax.set_title(f"Confusion Matrix — {run_name}")
        fig.savefig(cm_path, bbox_inches="tight")
        plt.close(fig)
        mlflow.log_artifact(cm_path)
        os.remove(cm_path)

        # --- FEATURE IMPORTANCE (RF only) ---
        if hasattr(model, "feature_importances_"):
            fi_path = f"feature_importance_{run_name.replace(' ', '_')}.png"
            importances = pd.Series(model.feature_importances_, index=feature_names)
            top20 = importances.nlargest(20).sort_values()
            fig2, ax2 = plt.subplots(figsize=(8, 7))
            top20.plot(kind="barh", color="#2dd4bf", ax=ax2)
            ax2.set_title("Top 20 Feature Importances")
            fig2.savefig(fi_path, bbox_inches="tight")
            plt.close(fig2)
            mlflow.log_artifact(fi_path)
            os.remove(fi_path)

        # --- LOG MODEL ---
        mlflow.sklearn.log_model(model, artifact_path="model")

        # --- LOG ARTIFACTS (only for best/final run) ---
        if "RandomForest" in run_name:
            joblib.dump(model,        "network_anomaly_model.pkl")
            joblib.dump(scaler,       "preprocessor.pkl")
            joblib.dump(le_dict,      "label_encoders.pkl")
            joblib.dump(list(feature_names), "feature_names.pkl")

            mlflow.log_artifact("network_anomaly_model.pkl")
            mlflow.log_artifact("preprocessor.pkl")
            mlflow.log_artifact("label_encoders.pkl")
            mlflow.log_artifact("feature_names.pkl")
            print("   📦 Artifacts saved & logged.")

        run_id = mlflow.active_run().info.run_id
        print(f"   🔗 MLflow Run ID: {run_id}")

    return {"run_name": run_name, "accuracy": acc, "f1_score": f1}


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    connect_dagshub()

    X_train, X_test, y_train, y_test, feature_names, scaler, le_dict = load_and_preprocess()

    results = []

    # Experiment 1 — Decision Tree (baseline)
    results.append(run_experiment(
        model=DecisionTreeClassifier(random_state=42),
        run_name="DecisionTree_Baseline",
        params={"model_type": "DecisionTree", "max_depth": "None", "random_state": 42},
        X_train=X_train, X_test=X_test,
        y_train=y_train, y_test=y_test,
        feature_names=feature_names,
        scaler=scaler, le_dict=le_dict
    ))

    # Experiment 2 — Random Forest (final model)
    results.append(run_experiment(
        model=RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1),
        run_name="RandomForest_Final",
        params={"model_type": "RandomForest", "n_estimators": 100, "random_state": 42},
        X_train=X_train, X_test=X_test,
        y_train=y_train, y_test=y_test,
        feature_names=feature_names,
        scaler=scaler, le_dict=le_dict
    ))

    # Summary table
    print("\n" + "="*55)
    print("📊 EXPERIMENT SUMMARY")
    print("="*55)
    df_results = pd.DataFrame(results)
    print(df_results.to_string(index=False))
    print("="*55)
    print(f"\n✅ All runs logged to: https://dagshub.com/{REPO_OWNER}/{REPO_NAME}/experiments")
