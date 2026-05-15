from fastapi import (
    APIRouter,
    Depends
)

from app.api.dependencies.auth_dependency import (
    get_current_user
)

from app.schemas.rca_schema import (
    RCARequest
)

from app.services.rca.root_cause_service import (
    analyze_root_cause
)

router = APIRouter(
    prefix="/rca",
    tags=["Root Cause Analysis"]
)


@router.post("/analyze")
async def perform_root_cause_analysis(
    request: RCARequest,
    current_user=Depends(get_current_user)
):

    result = await analyze_root_cause(
        request.query
    )

    return result