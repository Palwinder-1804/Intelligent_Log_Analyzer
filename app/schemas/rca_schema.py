from fastapi import (
    APIRouter,
    Depends
)

from app.api.dependencies.auth_dependency import (
    get_current_user
)

from app.schemas.llm_schema import (
    IncidentExplainRequest
)

from app.services.llm.incident_explainer_service import (
    explain_incident
)

router = APIRouter(
    prefix="/llm",
    tags=["LLM"]
)


@router.post("/explain")
async def explain_log_incident(
    request: IncidentExplainRequest,
    current_user=Depends(get_current_user)
):

    result = await explain_incident(
        request.query
    )

    return result