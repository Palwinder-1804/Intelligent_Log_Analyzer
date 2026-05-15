from fastapi import (
    APIRouter,
    Depends
)

from app.api.dependencies.auth_dependency import (
    get_current_user
)

from app.services.rag.retrieval_service import (
    retrieve_similar_logs
)

router = APIRouter(
    prefix="/rag",
    tags=["RAG"]
)


@router.post("/search")
async def search_logs(
    query: str,
    current_user=Depends(get_current_user)
):

    results = retrieve_similar_logs(query)

    formatted_results = []

    for result in results:

        formatted_results.append({
            "content": result.page_content,
            "metadata": result.metadata
        })

    return {
        "query": query,
        "results": formatted_results
    }


