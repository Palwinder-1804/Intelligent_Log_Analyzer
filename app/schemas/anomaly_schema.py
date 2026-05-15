from pydantic import BaseModel
from typing import Optional


class AnomalyDetectRequest(BaseModel):
    log: str


class AnomalyResultSchema(BaseModel):
    raw_log_id: str
    anomaly_score: float
    is_anomaly: bool
    severity: str
    message: Optional[str] = None