from datetime import datetime

from sklearn.ensemble import IsolationForest

import joblib

from app.models.anomaly_model import anomalies_collection

from app.services.anomaly.feature_extraction_service import (
    extract_features
)


MODEL_PATH = "trained_models/isolation_forest.pkl"


async def train_anomaly_model(parsed_logs):

    dataframe = extract_features(parsed_logs)

    model = IsolationForest(
        contamination=0.1,
        random_state=42
    )

    model.fit(dataframe)

    joblib.dump(
        model,
        MODEL_PATH
    )

    return {
        "message": "Anomaly model trained successfully"
    }


async def detect_anomalies(parsed_logs):

    model = joblib.load(MODEL_PATH)

    dataframe = extract_features(parsed_logs)

    predictions = model.predict(dataframe)

    scores = model.decision_function(dataframe)

    anomaly_results = []

    for index, prediction in enumerate(predictions):

        is_anomaly = prediction == -1

        score = float(scores[index])

        severity = "LOW"

        if score < -0.2:
            severity = "CRITICAL"
        elif score < -0.1:
            severity = "HIGH"
        elif score < 0:
            severity = "MEDIUM"

        result = {
            "raw_log_id": parsed_logs[index]["raw_log_id"],
            "anomaly_score": score,
            "is_anomaly": is_anomaly,
            "severity": severity,
            "message": parsed_logs[index].get("message"),
            "created_at": datetime.utcnow()
        }

        anomaly_results.append(result)

    if anomaly_results:
        await anomalies_collection.insert_many(
            anomaly_results
        )

    return anomaly_results