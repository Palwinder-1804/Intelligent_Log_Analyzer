from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends,
    HTTPException
)

from bson import ObjectId

from app.api.dependencies.auth_dependency import get_current_user

from app.services.ingestion.log_ingestion_service import (
    process_uploaded_log
)

from app.models.log_model import (
    raw_logs_collection,
    parsed_logs_collection
)

router = APIRouter(
    prefix="/logs",
    tags=["Logs"]
)


@router.post("/upload")
async def upload_log_file(
    file: UploadFile = File(...),
    current_user=Depends(get_current_user)
):

    allowed_extensions = (
        ".log",
        ".txt",
        ".json"
    )

    if not file.filename.endswith(allowed_extensions):
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type"
        )

    content = await file.read()

    file_content = content.decode("utf-8")

    result = await process_uploaded_log(
        filename=file.filename,
        content_type=file.content_type,
        uploaded_by=current_user["email"],
        file_content=file_content
    )

    return {
        "message": "Log uploaded successfully",
        "data": result
    }


@router.get("/")
async def get_uploaded_logs(
    current_user=Depends(get_current_user)
):

    logs = []

    async for log in raw_logs_collection.find():

        logs.append({
            "id": str(log["_id"]),
            "filename": log["filename"],
            "uploaded_by": log["uploaded_by"],
            "uploaded_at": log["uploaded_at"]
        })

    return logs


@router.get("/{log_id}")
async def get_log_details(
    log_id: str,
    current_user=Depends(get_current_user)
):

    log = await raw_logs_collection.find_one(
        {"_id": ObjectId(log_id)}
    )

    if not log:
        raise HTTPException(
            status_code=404,
            detail="Log not found"
        )

    parsed_logs = []

    async for parsed_log in parsed_logs_collection.find(
        {"raw_log_id": log_id}
    ):
        parsed_log["_id"] = str(parsed_log["_id"])
        parsed_logs.append(parsed_log)

    return {
        "raw_log": {
            "id": str(log["_id"]),
            "filename": log["filename"],
            "uploaded_by": log["uploaded_by"]
        },
        "parsed_logs": parsed_logs
    }


@router.delete("/{log_id}")
async def delete_log(
    log_id: str,
    current_user=Depends(get_current_user)
):

    await raw_logs_collection.delete_one(
        {"_id": ObjectId(log_id)}
    )

    await parsed_logs_collection.delete_many(
        {"raw_log_id": log_id}
    )

    return {
        "message": "Log deleted successfully"
    }