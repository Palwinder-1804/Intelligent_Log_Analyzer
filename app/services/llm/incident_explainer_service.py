from app.services.llm.rag_chain_service import (
    run_rag_incident_chain
)


async def explain_incident(query: str):

    result = await run_rag_incident_chain(query)

    return result