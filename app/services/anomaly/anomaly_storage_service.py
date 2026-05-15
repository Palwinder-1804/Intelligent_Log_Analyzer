from datetime import datetime

from app.core.database import database


anomaly_collection = database[
    "hybrid_anomalies"
]


async def store_anomaly(result):

    result["created_at"] = datetime.utcnow()

    await anomaly_collection.insert_one(
        result
    )