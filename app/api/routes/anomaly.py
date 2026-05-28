import asyncio
from fastapi import (
    APIRouter,
    Depends
)

from app.api.dependencies.auth_dependency import (
    get_current_user
)

from app.schemas.anomaly_schema import (
    AnomalyDetectRequest,
)

from app.services.anomaly.hybrid_detection_service import (
    detect_anomaly
)

from app.services.anomaly.anomaly_storage_service import (
    store_anomaly
)

router = APIRouter(
    prefix="/anomaly",
    tags=["Hybrid Anomaly Detection"]
)


@router.post("/detect")
async def detect_log_anomaly(
    request: AnomalyDetectRequest,
    current_user=Depends(get_current_user)
):

    result = await asyncio.to_thread(detect_anomaly, request.log)

    await store_anomaly(result)

    return result