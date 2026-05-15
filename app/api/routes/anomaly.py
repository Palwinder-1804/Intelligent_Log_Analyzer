from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from app.api.dependencies.auth_dependency import get_current_user

from app.models.log_model import parsed_logs_collection

from app.services.anomaly.anomaly_detection_service import (
    train_anomaly_model,
    detect_anomalies,
    MODEL_PATH
)

from app.services.anomaly.model_loader_service import (
    model_exists
)

router = APIRouter(
    prefix="/anomaly",
    tags=["Anomaly Detection"]
)


@router.post("/train")
async def train_model(
    current_user=Depends(get_current_user)
):

    parsed_logs = []

    async for log in parsed_logs_collection.find(
        {"parsed": True}
    ):
        parsed_logs.append(log)

    if not parsed_logs:
        raise HTTPException(
            status_code=400,
            detail="No parsed logs available"
        )

    return await train_anomaly_model(parsed_logs)


@router.post("/detect")
async def detect_log_anomalies(
    current_user=Depends(get_current_user)
):

    if not model_exists(MODEL_PATH):
        raise HTTPException(
            status_code=400,
            detail="Train model first"
        )

    parsed_logs = []

    async for log in parsed_logs_collection.find(
        {"parsed": True}
    ):
        parsed_logs.append(log)

    if not parsed_logs:
        raise HTTPException(
            status_code=400,
            detail="No parsed logs found"
        )

    results = await detect_anomalies(parsed_logs)

    return {
        "total_logs": len(parsed_logs),
        "anomalies_detected": len(
            [r for r in results if r["is_anomaly"]]
        ),
        "results": results
    }